from nose.tools import raises
from nose.plugins.attrib import attr
from requests import HTTPError

from rightscale import RightScale


@raises(ValueError)
def test_empty_refresh_token():
    rs = RightScale(refresh_token='')
    rs.login()


@attr('real_conn')
@raises(HTTPError)
def test_bogus_refresh_token():
    rs = RightScale(refresh_token='bogus')
    rs.login()
