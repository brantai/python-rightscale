"""
Python-Rightscale

A stupid wrapper around rightscale's HTTP API
"""
import types
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

# In theory, RightScale's API is discoverable through ``links`` in responses.
# In practice, we have to help our robots along with the following hints:
RS_DEFAULT_ACTIONS = {
        'index': {
            'http_method': 'get',
            },
        'show': {
            'http_method': 'get',
            'extra_path': '/%(res_id)s',
            },
        'create': {
            'http_method': 'post',
            },
        'update': {
            'http_method': 'put',
            'extra_path': '/%(res_id)s',
            },
        'destroy': {
            'http_method': 'delete',
            'extra_path': '/%(res_id)s',
            },
        }

# Specify variations from the default actions defined in RS_DEFAULT_ACTIONS.
# These specs come from http://reference.rightscale.com/api1.5/index.html
RS_REST_ACTIONS = {

        'account_groups': {
            'create': None,
            'update': None,
            'destroy': None,
            },

        'accounts': {
            'index': None,
            'create': None,
            'update': None,
            'destroy': None,
            },

        'alerts': {
            'disable': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/disable',
                },
            'enable': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/enable',
                },
            'quench': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/quench',
                },
            'create': None,
            'update': None,
            'destroy': None,
            },

        'audit_entries': {
            'append': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/append',
                },
            'detail': {
                'http_method': 'get',
                'extra_path': '/%(res_id)s/detail',
                },
            'destroy': None,
            },

        'backups': {
            'cleanup': {
                'http_method': 'post',
                'extra_path': '/cleanup',
                },
            },

        'child_accounts': {
            'show': None,
            'destroy': None,
            },

        'cloud_accounts': {
            'update': None,
            },

        'clouds': {
            'create': None,
            'update': None,
            'destroy': None,
            },

        # these are only in the 1.5 docs and are not available as hrefs.
        'cookbook_attachments': {
            'multi_attach': {
                'http_method': 'post',
                'extra_path': '/multi_attach',
                },
            'multi_detach': {
                'http_method': 'post',
                'extra_path': '/multi_detach',
                },
            'update': None,
            },

        'cookbooks': {
            'follow': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/follow',
                },
            'freeze': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/freeze',
                },
            'obsolete': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/obsolete',
                },
            'create': None,
            'update': None,
            },

        'deployments': {
            'clone': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/clone',
                },
            'lock': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/lock',
                },
            'servers': {
                'http_method': 'get',
                'extra_path': '/%(res_id)s/servers',
                },
            'unlock': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/unlock',
                },
            },

        'identity_providers': {
            'create': None,
            'update': None,
            'destroy': None,
            },

        'multi_cloud_images': {
            'clone': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/clone',
                },
            'commit': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/commit',
                },
            },

        'permissions': {
            'update': None,
            },

        # only in 1.5 api docs, not discoverable via href
        'placement_groups': {
            'update': None,
            },

        'preferences': {
            'create': None,
            },

        'publication_lineages': {
            'index': None,
            'create': None,
            'update': None,
            'destroy': None,
            },

        'publications': {
            'import': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/import',
                },
            'create': None,
            'update': None,
            'destroy': None,
            },

        'repositories': {
            'cookbook_import': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/cookbook_import',
                },
            'refetch': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/refetch',
                },
            'resolve': {
                'http_method': 'post',
                'extra_path': '/resolve',
                },
            },

        'right_scripts': {
            'create': None,
            'update': None,
            'destroy': None,
            },

        # rs api 1.5 returns a link where rel=self for the ``/api/sessions``
        # resource.  sadly, the href=/api/session.  regardless, we don't need
        # it as an attribute because it's where we started off.
        'self': None,

        'server_arrays': {
            'clone': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/clone',
                },
            'current_instances': {
                'http_method': 'get',
                'extra_path': '/%(res_id)s/current_instances',
                },
            'launch': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/launch',
                },
            'multi_run_executable': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/multi_run_executable',
                },
            'multi_terminate': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/multi_terminate',
                },
            },

        'server_template_multi_cloud_images': {
            'make_default': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/make_default',
                },
            'update': None,
            },

        'server_templates': {
            'clone': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/clone',
                },
            'commit': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/commit',
                },
            'detect_changes_in_head': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/detect_changes_in_head',
                },
            'publish': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/publish',
                },
            'resolve': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/resolve',
                },
            'swap_repository': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/swap_repository',
                },
            },

        'servers': {
            'clone': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/clone',
                },
            'launch': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/launch',
                },
            'terminate': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/terminate',
                },
            },

        # workaround inconsistency in rs hateoas
        'sessions': {
            'accounts': {
                'http_method': 'get',
                'extra_path': '/accounts',
                },
            'index': None,
            'show': None,
            'create': None,
            'update': None,
            'destroy': None,
            },

        'tags': {
            'by_resource': {
                'http_method': 'post',
                'extra_path': '/by_resource',
                },
            'by_tag': {
                'http_method': 'post',
                'extra_path': '/by_tag',
                },
            'multi_add': {
                'http_method': 'post',
                'extra_path': '/multi_add',
                },
            'multi_delete': {
                'http_method': 'post',
                'extra_path': '/multi_delete',
                },
            'index': None,
            'show': None,
            'create': None,
            'update': None,
            'destroy': None,
            },

        'users': {
            'destroy': None,
            },

        }


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
            action_templates=RS_REST_ACTIONS,
            ):
        """
        Creates and configures the API object.
        :param str refresh_token: The refresh token provided by Rightscale when
            API access is enabled.
        :param api_endpoint: The rightscale subdomain to be hit with API
            requests.
        :param str api_prepath: A string to prepend to partial resource paths.
            E.g. ``/api/``.
        :param dict action_templates: A map of templates that is used to create
            the "action" methods on RightScaleResource objects.
        """
        self.oauth_url = None
        self.api_endpoint = api_endpoint
        self.refresh_token = refresh_token
        self.auth_token = None
        self.api_prepath = api_prepath
        self.action_templates = action_templates
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
        for name, action in self.action_templates.iteritems():
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
        tpl = self.action_templates.get(name)
        if tpl:
            actions.update(tpl)
        return RightScaleResource(path, self.client, actions)
