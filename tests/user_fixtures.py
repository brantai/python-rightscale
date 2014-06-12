from nose.tools import nottest

from rightscale.util import get_config


__all__ = [
    'requires',
    'SCRIPT',
    'TARGET_SERVER',
    'TARGET_DEPLOYMENT',
    'INPUTS',
    ]


SCRIPT = None
TARGET_SERVER = None
TARGET_DEPLOYMENT = None
INPUTS = None


def requires(*args):
    """
    Decorator to make test optional based on required user fixtures.

    If any of the values in :attr:`*args` are ``None``, then the wrapped test
    is considered not-runnable.
    """
    def wrap(fn):
        if None in args:
            return nottest(fn)
        return fn
    return wrap


CFG_SECTION_TESTING = 'Testing'
CFG_OPTION_SAFE_SCRIPT_NAME = 'safe_script_name'
CFG_OPTION_SAFE_TGT_DPL_NAME = 'safe_target_deployment_name'
CFG_OPTION_SAFE_TGT_SRV_NAME = 'safe_target_server_name'
CFG_OPTION_INPUTS = 'inputs'


def _parse_inputs(raw):
    global INPUTS
    INPUTS = {}
    for kvs in raw.split(','):
        k, v = kvs.split(':')
        INPUTS[k] = v


def _get_user_fixtures_from_rc():
    global SCRIPT
    global TARGET_SERVER
    global TARGET_DEPLOYMENT

    config = get_config()
    if CFG_SECTION_TESTING not in config.sections():
        return

    avail_opts = config.options(CFG_SECTION_TESTING)
    if not (CFG_OPTION_SAFE_SCRIPT_NAME in avail_opts
            and CFG_OPTION_SAFE_TGT_SRV_NAME in avail_opts):
        return

    SCRIPT = config.get(CFG_SECTION_TESTING, CFG_OPTION_SAFE_SCRIPT_NAME)
    TARGET_SERVER = config.get(
            CFG_SECTION_TESTING,
            CFG_OPTION_SAFE_TGT_SRV_NAME,
            )
    TARGET_DEPLOYMENT = config.get(
            CFG_SECTION_TESTING,
            CFG_OPTION_SAFE_TGT_DPL_NAME,
            )

    if CFG_OPTION_INPUTS in avail_opts:
        _parse_inputs(config.get(CFG_SECTION_TESTING, CFG_OPTION_INPUTS))


_get_user_fixtures_from_rc()
