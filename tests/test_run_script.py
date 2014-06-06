"""
Tests for successful execution of RightScript.

Note that this is just from the viewpoint of the RightScale API.  You still
have to provide a RightScript that works.

To make these tests run, add a section like the following to your
~/.rightscalerc::

    [Testing]
    safe_script_name = Name of some RightScript
    safe_target_server_name = Ops Test Target
    inputs = Key1:value one,key 2:value2

Where ``inputs`` is a comma-separated list of key-value pairs, each of which is
the key string, a colon, and the value string.  The ``inputs`` example above
would be parsed to the following Python object::

    {
        'Key1': 'value one',
        'key 2': 'value2',
    }

"""
from StringIO import StringIO
from nose.plugins.attrib import attr

from rightscale.util import get_config
from rightscale import run_script_on_server

CFG_SECTION_TESTING = 'Testing'
CFG_OPTION_SAFE_SCRIPT_NAME = 'safe_script_name'
CFG_OPTION_SAFE_TGT_SRV_NAME = 'safe_target_server_name'
CFG_OPTION_INPUTS = 'inputs'


_SCRIPT = None
_TARGET = None
_INPUTS = None


def parse_inputs(raw):
    global _INPUTS
    _INPUTS = {}
    for kvs in raw.split(','):
        k, v = kvs.split(':')
        _INPUTS[k] = v


def get_user_fixtures_from_rc():
    global _SCRIPT
    global _TARGET

    config = get_config()
    if CFG_SECTION_TESTING not in config.sections():
        return

    avail_opts = config.options(CFG_SECTION_TESTING)
    if not (CFG_OPTION_SAFE_SCRIPT_NAME in avail_opts
            and CFG_OPTION_SAFE_TGT_SRV_NAME in avail_opts):
        return

    _SCRIPT = config.get(CFG_SECTION_TESTING, CFG_OPTION_SAFE_SCRIPT_NAME)
    _TARGET = config.get(CFG_SECTION_TESTING, CFG_OPTION_SAFE_TGT_SRV_NAME)

    if CFG_OPTION_INPUTS in avail_opts:
        parse_inputs(config.get(CFG_SECTION_TESTING, CFG_OPTION_INPUTS))


get_user_fixtures_from_rc()

if _SCRIPT and _TARGET:

    @attr('rc_creds', 'real_conn')
    def test_run_script_on_server():
        global _SCRIPT
        global _TARGET
        global _INPUTS
        run_script_on_server(
                _SCRIPT,
                _TARGET,
                inputs=_INPUTS,
                timeout_s=25,
                )

    @attr('rc_creds', 'real_conn')
    def test_run_script_timeout():
        out = StringIO()
        run_script_on_server(
            _SCRIPT,
            _TARGET,
            inputs=_INPUTS,
            timeout_s=0,
            output=out,
            )
        output = out.getvalue().strip()
        assert '/api/' in output
