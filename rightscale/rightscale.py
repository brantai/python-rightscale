"""
Python-Rightscale

A stupid wrapper around rightscale's HTTP API
"""
import requests
import time


def _get(url, headers, payload=None):
    """
    Internal method to make HTTP GET requests
    """
    if payload:
        response = requests.get(url, headers=headers, data=payload)
    else:
        response = requests.get(url, headers=headers)
    output = response.json()
    return output


def _post(url, headers, payload=None):
    """
    Internal method to make HTTP POST requests
    """
    if payload:
        response = requests.post(url, data=payload, headers=headers)
    else:
        response = requests.post(url, headers=headers)
    return response


def _verify(v_url, headers):
    """
    Internal method to return the progress of an API call until it is completed
    """
    status = 'unknown'
    v = _get(v_url, headers)
    while status != 'completed':
        time.sleep(5)
        v = _get(v_url, headers)
        status = v['state']
        print status
    return v


class RightScale(object):
    def __init__(
            self,
            account,
            refresh_token,
            api_endpoint='my',
            oauth_endpoint='my',
            cloud_id='1'
            ):
        """
        Creates and configures the API object.
        :param account: The Rightscale account number
        :param refresh_token: The refresh token provided by Rightscale when API
            access is enabled.
        :param api_endpoint: The rightscale subdomain to be hit with API
            requests.  Defaults to 'my'.
        :param oauth_endpoint: The rightscale subdomain to be hit with OAuth
            token requests.  Defaults to 'my'.
        """
        self.account = account
        self.oauth_url = (
                'https://%s.rightscale.com/api/oauth2'
                % oauth_endpoint
                )
        self.refresh_token = refresh_token
        self.api_url = 'https://%s.rightscale.com/api/' % api_endpoint
        self.auth_token = None
        self.headers = {'X-API-Version': '1.5'}
        self.cloud_id = cloud_id

    def login(self):
        """
        Gets and stores an OAUTH token from Rightscale.
        """
        login_data = {
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token,
                }
        response = requests.post(
                self.oauth_url,
                headers=self.headers,
                data=login_data,
                )

        if response.status_code == requests.codes.ok:
            raw_token = response.json()
            self.auth_token = "Bearer %s" % raw_token['access_token']
            self.headers['Authorization'] = self.auth_token
            return True

        return False

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
        api_request = '%scloud/%s/instances/%s/run_executable' % (
                self.api_url,
                self.cloud_id,
                server_id,
                )
        script_href = '/api/right_script/%s' % (script_id)
        payload = {}
        payload['right_script_href'] = script_href
        input_list = []
        if inputs:
            for key in inputs:
                input_list.append('[name]=' + key)
            input_list.append('[value]' + inputs[key])
        payload['inputs[]'] = input_list
        response = _post(api_request, self.headers, payload)
#       _verify(response.headers['location'],self.headers)
        return response

    def send(self, uri, method='get', verify=False, payload=None):
        """
        Sends an API request.

        :param uri: The API URI of the request.  This consists of everything in
            a URL after the account id.
        :param method (optional): the HTTP method to use in the call.  Current
            supports GET and POST.  Defaults to GET.
        :param verify (optional): Boolean to indicate if the POST status should
            be tracked.
        :param payload (optional): dict containing any POST data to be
            conveyed.
        """
        api_request = self.api_url + uri
        if method.lower() == 'get':
            response = _get(api_request, self.headers)
        elif method.lower() == 'post':
            if payload:
                response = _post(api_request, self.headers, payload)
            else:
                response = _post(api_request, self.headers)

            if verify and response.headers['location']:
                _verify(response.headers['location'], self.headers)

        return response

    def list_instances(self, deployment=None):
        """
        Returns a list of instances from your account.

        :param deployment (optional): If provided, only lists servers in the
            specified deployment
        """
        if deployment:
            search_filter = [
                    'state==operational',
                    'deployment_href==/api/deployments/' + deployment,
                    ]
            payload = {'filter[]': search_filter}
        else:
            payload = {'filter[]': 'state==operational'}
        api_request = self.api_url + 'clouds/' + self.cloud + '/instances'
        response = _get(api_request, self.headers, payload=payload)
        instance_list = {}
        for svr in response:
            instance_list[svr['resource_uid']] = svr

        return instance_list
