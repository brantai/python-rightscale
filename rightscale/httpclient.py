from functools import partial
import requests


DEFAULT_ROOT_RES_PATH = '/'


class RESTOAuthClient(object):

    """
    HTTP client that is aware of REST and OAuth semantics.

    Provides CRUD methods for API resources using HTTP verbs.  It also
    interrogates the API server for links to related resources and exposes
    discovered resources as attributes on this root object.

    For additional flexibility, helper methods like :meth:`get`, :meth:`post`,
    and the generic :meth:`request` allow the caller to call any routes that
    are not automatically exposed as attributes of this object.

    :param str endpoint: URL for the API endpoint. E.g. ``https://blah.org``.

    :param str root_path: The initial path to use for discovering the rest of
        the resources.  E.g. ``/api/``.

    :param dict hints: Hints for URL paths that should be added or removed from
        the set of discovered paths.  This allows users to work around
        inconsistencies in a vendor's REST implementation, or just ignore large
        swaths of discovered routes that they don't need.

    """

    def __init__(
            self,
            endpoint='',
            root_path=DEFAULT_ROOT_RES_PATH,
            hints=None,
            ):
        self.endpoint = endpoint
        self.root_path = root_path
        self.hints = hints
        self.headers = {'Accept': 'application/json'}

        # convenience methods
        self.delete = partial(self.request, 'delete')
        self.get = partial(self.request, 'get')
        self.head = partial(self.request, 'head')
        self.post = partial(self.request, 'post')
        self.put = partial(self.request, 'put')

        self.reset_cache()

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

        # merge with defaults in headers attribute.  incoming 'headers' take
        # priority over values in self.headers to allow last-minute overrides
        # if the caller really knows what they're doing.
        if 'headers' in kwargs:
            headers = kwargs.pop('headers')
            for k, v in self.headers.items():
                headers.setdefaults(k, v)
        else:
            headers = self.headers
        kwargs['headers'] = headers

        r = requests.request(method, _url, **kwargs)
        if not r.ok and r.status_code not in ignore_codes:
            r.raise_for_status()
        return r

    def reset_cache(self):
        self._links = None
        self._root_response = None

    @property
    def root_response(self):
        if self._root_response is None:
            try:
                self._root_response = self.get(self.root_path).json()
            except:
                return {}
        return self._root_response

    @property
    def _unfiltered_links(self):
        if self._links is None:
            response = self.get(self.root_path)
            if not response.ok:
                return {}
            blob = response.json()
            self._links = dict(
                (raw['rel'], raw['href']) for raw in blob.get('links', [])
                )
        return self._links

    @property
    def links(self):
        hinted_links = self._unfiltered_links.copy()
        if self.hints:
            for r in self.hints.get('remove', []):
                hinted_links.pop(r, None)
            hinted_links.update(self.hints.get('add', {}))
        return hinted_links

    def __getattr__(self, name):
        if name not in self.links:
            raise AttributeError('%s object has no attribute %s' % (
                self.__class__.__name__,
                name,
                ))
        path = self.links[name]
        response = self.get(path)
        # TODO: construct appropriate objects based on content-type
        return response.json()
