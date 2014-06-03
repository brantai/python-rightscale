import time
from .rightscale import RightScale as _RS
from .util import find_by_name


__all__ = [
    'get_api',
    'get_accounts',
    'list_instances',
    'run_script_on_server',
    ]


_api = None


def get_api():
    global _api
    if not _api:
        _api = _RS()
    return _api


def get_accounts():
    """
    Returns the RightScale accounts for the given login creds.
    """
    api = get_api()
    return api.sessions.accounts()


def list_instances(deployment_name='', cloud_name='EC2 us-east-1', view='tiny'):
    """
    Returns a list of instances from your account.

    :param str deployment_name: If provided, only lists servers in the
        specified deployment.

    :param str cloud_name: The friendly name for a RightScale-supported cloud.
        E.g. ``EC2 us-east-1``, ``us-west-2``, etc...

    :param str view: The level of detail to request of RightScale.  Valid
        values are ``default``, ``extended``, ``full``, ``full_inputs_2_0``,
        ``tiny``.  Defaults to ``tiny``.

    """
    api = get_api()
    cloud = find_by_name(api.clouds, cloud_name)
    filters = ['state==operational']
    if deployment_name:
        deploy = find_by_name(api.deployments, deployment_name)
        filters.append('deployment_href==' + deploy.href)
    params = {'filter[]': filters, 'view': view}
    api_request = cloud.href + '/instances'
    response = get_api().client.get(api_request, params=params)
    # TODO: return something more meaningful once we know what format it
    # comes back in.
    return response.json()


def run_script_on_server(script_name, server_name, inputs=None, timeout_s=10):
    """
    Runs a RightScript and polls for status.

    Sample usage::

        rs = RightScale()
        rs.run_script_on_server(
                'my cool bob lol script',
                'some server',
                inputs={'BOB': 'blah blah', 'LOL': 'fubar'},
                )

    Sample output::

        status: Querying tags
        status: Querying tags
        status: Preparing execution
        status: RightScript: 'my cool bob lol script'
        status: completed: my cool bob lol script

    """
    api = get_api()
    script = find_by_name(api.right_scripts, script_name)
    server = find_by_name(api.servers, server_name)
    path = server.links['current_instance'] + '/run_executable'

    data = {
            'right_script_href': script.href,
            }
    if inputs:
        for k, v in inputs.items():
            data['inputs[%s]' % k] = 'text:' + v
    response = api.client.post(path, data=data)
    status_path = response.headers['location']
    for i in range(timeout_s):
        status = api.client.get(status_path).json()
        summary = status.get('summary', '')
        print 'status: %s' % summary
        if summary.startswith('completed'):
            return
        time.sleep(1)
    print 'Done waiting. Poll %s for status.' % status_path
