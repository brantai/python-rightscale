import os.path
import ConfigParser

CFG_USER_RC = '.rightscalerc'
CFG_SECTION_OAUTH = 'OAuth'
CFG_OPTION_ENDPOINT = 'api_endpoint'
CFG_OPTION_REF_TOKEN = 'refresh_token'


def get_rc_creds():
    """
    Reads ~/.rightscalerc and returns API endpoint and refresh token.

    Always returns a tuple of strings even if the file is empty - in which
    case, returns ``('', '')``.
    """
    config = ConfigParser.SafeConfigParser()

    # set up some defaults - too bad only newer pythons know how to do this
    # more gracefully:
    config.add_section(CFG_SECTION_OAUTH)
    config.set(CFG_SECTION_OAUTH, CFG_OPTION_ENDPOINT, '')
    config.set(CFG_SECTION_OAUTH, CFG_OPTION_REF_TOKEN, '')

    home = os.path.expanduser('~')
    rc_file = os.path.join(home, CFG_USER_RC)
    try:
        config.read(rc_file)
        return (
                config.get(CFG_SECTION_OAUTH, CFG_OPTION_ENDPOINT),
                config.get(CFG_SECTION_OAUTH, CFG_OPTION_REF_TOKEN),
                )
    except:
        return ('', '')
