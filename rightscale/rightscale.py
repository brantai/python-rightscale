"""
Python-Rightscale

A stupid wrapper around rightscale's HTTP API
"""
import types
from .actions import RS_DEFAULT_ACTIONS, COLLECTIONS
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

        loc = response.headers.get('location', None)

        if loc:
            # If the returned code is a 201, then there should be a location
            # header in the response that we can use to re-get the newly created
            # resource.
            loc = response.headers.get('location')
            response = self.client.get(loc, **kwargs)

        # At this point, we better have a valid JSON response object
        try:
            obj = response.json()
        except:
            # The response had no JSON ... not a resource object
            return

        if COLLECTION_TYPE in response.content_type:
            ret = HookList(
                    [Resource(r, path, response, self.client) for r in obj],
                    response=response
                    )
        else:
            ret = Resource(obj, path, response, self.client)
        return ret

    rsr_meth.__name__ = name
    return rsr_meth


class Resource(object):
    """
    A single resource.

    :param dict soul: The essence of the resource as returned by the RightScale
        API.  This is the dictionary of attributes originally returned as the
        JSON body of the HTTP response from RightScale.

    :param str path: The path portion of the URL.  E.g. ``/api/clouds/1``.

    :param rightscale.httpclient.HTTPResponse response: The raw response object
        returned by :meth:`HTTPClient.request`.

    """
    def __init__(self, soul=None, path='', response=None, client=None):
        if soul is None:
            soul = {}
        self.soul = soul
        self.path = path
        self.collection_actions = {}
        self.response = response
        self.client = client
        self._links = None

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.soul)

    def __str__(self):
        return str(self.soul)

    def __cmp__(self, other):
        return cmp(self.soul, other.soul)

    @property
    def content_type(self):
        if self.response:
            return self.response.content_type[0]
        return ''

    def _get_rel_hrefs(self):
        rel_hrefs = self.soul.get('links', [])
        return dict((raw['rel'], raw['href']) for raw in rel_hrefs)

    @property
    def href(self):
        return self._get_rel_hrefs().get('self', '')

    @property
    def links(self):
        # only initialize once, not if empty
        if self._links is None:
            _links = self._get_rel_hrefs()

            collection_actions = COLLECTIONS.get(self.content_type, {})
            self.collection_actions = collection_actions
            for name, action in collection_actions.iteritems():
                if action is None and name in _links:
                    del _links[name]
                    continue
                if name not in _links:
                    _links[unicode(name)] = unicode(
                            '%s/%s' % (self.path, name)
                            )

            self._links = _links
        return self._links

    def __dir__(self):
        return self.links.keys()

    def __getattr__(self, name):
        path = self.links.get(name)
        if not path:
            raise AttributeError('%s object has no attribute %s' % (
                self.__class__.__name__,
                name,
                ))
        actions = RS_DEFAULT_ACTIONS.copy()
        tpl = self.collection_actions.get(name)
        if tpl:
            actions.update(tpl)
        return ResourceCollection(path, self.client, actions)


class ResourceCollection(object):
    def __init__(self, path, client, actions):
        self.path = path
        self.client = client
        for name, template in actions.items():
            if not template:
                continue
            method = get_resource_method(name, template)
            setattr(self, name, types.MethodType(method, self, self.__class__))


class RightScale(Resource):

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
        super(RightScale, self).__init__({}, path)
        self.auth_token = None

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

        self.client = HTTPClient(
                api_endpoint,
                {'X-API-Version': '1.5'},
                OAUTH2_RES_PATH,
                refresh_token,
                )

    def health_check(self):
        # only in 1.5 api docs, not discoverable via href
        return self.client.get(HEALTH_CHECK_RES_PATH).json()

    @property
    def links(self):
        if not self.soul:
            try:
                response = self.client.get(ROOT_RES_PATH)
                self.response = response
                self.soul = response.json()
            except:
                self.soul = {}
        return super(RightScale, self).links
