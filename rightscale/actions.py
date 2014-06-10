# In theory, RightScale's API is discoverable through ``links`` in responses.
# In practice, we have to help our robots along with the following hints:
RS_DEFAULT_ACTIONS = {
        'index': {
            'http_method': 'get',
            },
        'show': {
            'http_method': 'get',
            'extra_path': '/%(res_id)s',
            },
        'create': {
            'http_method': 'post',
            },
        'update': {
            'http_method': 'put',
            'extra_path': '/%(res_id)s',
            },
        'destroy': {
            'http_method': 'delete',
            'extra_path': '/%(res_id)s',
            },
        }

ALERT_ACTIONS = {
        'disable': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/disable',
            },
        'enable': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/enable',
            },
        'quench': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/quench',
            },
        'create': None,
        'update': None,
        'destroy': None,
        }

COOKBOOK_ATTACHMENT_ACTIONS = {
        'multi_attach': {
            'http_method': 'post',
            'extra_path': '/multi_attach',
            },
        'multi_detach': {
            'http_method': 'post',
            'extra_path': '/multi_detach',
            },
        'update': None,
        }

INPUT_ACTIONS = {
        'multi_update': {
            'http_method': 'put',
            'extra_path': '/multi_update',
            },
        'show': None,
        'create': None,
        'update': None,
        'destroy': None,
        }

INSTANCE_ACTIONS = {
        'launch': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/launch',
            },
        'lock': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/lock',
            },
        'multi_run_executable': {
            'http_method': 'post',
            'extra_path': '/multi_run_executable',
            },
        'multi_terminate': {
            'http_method': 'post',
            'extra_path': '/multi_terminate',
            },
        'reboot': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/reboot',
            },
        'run_executable': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/run_executable',
            },
        'set_custom_lodgement': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/set_custom_lodgement',
            },
        'start': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/start',
            },
        'stop': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/stop',
            },
        'terminate': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/terminate',
            },
        'unlock': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/unlock',
            },
        'create': None,
        'destroy': None,
        }

MULTI_CLOUD_IMAGE_ACTIONS = {
        'clone': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/clone',
            },
        'commit': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/commit',
            },
        }

SERVER_ARRAY_ACTIONS = {
        'clone': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/clone',
            },
        'current_instances': {
            'http_method': 'get',
            'extra_path': '/%(res_id)s/current_instances',
            },
        'launch': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/launch',
            },
        'multi_run_executable': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/multi_run_executable',
            },
        'multi_terminate': {
            'http_method': 'post',
            'extra_path': '/%(res_id)s/multi_terminate',
            },
        }

UPDATE_NONE_ACTIONS = {
        'update': None,
        }

