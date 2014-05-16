from nose.plugins.attrib import attr
from mock import MagicMock

from rightscale import RightScale
from rightscale.httpclient import RESTOAuthClient


@attr('real_conn')
def test_root_links():
    rs = RightScale()
    links = rs.client.links
    # check for some bare minimum resources
    for res in ['clouds', 'servers', 'networks']:
        assert res in links


GOODATTRS = ['asdf', 'qwerty', 'poiuy']
BADATTRS = ['hiss', 'boo']


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
