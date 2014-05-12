python-rightscale
=================

A python wrapper for the Rightscale API.  At the moment, this only supports the 1.0 API and Rightscale's OAuth token authentication.

Most operations currently require you to know the rightscale HTTP API you are invoking, unless you're running a rightscript on a single server in which case I've written a helper function for that.


Usage examples
--------------

**Setting up your auth token**

```
from rightscale import rightscale
api = rightscale('account#','refreshtoken',oauth_endpoint='oauth-endpoint',api_endpoint='oauth-endpoint')
api.login()
```

account# is the account number listed in your Rightscale URL

refreshtoken is the refresh token issued to you when you enabled api access

oauth-endpoint is the rightscale subdomain the api access page told you to hit (i.e. us-4, my, us-3).  This defaults to "my" if you don't provide anything.

**Running a rightscript on a single server**

```
payload = { 'SYS_TZINFO': 'text:US/Pacific'}

api.run_script('serverid', 'script_id', payload)
```

serverid is the numeric server identifier taken from the Rightscale url of the server's page.

script_id is the number id of the script taken from the Rightscale url of the script's page.

payload is a python dict in the format INPUT_NAME: value

run_script will run your rightscript on the specified server and then return the audit status of the script every 5 seconds until completed.

**Getting a list of all servers**

```
server_list = api.send('servers')
```

server_list ends up being a python list of every server in your account.

**Rebooting a server**

```
response = api.send('servers/######/reboot')
```

where ###### is the numeric server identifier from the rightscale url.


Rightscale API documentation is available at http://support.rightscale.com/12-Guides/03-Rightscale_API
