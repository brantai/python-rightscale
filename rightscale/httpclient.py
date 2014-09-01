from functools import partial
import requests



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

    def request(self, method, path='/', url=None, ignore_codes=[], **kwargs):
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
