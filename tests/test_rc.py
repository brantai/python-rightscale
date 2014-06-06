from mock import patch
from rightscale import util


def test_read_rc():
    """
    get_rc_creds() should return (endpoint, token).
    """
    exp_endpoint = 'the endpoint yo'
    exp_token = 'the ref token'

    def fake_config_parser_get(_, key):
        return {
                util.CFG_OPTION_ENDPOINT: exp_endpoint,
                util.CFG_OPTION_REF_TOKEN: exp_token,
                }.get(key)

    with patch('rightscale.util.get_config') as _get_config:
        _get_config.return_value.get.side_effect = fake_config_parser_get
        assert (exp_endpoint, exp_token) == util.get_rc_creds()


def test_failed_rc():
    """
    get_rc_creds() should return empty strings on errors.
    """
    with patch('rightscale.util.get_config') as _get_config:
        _get_config.return_value.get.side_effect = ['first', ValueError]
        assert ('', '') == util.get_rc_creds()

        _get_config.return_value.get.side_effect = [NameError, 'last']
        assert ('', '') == util.get_rc_creds()

        _get_config.return_value = ValueError
        assert ('', '') == util.get_rc_creds()