# Specify variations from the default actions defined in RS_DEFAULT_ACTIONS.
# These specs come from http://reference.rightscale.com/api1.5/index.html
ROOT_COLLECTIONS = {

        'account_groups': {
            'create': None,
            'update': None,
            'destroy': None,
            },

        'accounts': {
            'index': None,
            'create': None,
            'update': None,
            'destroy': None,
            },

        # alert_specs use defaults

        'alerts': ALERT_ACTIONS,

        'audit_entries': {
            'append': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/append',
                },
            'detail': {
                'http_method': 'get',
                'extra_path': '/%(res_id)s/detail',
                },
            'destroy': None,
            },

        'backups': {
            'cleanup': {
                'http_method': 'post',
                'extra_path': '/cleanup',
                },
            },

        'child_accounts': {
            'show': None,
            'destroy': None,
            },

        'cloud_accounts': {
            'update': None,
            },

        'clouds': {
            'create': None,
            'update': None,
            'destroy': None,
            },

        # these are only in the 1.5 docs and are not available as hrefs.
        'cookbook_attachments': COOKBOOK_ATTACHMENT_ACTIONS,

        'cookbooks': {
            'follow': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/follow',
                },
            'freeze': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/freeze',
                },
            'obsolete': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/obsolete',
                },
            'create': None,
            'update': None,
            },

        # credentials use defaults

        'deployments': {
            'clone': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/clone',
                },
            'lock': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/lock',
                },
            'servers': {
                'http_method': 'get',
                'extra_path': '/%(res_id)s/servers',
                },
            'unlock': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/unlock',
                },
            },

        'identity_providers': {
            'create': None,
            'update': None,
            'destroy': None,
            },

        'multi_cloud_images': MULTI_CLOUD_IMAGE_ACTIONS,

        # network_gateways use defaults
        # network_option_group_attachments use defaults
        # network_option_groups use defaults
        # networks use defaults

        # oauth2 is a special case just used during auth

        'permissions': {
            'update': None,
            },

        # only in 1.5 api docs, not discoverable via href
        'placement_groups': {
            'update': None,
            },

        'preferences': {
            'create': None,
            },

        'publication_lineages': {
            'index': None,
            'create': None,
            'update': None,
            'destroy': None,
            },

        'publications': {
            'import': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/import',
                },
            'create': None,
            'update': None,
            'destroy': None,
            },

        'repositories': {
            'cookbook_import': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/cookbook_import',
                },
            'refetch': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/refetch',
                },
            'resolve': {
                'http_method': 'post',
                'extra_path': '/resolve',
                },
            },

        'right_scripts': {
            'create': None,
            'update': None,
            'destroy': None,
            },

        # route_tables uses defaults
        # routes uses defaults
        # security_group_rules uses defaults

        # rs api 1.5 returns a link where rel=self for the ``/api/sessions``
        # resource.  sadly, the href=/api/session.  regardless, we don't need
        # it as an attribute because it's where we started off.
        'self': None,

        'server_arrays': SERVER_ARRAY_ACTIONS,

        'server_template_multi_cloud_images': {
            'make_default': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/make_default',
                },
            'update': None,
            },

        'server_templates': {
            'clone': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/clone',
                },
            'commit': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/commit',
                },
            'detect_changes_in_head': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/detect_changes_in_head',
                },
            'publish': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/publish',
                },
            'resolve': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/resolve',
                },
            'swap_repository': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/swap_repository',
                },
            },

        'servers': {
            'clone': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/clone',
                },
            'launch': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/launch',
                },
            'terminate': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/terminate',
                },
            },

        # workaround inconsistency in rs hateoas
        'sessions': {
            'accounts': {
                'http_method': 'get',
                'extra_path': '/accounts',
                },
            'index': None,
            'show': None,
            'create': None,
            'update': None,
            'destroy': None,
            },

        'tags': {
            'by_resource': {
                'http_method': 'post',
                'extra_path': '/by_resource',
                },
            'by_tag': {
                'http_method': 'post',
                'extra_path': '/by_tag',
                },
            'multi_add': {
                'http_method': 'post',
                'extra_path': '/multi_add',
                },
            'multi_delete': {
                'http_method': 'post',
                'extra_path': '/multi_delete',
                },
            'index': None,
            'show': None,
            'create': None,
            'update': None,
            'destroy': None,
            },

        'users': {
            'destroy': None,
            },

        }

CLOUD_COLLECTIONS = {

        'datacenters': {
            'create': None,
            'update': None,
            'destroy': None,
            },

        'images': {
            'create': None,
            'update': None,
            'destroy': None,
            },

        'instance_types': {
            'create': None,
            'update': None,
            'destroy': None,
            },

        'instances': INSTANCE_ACTIONS,

        'ip_address_bindings': UPDATE_NONE_ACTIONS,

        # ip_addresses uses defaults

        'recurring_volume_attachments': UPDATE_NONE_ACTIONS,

        'security_groups': {
            'update': None,
            },

        'ssh_keys': {
            'update': None,
            },

        # subnets uses defaults

        'volume_attachments': UPDATE_NONE_ACTIONS,

        'volume_snapshots': UPDATE_NONE_ACTIONS,

        }

