from .permissions import CustomPermissions


class MyProjectPermissions(CustomPermissions):
    actions_scopes = {
        'list': 'pass',
        'retrieve': "pass",
        'update': 'pass',
        'destroy': 'projects_d',
        'users': 'pass',
        'add_users': 'pass',
        'teams': 'pass',
        'add_teams': 'pass',
        'excluded_users': "pass",
        'excluded_teams': "pass",
        'delete_users': 'pass',
        'delete_teams': 'pass',
        'add_attachments': 'pass',
        'delete_attachments': 'pass'
    }
