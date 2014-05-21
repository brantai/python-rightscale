from nose.plugins.attrib import attr
from mock import MagicMock

from rightscale import RightScale
from rightscale.rightscale import RightScaleLinkyThing
from rightscale.httpclient import RESTOAuthClient


def test_empty_linky_thing():
    linky = RightScaleLinkyThing()
    assert {} == linky.links


def test_loaded_linky_thing():
    exp = {
            'a': '/path/to/a',
            'mojo': '/somefingelse/blah/blah',
            'thang': '/thang.thang',
            }
    data = []
    for k, v in exp.items():
        data.append({'rel': k, 'href': v})
    linky = RightScaleLinkyThing({'links': data})
    assert exp == linky.links


@attr('real_conn')
def test_root_links():
    rs = RightScale()
    links = rs.client.links
    # check for some bare minimum resources
    for res in ['clouds', 'servers', 'networks']:
        assert res in links


GOODATTRS = ['asdf', 'qwerty', 'poiuy']
BADATTRS = ['hiss', 'boo']


class TestUnfilteredLinks:
    def setup(self):
        client = RESTOAuthClient()
        client.get = MagicMock()
        self.client = client

    def test_http_failure_returns_no_links(self):
        mock_response = self.client.get.return_value
        mock_response.ok = False
        assert {} == self.client._unfiltered_links

    def test_return_memoized(self):
        mlinks = {'foo': '/api/foo', 'bar': '/bazbazbaz'}
        self.client._links = mlinks
        assert self.client._unfiltered_links == mlinks
        id_first = id(self.client._unfiltered_links)
        id_next = id(self.client._unfiltered_links)
        assert id_first == id_next

    def test_reset_return_new(self):
        self.client._links = {'foo': '/api/foo', 'bar': '/bazbazbaz'}
        id_first = id(self.client._unfiltered_links)
        self.client.reset_cache()
        id_next = id(self.client._unfiltered_links)
        assert id_first != id_next


class TestResAttrs:
    def setup(self):
        client = RESTOAuthClient()
        client._links = dict((g, '/api/' + g) for g in GOODATTRS)
        client.get = MagicMock()
        self.client = client

    def test_good_attrs(self):
        c = self.client
        for g in GOODATTRS:
            assert hasattr(c, g)
            c.get.assert_called_with('/api/' + g)

    def test_bad_attrs(self):
        for b in BADATTRS:
            assert not hasattr(self.client, b)


class TestHints:
    def setup(self):
        client = RESTOAuthClient()
        client._links = dict((g, '/api/' + g) for g in GOODATTRS)
        self.client = client

    def test_add_hints(self):
        new_routes = {'new1': '/new/1', 'new2': '/new/2'}
        self.client.hints = {'add': new_routes}
        exp = dict((g, '/api/' + g) for g in GOODATTRS)
        exp.update(new_routes)
        assert exp == self.client.links

    def test_remove_hints(self):
        self.client.hints = {'remove': [GOODATTRS[0]]}
        exp = dict((g, '/api/' + g) for g in GOODATTRS[1:])
        assert exp == self.client.links
