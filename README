python-rightscale
=================

A python wrapper for the Rightscale API.  At the moment, this only supports the 1.0 API and Rightscale's OAuth token authentication.

Most operations currently require you to know the rightscale HTTP API you are invoking, unless you're running a rightscript on a single server in which case I've written a helper function for that.


Usage examples
--------------

**Setting up your auth token**

```
import rightscale
api = rightscale.RightScale(refresh_token='token',api_endpoint='api-endpoint')
```

refreshtoken is the refresh token issued to you when you enabled api access.
api_endpoint is the FQDN of "Token Endpoint (API 1.5)" from the same page.

**Getting a list of all servers**

```
server_list = api.list_instances()
```

server_list ends up being a python list of every instance in your account in the json format provided by RightScale.


Rightscale API documentation is available at http://support.rightscale.com/12-Guides/RightScale_API_1.5
