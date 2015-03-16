import os.path
import ConfigParser

CFG_USER_RC = '.rightscalerc'
CFG_SECTION_OAUTH = 'OAuth'
CFG_OPTION_ENDPOINT = 'api_endpoint'
CFG_OPTION_REF_TOKEN = 'refresh_token'

_config = None


class HookList(list):
    def __init__(self, *args, **kwargs):
        super(HookList, self).__init__(*args)
        for k, v in kwargs.items():
            setattr(self, k, v)


class HookDict(dict):
    pass


def get_config():
    global _config
    if not _config:
        _config = ConfigParser.SafeConfigParser()

        # set up some defaults - too bad only newer pythons know how to do this
        # more gracefully:
        _config.add_section(CFG_SECTION_OAUTH)
        _config.set(CFG_SECTION_OAUTH, CFG_OPTION_ENDPOINT, '')
        _config.set(CFG_SECTION_OAUTH, CFG_OPTION_REF_TOKEN, '')

        home = os.path.expanduser('~')
        rc_file = os.path.join(home, CFG_USER_RC)
        _config.read(rc_file)
    return _config


def get_rc_creds():
    """
    Reads ~/.rightscalerc and returns API endpoint and refresh token.

    Always returns a tuple of strings even if the file is empty - in which
    case, returns ``('', '')``.
    """
    config = get_config()
    try:
        return (
                config.get(CFG_SECTION_OAUTH, CFG_OPTION_ENDPOINT),
                config.get(CFG_SECTION_OAUTH, CFG_OPTION_REF_TOKEN),
                )
    except:
        return ('', '')


def find_by_name(collection, name, exact=True):
    """
    Searches collection by resource name.

    :param rightscale.ResourceCollection collection: The collection in which to
        look for :attr:`name`.

    :param str name: The name to look for in collection.

    :param bool exact: A RightScale ``index`` search with a :attr:`name` filter
        can return multiple results because it does a substring match on
        resource names.  So any resource that contains the specified name will
        be returned.  The :attr:`exact` flag controls whether to attempt to
        find an exact match for the given name.  If :attr:`exact` is ``False``,
        this will return a list of all the matches.  The default behaviour is
        to perform an exact match and return a single result.

    Returns ``None`` if no resources are found with a matching name.

    """
    params = {'filter[]': ['name==%s' % name]}
    found = collection.index(params=params)
    if not exact and len(found) > 0:
        return found
    for f in found:
        if f.soul['name'] == name:
            return f
