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

        'alerts': {
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
            },

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
        'cookbook_attachments': {
            'multi_attach': {
                'http_method': 'post',
                'extra_path': '/multi_attach',
                },
            'multi_detach': {
                'http_method': 'post',
                'extra_path': '/multi_detach',
                },
            'update': None,
            },

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

        'multi_cloud_images': {
            'clone': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/clone',
                },
            'commit': {
                'http_method': 'post',
                'extra_path': '/%(res_id)s/commit',
                },
            },

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

        # rs api 1.5 returns a link where rel=self for the ``/api/sessions``
        # resource.  sadly, the href=/api/session.  regardless, we don't need
        # it as an attribute because it's where we started off.
        'self': None,

        'server_arrays': {
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
            },

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

COLLECTIONS = {
        'application/vnd.rightscale.session+json': ROOT_COLLECTIONS,
        }
