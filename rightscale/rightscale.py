"""
Python-Rightscale

A stupid wrapper around rightscale's HTTP API
"""
import types
from .actions import RS_DEFAULT_ACTIONS, RS_REST_ACTIONS
from .httpclient import RESTOAuthClient
from .util import get_rc_creds


# magic strings from the 1.5 api
DEFAULT_API_PREPATH = '/api/'
ROOT_RES_PATH = DEFAULT_API_PREPATH + 'sessions'

# these *should* be discoverable from the '/api/sessions' route above, but they
# are not.  there is an open ticket filed with rightscale.  until it gets
# addressed, it's just more magic:
ACCOUNT_INFO_RES_PATH = DEFAULT_API_PREPATH + 'sessions/accounts'
HEALTH_CHECK_RES_PATH = DEFAULT_API_PREPATH + 'health-check'


def get_resource_method(name, template):
    """
    Creates a function that is suitable as a method for RightScaleResource.
    """
    def rsr_meth(self, **kwargs):
        http_method = template['http_method']
        extra_path = template.get('extra_path')
        if extra_path:
            fills = {'res_id': kwargs.pop('res_id', '')}
            path = self.path + (extra_path % fills)
        else:
            path = self.path
        return self.client.request(http_method, path, **kwargs)
    rsr_meth.__name__ = name
    return rsr_meth


class RightScaleLinkyThing(dict):
    @property
    def links(self):
        rel_hrefs = self.get('links', [])
        return dict((raw['rel'], raw['href']) for raw in rel_hrefs)


class RightScaleResource(object):
    def __init__(self, path, client, actions):
        self.path = path
        self.client = client
        for name, template in actions.items():
            if not template:
                continue
            method = get_resource_method(name, template)
            setattr(self, name, types.MethodType(method, self, self.__class__))


class RightScale(object):

    def __init__(
            self,
            refresh_token=None,
            api_endpoint=None,
            api_prepath=DEFAULT_API_PREPATH,
            ):
        """
        Creates and configures the API object.
        :param str refresh_token: The refresh token provided by Rightscale when
            API access is enabled.
        :param api_endpoint: The rightscale subdomain to be hit with API
            requests.
        :param str api_prepath: A string to prepend to partial resource paths.
            E.g. ``/api/``.
        """
        self.oauth_url = None
        self.api_endpoint = api_endpoint
        self.refresh_token = refresh_token
        self.auth_token = None
        self.api_prepath = api_prepath
        self._client = None

    @property
    def client(self):
        if not self._client:
            self.login()
        return self._client

    def login(self):
        """
        Gets and stores an OAUTH token from Rightscale.
        """
        rc_creds = get_rc_creds()

        if self.api_endpoint is not None:
            api_endpoint = self.api_endpoint
        else:
            api_endpoint = rc_creds[0]
        if not api_endpoint:
            raise ValueError("Can't login with no api endpoint.")

        if self.refresh_token is not None:
            refresh_token = self.refresh_token
        else:
            refresh_token = rc_creds[1]
        if not refresh_token:
            raise ValueError("Can't login. Need refresh token!")

        self.oauth_url = api_endpoint + DEFAULT_API_PREPATH + 'oauth2'
        client = RESTOAuthClient(api_endpoint, ROOT_RES_PATH)
        client.headers['X-API-Version'] = '1.5'
        login_data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            }
        response = client.post(url=self.oauth_url, data=login_data)
        if not response.ok:
            response.raise_for_status()

        raw_token = response.json()
        self.auth_token = "Bearer %s" % raw_token['access_token']
        client.headers['Authorization'] = self.auth_token
        self._client = client

    def health_check(self):
        # only in 1.5 api docs, not discoverable via href
        return self.client.get(HEALTH_CHECK_RES_PATH).json()

    def _resources(self):
        rs_root = RightScaleLinkyThing(self.client.root_response)
        links = rs_root.links
        for name, action in RS_REST_ACTIONS.iteritems():
            if action is None:
                del links[name]
                continue
            if name not in links:
                links[unicode(name)] = unicode(self.api_prepath + name)
        return links

    def __dir__(self):
        return self._resources().keys()

    def __getattr__(self, name):
        path = self._resources().get(name)
        if not path:
            raise AttributeError('%s object has no attribute %s' % (
                self.__class__.__name__,
                name,
                ))
        actions = RS_DEFAULT_ACTIONS.copy()
        tpl = RS_REST_ACTIONS.get(name)
        if tpl:
            actions.update(tpl)
        return RightScaleResource(path, self.client, actions)
