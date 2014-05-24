"""
Python-Rightscale

A stupid wrapper around rightscale's HTTP API
"""
import types
from .actions import RS_DEFAULT_ACTIONS, RS_REST_ACTIONS
from .httpclient import HTTPClient
from .util import get_rc_creds, HookList


# magic strings from the 1.5 api
DEFAULT_API_PREPATH = '/api'

# authenticate here
OAUTH2_RES_PATH = '/'.join((DEFAULT_API_PREPATH, 'oauth2'))

# start hypermedia searches here
ROOT_RES_PATH = '/'.join((DEFAULT_API_PREPATH, 'sessions'))

# these *should* be discoverable from the '/api/sessions' route above, but they
# are not.  there is an open ticket filed with rightscale.  until it gets
# addressed, it's just more magic:
ACCOUNT_INFO_RES_PATH = '/'.join((DEFAULT_API_PREPATH, 'sessions/accounts'))
HEALTH_CHECK_RES_PATH = '/'.join((DEFAULT_API_PREPATH, 'health-check'))

COLLECTION_TYPE = 'type=collection'


def get_resource_method(name, template):
    """
    Creates a function that is suitable as a method for ResourceCollection.
    """
    def rsr_meth(self, **kwargs):
        http_method = template['http_method']
        extra_path = template.get('extra_path')
        if extra_path:
            fills = {'res_id': kwargs.pop('res_id', '')}
            path = self.path + (extra_path % fills)
        else:
            path = self.path
        response = self.client.request(http_method, path, **kwargs)
        content_type = response.headers['content-type']
        ct_fields = content_type.split(';')
        obj = response.json()
        if COLLECTION_TYPE in ct_fields:
            ret = HookList([Resource(r) for r in obj])
        else:
            ret = Resource(obj)
        ret.response = response
        return ret
    rsr_meth.__name__ = name
    return rsr_meth


class Resource(dict):
    @property
    def links(self):
        rel_hrefs = self.get('links', [])
        return dict((raw['rel'], raw['href']) for raw in rel_hrefs)


class ResourceCollection(object):
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
            path=DEFAULT_API_PREPATH,
            refresh_token=None,
            api_endpoint=None,
            ):
        """
        Creates and configures the API object.
        :param str refresh_token: The refresh token provided by Rightscale when
            API access is enabled.
        :param api_endpoint: The rightscale subdomain to be hit with API
            requests.
        :param str path: The path portion of the URL.
            E.g. ``/api``.
        """
        self.api_endpoint = api_endpoint
        self.refresh_token = refresh_token
        self.auth_token = None
        self.path = path
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

        client = HTTPClient(api_endpoint, ROOT_RES_PATH)
        client.s.headers['X-API-Version'] = '1.5'
        login_data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            }
        response = client.post(OAUTH2_RES_PATH, data=login_data)
        if not response.ok:
            response.raise_for_status()

        raw_token = response.json()
        self.auth_token = "Bearer %s" % raw_token['access_token']
        client.s.headers['Authorization'] = self.auth_token
        self._client = client

    def health_check(self):
        # only in 1.5 api docs, not discoverable via href
        return self.client.get(HEALTH_CHECK_RES_PATH).json()

    def _resources(self):
        rs_root = Resource(self.client.root_response)
        links = rs_root.links
        for name, action in RS_REST_ACTIONS.iteritems():
            if action is None:
                del links[name]
                continue
            if name not in links:
                links[unicode(name)] = unicode('%s/%s' % (self.path, name))
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
        return ResourceCollection(path, self.client, actions)
