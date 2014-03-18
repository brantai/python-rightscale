"""
Python-Rightscale

A stupid wrapper around rightscale's HTTP API
"""

import requests
import json
import time

def _get(url,headers,params):
	"""
	Internal method to make HTTP GET requests
	"""
	response = requests.get(url, headers=headers, params=params)
	output = response.json()
	return output

def _post(url,headers,params,payload=None):
	"""
	Internal method to make HTTP POST requests
	"""
	if payload:
		response = requests.post(url,data=payload,headers=headers,params=params)
	else:
		response = requests.post(url,headers=headers,params=params)
	return response

def _verify(v_url,headers,params):
	"""
	Internal method to return the progress of an API call until it is completed
	"""
	status = 'unknown'
	v = _get(v_url,headers,params)
	while status != 'completed':
		time.sleep(5)
		v = _get(v_url,headers,params)
	        status = v['state']
		print status
	return v

class rightscale:
    def __init__(self, account, refresh_token, api_endpoint='my', oauth_endpoint='my', api_level='1.0'):
	    """
	    Creates and configures the API object.
	    :param account: The Rightscale account number
	    :param refresh_token: The refresh token provided by Rightscale when API access is enabled.
	    :param api_endpoint: The rightscale subdomain to be hit with API requests.  Defaults to 'my'.
	    :param oauth_endpoint: The rightscale subdomain to be hit with OAuth token requests.  Defaults to 'my'.
	    :param api_level: The rightscale api level for requests.  Currently defaults to '1.0' because 1.5 support isn't here yet.
	    """
	    self.account = account
	    self.oauth_url = 'https://%s.rightscale.com/api/acct/%s/oauth2' % (oauth_endpoint, account)
	    self.refresh_token = refresh_token
	    self.api_url = 'https://%s.rightscale.com/api/' % (api_endpoint)
	    self.api_level = api_level
            self.auth_token = None
	    self.headers = {'X-API-Version': self.api_level}
	    self.url_params = {'format': 'js'}

    def login(self):
	    """
	    Gets and stores an OAUTH token from Rightscale.
	    """
	    login_data = {'grant_type': 'refresh_token', 'refresh_token': self.refresh_token}
	    response = requests.post(self.oauth_url, headers=self.headers, params=self.url_params, data=login_data)

	    if response.status_code == requests.codes.ok:
		    raw_token = response.json()
		    self.auth_token = "Bearer %s" % raw_token['access_token']
		    self.headers['Authorization'] = self.auth_token
		    return True

	    return False


    def run_script(self,server_id,script_id,inputs=None):
	    """
	    Convenience function to run a rightscript on a single server and verify its status.
	    :param server_id: the Rightscale server id taken from the url of the server
	    :param script_id: the id of the Rightscript to run on the server, taken from the url of the rightscript
	    :param inputs (optional): a dict of the inputs to pass to the rightscript, in the format 'INPUT NAME': 'text:Value'
	    """
	    api_request = self.api_url + 'acct/%s/servers/%s/run_script' % (self.account,server_id) 
            script_href = '%sacct/%s/right_script/%s' % (self.api_url,self.account,script_id)
	    payload = {}
	    payload['server[right_script_href]'] = script_href
	    if inputs:
	        for key in inputs:
		        payload['server[parameters]['+key+']'] = inputs[key]
	    response = _post(api_request, self.headers,self.url_params,payload)
	    _verify(response.headers['location'],self.headers,self.url_params)
	    return response
		    

    def send(self,uri,method='get',verify=False,payload=None):
	    """
	    Sends an API request.
	    :param uri: The API URI of the request.  This consists of everything in a URL after the account id.
	    :param method (optional): the HTTP method to use in the call.  Current supports GET and POST.  Defaults to GET.
	    :param verify (optional): Boolean to indicate if the POST status should be tracked.
	    :param payload (optional): dict containing any POST data to be conveyed.
	    """
	    api_request=self.api_url + uri
	    if method.lower() == 'get':
		    response = _get(api_request,self.headers,self.url_params)
            elif method.lower() == 'post':
		    if payload:
		        response = _post(uri,self.headers,self.url_params,payload)
		    else:
			response = _post(uri,self.headers,self.url_params)
	    
	            if verify and response.headers['location']:
			_verify(response.headers['location'],self.headers,self.url_params)
	    
	    return response

