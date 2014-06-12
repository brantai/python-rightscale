import user_fixtures as UF

from pprint import pprint
from nose.plugins.attrib import attr

from rightscale.commands import get_by_path


@UF.requires(UF.TARGET_DEPLOYMENT, UF.TARGET_SERVER)
@attr('rc_creds', 'real_conn')
def test_get_by_path():
    res = get_by_path(
            'deployments:%s:servers:%s:current_instance'
            % (UF.TARGET_DEPLOYMENT, UF.TARGET_SERVER)
            )
    pprint(res)
