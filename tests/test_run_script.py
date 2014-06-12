"""
Tests for successful execution of RightScript.

Note that this is just from the viewpoint of the RightScale API.  You still
have to provide a RightScript that works.

To make these tests run, add a section like the following to your
~/.rightscalerc::

    [Testing]
    safe_script_name = Name of some RightScript
    safe_target_server_name = Ops Test Target
    safe_target_deployment_name = Operations
    inputs = Key1:value one,key 2:value2

Where ``inputs`` is a comma-separated list of key-value pairs, each of which is
the key string, a colon, and the value string.  The ``inputs`` example above
would be parsed to the following Python object::

    {
        'Key1': 'value one',
        'key 2': 'value2',
    }

"""
import user_fixtures as UF

from StringIO import StringIO
from nose.plugins.attrib import attr

from rightscale import run_script_on_server


@UF.requires(UF.SCRIPT, UF.TARGET_SERVER, UF.INPUTS)
@attr('rc_creds', 'real_conn')
def test_run_script_on_server():
    run_script_on_server(
            UF.SCRIPT,
            UF.TARGET_SERVER,
            inputs=UF.INPUTS,
            timeout_s=25,
            )


@UF.requires(UF.SCRIPT, UF.TARGET_SERVER, UF.INPUTS)
@attr('rc_creds', 'real_conn')
def test_run_script_timeout():
    out = StringIO()
    run_script_on_server(
        UF.SCRIPT,
        UF.TARGET_SERVER,
        inputs=UF.INPUTS,
        timeout_s=0,
        output=out,
        )
    output = out.getvalue().strip()
    assert '/api/' in output
