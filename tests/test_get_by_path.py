from pprint import pprint
from nose.plugins.attrib import attr

from rightscale.commands import get_by_path


@attr('rc_creds', 'real_conn')
def test_get_by_path():
    res = get_by_path('deployments:Operations:servers:NewOps:current_instance')
    pprint(res)
