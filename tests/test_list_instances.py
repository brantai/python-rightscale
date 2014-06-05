from nose.plugins.attrib import attr

from rightscale import list_instances


@attr('rc_creds', 'real_conn')
def test_list_all_instances_tiny():
    all_instances = list_instances()
    print "Got %d instances" % len(all_instances)


@attr('rc_creds', 'real_conn')
def test_list_some_instances_tiny():
    some_instances = list_instances(deployment_name='production')
    print "Got %d instances" % len(some_instances)
