from nose.plugins.attrib import attr

from rightscale import RightScale


@attr('real_conn')
def test_root_links():
    rs = RightScale()
    links = rs.client.links
    # check for some bare minimum resources
    for res in ['clouds', 'servers', 'networks']:
        assert res in links
