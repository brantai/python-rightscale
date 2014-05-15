import os.path
import ConfigParser
from nose.plugins.attrib import attr

from rightscale import RightScale


def read_rc():
    home = os.path.expanduser('~')
    rc_file = os.path.join(home, '.rightscalerc')
    config = ConfigParser.SafeConfigParser()
    config.read(rc_file)
    account_id = config.get('OAuth', 'account_id')
    refresh_token = config.get('OAuth', 'refresh_token')
    return (account_id, refresh_token)


@attr('real_creds')
def test_list_all_instances_tiny():
    account_id, refresh_token = read_rc()
    rs = RightScale(account_id, refresh_token)
    all_instances = rs.list_instances()
    print "Got %d instances" % len(all_instances)
