"""
Python-Rightscale

A stupid wrapper around rightscale's HTTP API
"""
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


class RightScale(object):

    def __init__(
            self,
            refresh_token=None,
            api_endpoint=None,
            ):
        """
        Creates and configures the API object.
        :param str refresh_token: The refresh token provided by Rightscale when
            API access is enabled.
        :param api_endpoint: The rightscale subdomain to be hit with API
            requests.
        """
        self.oauth_url = None
        if api_endpoint is not None:
            self.api_endpoint = api_endpoint
        if refresh_token is not None:
            self.refresh_token = refresh_token
        self.auth_token = None
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
        if hasattr(self, 'refresh_token'):
            # when specified to the constructor, take the user at its word.
            # don't try to fall back to the rc file because they may be trying
            # to login to a different account and we don't want to surprise
            # them.  if they passed in None, shame on them.
            refresh_token = self.refresh_token
        else:
            rc_creds = get_rc_creds()
            refresh_token = rc_creds[1]
        if not refresh_token:
            raise ValueError("Can't login. Need refresh token!")
        self.refresh_token = refresh_token

        if hasattr(self, 'api_endpoint'):
            api_endpoint = self.api_endpoint
        else:
            rc_creds = get_rc_creds()
            api_endpoint = rc_creds[0]

        if not api_endpoint:
            raise ValueError("Can't login with no api endpoint.")
        self.api_endpoint = api_endpoint

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
