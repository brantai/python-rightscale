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

# this *should* be discoverable from the '/api/sessions' route above, but it is
# not.  there is an open ticket filed with rightscale.  until it gets
# addressed, it's another piece of magic:
ACCOUNT_INFO_RES_PATH = DEFAULT_API_PREPATH + 'sessions/accounts'

# In theory, RightScale's API is discoverable through ``links`` in responses.
# In practice, we have to help our robots along with the following hints:
REST_HINTS = {
        # using unicodes below just to be consistent with what is discovered
        # directly from the http requests
        'add': {
            u'sessions.accounts': unicode(ACCOUNT_INFO_RES_PATH),
            },
        'remove': [
            u'accounts.index',
            u'self'
            ],
        }

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

RS_REST_ACTIONS = {

        'accounts': {
            'index': None,
            'create': None,
            'update': None,
            'destroy': None,
            },

        'self': None,

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
    def __init__(self, path, client, actions=RS_DEFAULT_ACTIONS):
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
        client = RESTOAuthClient(api_endpoint, ROOT_RES_PATH, REST_HINTS)
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

    def run_script(self, server_id, script_id, inputs=None):
        """
        Convenience function to run a rightscript on a single server and verify
        its status.

        :param server_id: the Rightscale server id taken from the url of the
            server
        :param script_id: the id of the Rightscript to run on the server, taken
            from the url of the rightscript
        :param inputs (optional): a dict of the inputs to pass to the
            rightscript, in the format 'INPUT NAME': 'text:Value'
        """
        api_request = 'cloud/%s/instances/%s/run_executable' % (
            self.cloud_id,
            server_id,
            )
        script_href = '/api/right_script/%s' % (script_id)
        payload = {'right_script_href': script_href}
        input_list = []
        if inputs:
            for key in inputs:
                input_list.append('[name]=' + key)
            input_list.append('[value]' + inputs[key])
            payload['inputs[]'] = input_list
        response = self.client.post(api_request, payload)
        return response

    def list_instances(self, deployment=None, view='tiny'):
        """
        Returns a list of instances from your account.

        :param deployment (optional): If provided, only lists servers in the
            specified deployment
        """
        filters = ['state==operational']
        if deployment:
            filters.append(
                'deployment_href==/api/deployments/' + deployment
                )
        params = {'filter[]': filters, 'view': view}
        # TODO: replace with cloud id discovered from self.links
        api_request = DEFAULT_API_PREPATH + 'clouds/1/instances'
        response = self.client.get(api_request, params=params)
        # TODO: return something more meaningful once we know what format it
        # comes back in.
        return response.json()
        # instance_list = {}
        # for svr in response:
        #     instance_list[svr['resource_uid']] = svr
        # return instance_list

    def get_accounts(self):
        """
        Returns the RightScale accounts available using the login creds
        for the API call.
        """
        return self.client.get(ACCOUNT_INFO_RES_PATH).json()

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
