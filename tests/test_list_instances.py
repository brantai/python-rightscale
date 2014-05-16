from nose.plugins.attrib import attr

from rightscale import RightScale


@attr('rc_creds', 'real_conn')
def test_list_all_instances_tiny():
    rs = RightScale()
    all_instances = rs.list_instances()
    print "Got %d instances" % len(all_instances)
