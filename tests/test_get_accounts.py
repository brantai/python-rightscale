from nose.plugins.attrib import attr

from rightscale.commands import get_accounts


@attr('rc_creds', 'real_conn')
def test_get_accounts():
    accounts = get_accounts()
    print "Got %d accounts" % len(accounts)