INSTANCE_COLLECTIONS = {

        'alerts': ALERT_ACTIONS,
        'inputs': INPUT_ACTIONS,

        # instance_custom_lodgements uses defaults

        'monitoring_metrics': {
            'data': {
                'http_method': 'get',
                'extra_path': '/%(res_id)s/data',
                },
            'create': None,
            'update': None,
            'destroy': None,
            },

        # subnets uses defaults

        # TODO: investigate to see how useful tasks is by itself.  i.e. there's
        # no way to index() all tasks for an instance.  regardless, this
        # definition is here at least for completeness.
        'tasks': {
            'show': {
                'http_method': 'get',
                'extra_path': '/live/tasks/%(res_id)s',
                },
            'index': None,
            'create': None,
            'update': None,
            'destroy': None,
            },

        'volume_attachments': UPDATE_NONE_ACTIONS,

        'volumes': {
            'update': None,
            },

        'volume_types': {
            'create': None,
            'update': None,
            'destroy': None,
            },

        }

COOKBOOK_COLLECTIONS = {
        'cookbook_attachments': COOKBOOK_ATTACHMENT_ACTIONS,
        }

DEPLOYMENT_COLLECTIONS = {
        'alerts': ALERT_ACTIONS,
        'inputs': INPUT_ACTIONS,
        'server_arrays': SERVER_ARRAY_ACTIONS,
        }

IP_ADDRESS_COLLECTIONS = {
        'ip_address_bindings': UPDATE_NONE_ACTIONS,
        }

REPOSITORY_COLLECTIONS = {
        'repository_assets': {
            'create': None,
            'update': None,
            'destroy': None,
            },
        }

SERVER_COLLECTIONS = {
        # alert_specs use defaults
        'alerts': ALERT_ACTIONS,
        }

SERVER_ARRAY_COLLECTIONS = {
        # alert_specs use defaults
        'alerts': ALERT_ACTIONS,
        'current_instances': INSTANCE_ACTIONS,
        }

SERVER_TEMPLATES_COLLECTIONS = {

        'cookbook_attachments': COOKBOOK_ATTACHMENT_ACTIONS,
        'inputs': INPUT_ACTIONS,
        'multi_cloud_images': MULTI_CLOUD_IMAGE_ACTIONS,

        'runnable_bindings': {
            'multi_update': {
                'http_method': 'put',
                'extra_path': '/multi_update',
                },
            'update': None,
            },

        }

VOLUME_COLLECTIONS = {
        'recurring_volume_attachments': UPDATE_NONE_ACTIONS,
        'volume_snapshots': UPDATE_NONE_ACTIONS,
        }

VOLUME_SNAPSHOT_COLLECTIONS = {
        'recurring_volume_attachments': UPDATE_NONE_ACTIONS,
        }

COLLECTIONS = {
        'application/vnd.rightscale.session+json': ROOT_COLLECTIONS,
        'application/vnd.rightscale.cookbook+json': COOKBOOK_COLLECTIONS,
        'application/vnd.rightscale.cloud+json': CLOUD_COLLECTIONS,
        'application/vnd.rightscale.instance+json': INSTANCE_COLLECTIONS,
        'application/vnd.rightscale.ip_address+json': IP_ADDRESS_COLLECTIONS,
        'application/vnd.rightscale.deployment+json': DEPLOYMENT_COLLECTIONS,

        # multi_cloud_image has a ``settings`` collection (a.k.a.
        # MultiCloudImageSettings in the RS docs) that just uses defaults, so
        # no need for an extra map

        'application/vnd.rightscale.repository+json': REPOSITORY_COLLECTIONS,
        'application/vnd.rightscale.server+json': SERVER_COLLECTIONS,
        'application/vnd.rightscale.server_array+json': SERVER_ARRAY_COLLECTIONS,
        'application/vnd.rightscale.server_template+json': SERVER_TEMPLATES_COLLECTIONS,

        # security_group has a ``security_group_rules`` collection that just
        # uses defaults, so no need for an extra map

        'application/vnd.rightscale.volume+json': VOLUME_COLLECTIONS,
        'application/vnd.rightscale.volume_snapshot+json': VOLUME_SNAPSHOT_COLLECTIONS,
        }
