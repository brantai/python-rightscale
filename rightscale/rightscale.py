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


class Resource(object):
    """
    A single resource.

    :param dict soul: The essence of the resource as returned by the RightScale
        API.  This is the dictionary of attributes originally returned as the
        JSON body of the HTTP response from RightScale.

    """
    def __init__(self, soul=None):
        if soul is None:
            soul = {}
        self.soul = soul
        self._links = None

    @property
    def links(self):
        # only initialize once, not if empty
        if self._links is None:
            rel_hrefs = self.soul.get('links', [])
            self._links = dict((raw['rel'], raw['href']) for raw in rel_hrefs)
        return self._links


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
        self.auth_token = None
        self.path = path

        rc_creds = get_rc_creds()

        # prevent dumb leakage from the environment by only grabbing creds from
        # rc file if they are not specified to the constructor.
        if api_endpoint is None:
            api_endpoint = rc_creds[0]
        if not api_endpoint:
            raise ValueError("Can't login with no api endpoint.")
        self.api_endpoint = api_endpoint

        if refresh_token is None:
            refresh_token = rc_creds[1]
        if not refresh_token:
            raise ValueError("Can't login. Need refresh token!")
        self.refresh_token = refresh_token

        self._client = HTTPClient(
                api_endpoint,
                ROOT_RES_PATH,
                {'X-API-Version': '1.5'},
                )

    @property
    def client(self):
        # lazy login so you can create instances without triggering a net hit
        if not self.auth_token:
            self.login()
        return self._client

    def login(self):
        """
        Gets and stores an OAUTH token from Rightscale.
        """
        login_data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            }
        client = self._client
        response = client.post(OAUTH2_RES_PATH, data=login_data)
        if not response.ok:
            response.raise_for_status()

        raw_token = response.json()
        self.auth_token = "Bearer %s" % raw_token['access_token']
        client.s.headers['Authorization'] = self.auth_token

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
