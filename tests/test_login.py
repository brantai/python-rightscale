from nose.tools import raises
from nose.plugins.attrib import attr
from requests import HTTPError

from rightscale import RightScale


@raises(ValueError)
def test_empty_api_endpoint():
    rs = RightScale(refresh_token='not empty', api_endpoint='')
    rs.login()


@raises(ValueError)
def test_empty_refresh_token():
    rs = RightScale(refresh_token='', api_endpoint='not empty')
    rs.login()


@attr('real_conn')
@raises(HTTPError)
def test_bogus_refresh_token():
    rs = RightScale(refresh_token='bogus')
    rs.login()
