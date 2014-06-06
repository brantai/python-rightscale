from nose.plugins.attrib import attr

from rightscale.rightscale import RightScale, Resource


@attr('rc_creds', 'real_conn')
def test_show_first_cloud():
    api = RightScale()
    res = api.clouds.show(res_id=1)
    assert isinstance(res, Resource)
