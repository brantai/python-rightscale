from nose.plugins.attrib import attr

from rightscale import RightScale


@attr('rc_creds', 'real_conn')
def test_health_check():
    api = RightScale()
    print "API health is %s" % api.health_check()
