python-rightscale
=================

A python wrapper for the Rightscale API.  This supports the 1.5 API and Rightscale's OAuth token authentication.


Usage Examples
--------------

**Setting up your auth token**

```python
import rightscale
api = rightscale.RightScale(refresh_token='token',api_endpoint='api-endpoint')
```

- `refreshtoken` is the refresh token issued to you when you enabled api access.
- `api_endpoint` is the FQDN of "Token Endpoint (API 1.5)" from the same page.

You may pre-store these attributes in `~/.rightscalerc`.  See the example file for format.  When using `~/.rightscalerc`, you can instantiate `RightScale` objects without specifying credentials and it will use the credentials in your rc file:

```python
import rightscale
api = rightscale.RightScale()
```

**Getting a list of all servers**

```python
server_list = api.list_instances()
```

server_list ends up being a python list of every instance in your account in the json format provided by RightScale.

**Running a RightScript on a server instance**

```python
inputs = {
    'APACHE_VHOST': 'my-photo-gallery',
    }
api.run_script('my web server', 'enable apache vhost', inputs=inputs)
```


Object Interface to RightScale API
----------------------------------
This library's object interface was modeled after the REST-ish API as documented in [the official RightScale API guide](http://support.rightscale.com/12-Guides/RightScale_API_1.5).

Users of this library should consult the [API reference](http://reference.rightscale.com/api1.5/index.html) for context-specific parameters like filters, views, GET and POST parameters.

**Resources and Actions**

The `rightscale.RightScale` class has attributes for the top-level resources documented in the API reference.  The methods on each of the `RightScale` attributes map to the actions listed in the documentation.  Invoking an action method is like issuing an HTTP request.  In fact, action methods return HTTP `Response` objects from the [Requests library](http://python-requests.org).  For example, the [Users resource](http://reference.rightscale.com/api1.5/resources/ResourceAccounts.html) has an `index` action that lists all the users available to the account.  The HTTP request for this list would be:

    GET /api/users

To retrieve the list using this library:

```python
response = api.users.index()
users = response.json()
```

Most actions that act on a specific resource (as opposed to a set of resources) require a resource `id` value.  For example, to get account details, the API documentation describes the [Accounts resource](http://reference.rightscale.com/api1.5/resources/ResourceAccounts.html) as having a `show` action that requires an `id` as the last part of the URL path.  If the account `id` were `12345`, the associated HTTP request would be:

    GET /api/accounts/12345

To specify a resource identifier to action methods, assign a value to the `res_id` keyword argument like this:

```python
account = api.accounts.show(res_id='12345').json()
```

Regardless of what the actual name of the resource is (e.g. `accounts`, `users`, `servers`, etc...), the special keyword argument is always called `res_id`.

**Filters**
The action methods are just wrappers around HTTP `Request` objects from the [Requests library](http://python-requests.org).  That means that the methods accept GET parameters and POST data as keyword arguments.  For example, to find a server by name, the API reference instructs us to use the `index` method on the Servers resource with a filter.  If the name of the server were `server_foo`, the HTTP request would be:

    GET /api/servers?filter[]=name==server_foo

And RightScale would return a list of matches.  Using this library, to conduct the same search would look like this:

```python
params = {
    'filter[]': ['name==server_foo'],
    }
found = api.servers.index(params=params).json()
```
