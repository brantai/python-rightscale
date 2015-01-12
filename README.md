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

**Convenience Commands**

Here are some examples of some common high-level operations for which functions have been implemented in this library:

- List all instances in `EC2 us-east-1`:

  ```python
  from rightscale import list_instances
  use1_instances = list_instances(cloud_name='EC2 us-east-1')
  ```

  Upon success, `use1_instances` will contain a list of dict objects representing the tiny view of each instance as returned by the RightScale API.

- Run a RightScript on a specific server:

  ```python
  from rightscale import run_script_on_server
  inputs = {
      'APACHE_VHOST': 'my-photo-gallery',
      }
  run_script_on_server('enable apache vhost', 'my web server', inputs=inputs)
  ```


Object Interface to RightScale API
----------------------------------
This library's object interface was modeled after the REST-ish API as documented in [the official RightScale API guide](http://support.rightscale.com/12-Guides/RightScale_API_1.5).

Users of this library should consult the [API reference](http://reference.rightscale.com/api1.5/index.html) for context-specific parameters like filters, views, GET and POST parameters.

**Root API Object**

If you only need to perform a common high-level operation like `run_script_on_server`, then you can just import the necessary function from the top-level package and start calling it.  The convenience commands all expect you to have working credentials in `~/.rightscalerc`.  They also use an implicitly created API object (i.e. singleton instance of `rightscale.RightScale`) and perform all the API calls for you.

However, if you need to specify different credentials than those stored in `~/.rightscalerc`, or if you need full access to the RightScale API, then you should create your own API object by instantiating `rightscale.RightScale`.  E.g.

```python
from rightscale import RightScale
api = RightScale()

# now check rightscale's health!
api.health_check()
```

**Resources and Actions**

The `rightscale.RightScale` class has attributes for the top-level resources documented in the API reference.  The methods on each of the `RightScale` attributes map to the actions listed in the documentation.  Invoking an action method is like issuing an HTTP request.  Action methods return objects that always have a `response` attribute containing the HTTP `Response` objects from the [Requests library](http://python-requests.org).  For example, the [Users resource](http://reference.rightscale.com/api1.5/resources/ResourceAccounts.html) has an `index` action that lists all the users available to the account.  The HTTP request for this list would be:

    GET /api/users

To retrieve the list using this library:

```python
users = api.users.index()

# inspect http response content type
assert 'application/vnd.rightscale.user+json' in users.response.content_type

# inspect other http response headers (note: contrived example; don't really do
# this because the library already checks status for you)
assert '200 OK' == users.response.headers['status']
```

Most actions that act on a specific resource (as opposed to a set of resources) require a resource `id` value.  For example, to get account details, the API documentation describes the [Accounts resource](http://reference.rightscale.com/api1.5/resources/ResourceAccounts.html) as having a `show` action that requires an `id` as the last part of the URL path.  If the account `id` were `12345`, the associated HTTP request would be:

    GET /api/accounts/12345

To specify a resource identifier to action methods, assign a value to the `res_id` keyword argument like this:

```python
account = api.accounts.show(res_id='12345')
```

Regardless of what the actual name of the resource is (e.g. `accounts`, `users`, `servers`, etc...), the special keyword argument is always called `res_id`.

**Filters**

The action methods are just wrappers around HTTP `Request` objects from the [Requests library](http://python-requests.org).  That means that the methods accept GET parameters and POST data as keyword arguments.  For example, to find a server by name, the API reference instructs us to use the `index` method on the [Servers resource](http://reference.rightscale.com/api1.5/resources/ResourceServers.html#index) with a filter.  If the name of the server were `server_foo`, the HTTP request would be:

    GET /api/servers?filter[]=name==server_foo

And RightScale would return a list of matches.  Using this library, to conduct the same search would look like this:

```python
params = {
    'filter[]': ['name==server_foo'],
    }
found = api.servers.index(params=params)
```

**Tags**

Here's an example of how to find resources by tag:

```python
params = {
    'tags[]': ['rs_backup:lineage=prod_db'],
    'resource_type': 'volume_snapshots',
    }
snapshots = api.tags.by_tag(params=params)
```
