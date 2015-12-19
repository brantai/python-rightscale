from functools import partial
import logging
import time
import requests


log = logging.getLogger(__name__)
DEFAULT_ROOT_RES_PATH = '/'


class HTTPResponse(object):
    """
    Wrapper around :class:`requests.Response`.

    Parses ``Content-Type`` header and makes it available as a list of fields
    in the :attr:`content_type` member.
    """
    def __init__(self, raw_response):
        self.raw_response = raw_response

        content_type = raw_response.headers.get('content-type', '')
        ct_fields = [f.strip() for f in content_type.split(';')]
        self.content_type = ct_fields

    def __getattr__(self, name):
        return getattr(self.raw_response, name)


class HTTPClient(object):

    """
    Convenience wrapper around Requests.

    :param str endpoint: URL for the API endpoint. E.g. ``https://blah.org``.

    :param dict extra_headers: When specified, these key-value pairs are added
        to the default HTTP headers passed in with each request.

    """

    def __init__(
            self,
            endpoint='',
            extra_headers=None,
            oauth_path=None,
            refresh_token=None,
            ):
        self.endpoint = endpoint

        s = requests.session()

        # Disable keepalives. They're unsafe in threaded apps that potentially
        # re-use very old connection objects from the urllib3 connection pool.
        s.headers['Accept'] = 'application/json'
        s.headers['Connection'] = 'close'
        if extra_headers:
            s.headers.update(extra_headers)
        self.s = s

        # convenience methods
        self.delete = partial(self.request, 'delete')
        self.get = partial(self.request, 'get')
        self.head = partial(self.request, 'head')
        self.post = partial(self.request, 'post')
        self.put = partial(self.request, 'put')

        # keep track of when our auth token expires
        self.oauth_path = oauth_path
        self.refresh_token = refresh_token
        self.auth_expires_at = None

    def login(self):
        """
        Gets and stores an OAUTH token from Rightscale.
        """
        log.debug('Logging into RightScale...')
        login_data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            }
        response = self._request('post', self.oauth_path, data=login_data)

        raw_token = response.json()
        auth_token = "Bearer %s" % raw_token['access_token']
        self.s.headers['Authorization'] = auth_token

        # Generate an expiration time for our token of 60-seconds before the
        # standard time returned by RightScale. This will be used in the
        # self.client property to validate that our token is still usable on
        # every API call.
        log.debug('Auth Token expires in %s(s)' % raw_token['expires_in'])
        self.auth_expires_at = time.time() + int(raw_token['expires_in']) - 60

    def request(self, method, path='/', url=None, ignore_codes=[], **kwargs):
        """
        Wrapper for the ._request method that verifies if we're logged into
        RightScale before making a call, and sanity checks the oauth expiration
        time.

        :param str method: An HTTP method (e.g. 'get', 'post', 'PUT', etc...)

        :param str path: A path component of the target URL.  This will be
            appended to the value of ``self.endpoint``.  If both :attr:`path`
            and :attr:`url` are specified, the value in :attr:`url` is used and
            the :attr:`path` is ignored.

        :param str url: The target URL (e.g.  ``http://server.tld/somepath/``).
            If both :attr:`path` and :attr:`url` are specified, the value in
            :attr:`url` is used and the :attr:`path` is ignored.

        :param ignore_codes: List of HTTP error codes (e.g.  404, 500) that
            should be ignored.  If an HTTP error occurs and it is *not* in
            :attr:`ignore_codes`, then an exception is raised.
        :type ignore_codes: list of int

        :param kwargs: Any other kwargs to pass to :meth:`requests.request()`.

        Returns a :class:`requests.Response` object.
        """
        # On every call, check if we're both logged in, and if the token is
        # expiring. If it is, we'll re-login with the information passed into
        # us at instantiation.
        if time.time() > self.auth_expires_at:
            self.login()

        # Now make the actual API call
        return self._request(method, path, url, ignore_codes, **kwargs)

    def _request(self, method, path='/', url=None, ignore_codes=[], **kwargs):
        """
        Performs HTTP request.

        :param str method: An HTTP method (e.g. 'get', 'post', 'PUT', etc...)

        :param str path: A path component of the target URL.  This will be
            appended to the value of ``self.endpoint``.  If both :attr:`path`
            and :attr:`url` are specified, the value in :attr:`url` is used and
            the :attr:`path` is ignored.

        :param str url: The target URL (e.g.  ``http://server.tld/somepath/``).
            If both :attr:`path` and :attr:`url` are specified, the value in
            :attr:`url` is used and the :attr:`path` is ignored.

        :param ignore_codes: List of HTTP error codes (e.g.  404, 500) that
            should be ignored.  If an HTTP error occurs and it is *not* in
            :attr:`ignore_codes`, then an exception is raised.
        :type ignore_codes: list of int

        :param kwargs: Any other kwargs to pass to :meth:`requests.request()`.

        Returns a :class:`requests.Response` object.
        """
        _url = url if url else (self.endpoint + path)
        r = self.s.request(method, _url, **kwargs)
        if not r.ok and r.status_code not in ignore_codes:
            r.raise_for_status()
        return HTTPResponse(r)
