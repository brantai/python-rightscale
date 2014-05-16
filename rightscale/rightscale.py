"""
Python-Rightscale

A stupid wrapper around rightscale's HTTP API
"""
from .httpclient import RESTOAuthClient
from .util import get_rc_creds


DEFAULT_API_ENDPOINT = 'https://us-3.rightscale.com'
DEFAULT_API_PREPATH = '/api/'
ROOT_RES_PATH = DEFAULT_API_PREPATH + 'sessions'


class RightScale(object):
    def __init__(
            self,
            refresh_token=None,
            api_endpoint=DEFAULT_API_ENDPOINT,
            ):
        """
        Creates and configures the API object.
        :param str account: The Rightscale account number
        :param str refresh_token: The refresh token provided by Rightscale when
            API access is enabled.
        :param api_endpoint: The rightscale subdomain to be hit with API
            requests.  Defaults to 'my'.
        :param oauth_endpoint: The rightscale subdomain to be hit with OAuth
            token requests.  Defaults to 'us-3'.
        """
        self.api_endpoint = api_endpoint
        self.oauth_url = api_endpoint + DEFAULT_API_PREPATH + 'oauth2'
        if refresh_token is not None:
            self.refresh_token = refresh_token
        self.auth_token = None
        self._client = None

    @property
    def client(self):
        if not self._client:
            self.login()
        return self._client

    @property
    def links(self):
        response = self.client.get(ROOT_RES_PATH)
        if not response.ok:
            return {}
        # TODO: debug log the raw
        blob = response.json()
        return dict((raw['rel'], raw['href']) for raw in blob.get('links', []))

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

        client = RESTOAuthClient(self.api_endpoint)
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
