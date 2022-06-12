from .permissions import CustomPermissions


class TaskPermissions(CustomPermissions):
    actions_scopes = {
        'list': 'tasks_v',
        'create': 'tasks_c',
        'retrieve': "tasks_v",
        'update': 'tasks_u',
        'partial_update': 'tasks_u',
        'destroy': 'tasks_d',
        'restore': 'tasks_d',
        'trashed': 'tasks_d',
        'all': 'tasks_v'
    }


class ProjectPermissions(CustomPermissions):
    actions_scopes = {
        'list': 'projects_v',
        'create': 'projects_c',
        'retrieve': "projects_v",
        'update': 'projects_u',
        'partial_update': 'projects_u',
        'destroy': 'projects_d',
        'restore': 'projects_d',
        'trashed': 'projects_d',
        'all': 'projects_v',
        'users': 'projects_v',
        'add_users': 'projects_c',
        'teams': 'projects_v',
        'add_teams': 'projects_c',
        'excluded_users': "users_v",
        'excluded_teams': "teams_v",
        'delete_users': 'projects_u',
        'delete_teams': 'projects_u',
        'add_attachments': 'project_attachments_c',
        'delete_attachments': 'project_attachments_d'
    }


class ProjectCommentPermissions(CustomPermissions):
    actions_scopes = {
        'list': 'project_comments_v',
        'create': 'project_comments_c',
        'retrieve': "project_comments_v",
        'update': 'project_comments_u',
        'partial_update': 'project_comments_u',
        'destroy': 'project_comments_d'
    }


class TaskCommentPermissions(CustomPermissions):
    actions_scopes = {
        'list': 'task_comments_v',
        'create': 'task_comments_c',
        'retrieve': "task_comments_v",
        'update': 'task_comments_u',
        'partial_update': 'task_comments_u',
        'destroy': 'task_comments_d'
    }


class UserPermissions(CustomPermissions):
    actions_scopes = {
        'list': 'users_v',
        'create': 'users_c',
        'retrieve': "users_v",
        'update': 'users_u',
        'partial_update': 'users_u',
        'destroy': 'users_d',
        'restore': 'users_d',
        'trashed': 'users_d',
        'all': 'users_v',
        'check_uniqueness': 'users_c'
    }


class TeamPermissions(CustomPermissions):
    actions_scopes = {
        'list': 'teams_v',
        'create': 'teams_c',
        'retrieve': "teams_v",
        'update': 'teams_u',
        'partial_update': 'teams_u',
        'destroy': 'teams_d',
        'restore': 'teams_d',
        'trashed': 'teams_d',
        'all': 'teams_v',
        'users': 'teams_v',
        'add_users': 'teams_c',
        'excluded_users': 'users_v',
        'excluded_projects': 'projects_v',
        'add_project': 'team_projects_c',
        'delete_user': 'teams_d'
    }


class HolidayPermissions(CustomPermissions):
    actions_scopes = {
        'list': 'holidays_v',
        'create': 'holidays_c',
        'retrieve': "holidays_v",
        'update': 'holidays_u',
        'partial_update': 'holidays_u',
        'destroy': 'holidays_d'
    }


class ReminderPermissions(CustomPermissions):
    actions_scopes = {
        'list': 'reminders_v',
        'create': 'reminders_c',
        'retrieve': "reminders_v",
        'update': 'reminders_u',
        'partial_update': 'reminders_u',
        'destroy': 'reminders_d'
    }


class LocationPermissions(CustomPermissions):
    methods_scopes = {
        'POST': 'projects_u',
    }


class PaymentPermissions(CustomPermissions):
    actions_scopes = {
        'list': 'project_payments_v',
        'create': 'project_payments_c',
        'retrieve': "project_payments_v",
        'update': 'project_payments_u',
        'partial_update': 'project_payments_u',
        'destroy': 'project_payments_d'
    }


class FocalPointPermissions(CustomPermissions):
    actions_scopes = {
        'list': 'project_focal_points_v',
        'create': 'project_focal_points_c',
        'retrieve': "project_focal_points_v",
        'update': 'project_focal_points_u',
        'partial_update': 'project_focal_points_u',
        'destroy': 'project_focal_points_d'
    }


class IncomePermissions(CustomPermissions):
    actions_scopes = {
        'list': 'project_incomes_v',
        'create': 'project_incomes_c',
        'retrieve': "project_incomes_v",
        'update': 'project_incomes_u',
        'partial_update': 'project_incomes_u',
        'destroy': 'project_incomes_d',
        'restore': 'project_incomes_d',
        'trashed': 'project_incomes_d',
        'all': 'project_incomes_v',
    }


class ProjectAttachmentPermissions(CustomPermissions):
    actions_scopes = {
        'list': 'project_attachments_v',
        'create': 'project_attachments_c',
        'retrieve': "project_attachments_v",
        'update': 'project_attachments_u',
        'partial_update': 'project_attachments_u',
        'destroy': 'project_attachments_d'
    }


class TaskAttachmentPermissions(CustomPermissions):
    actions_scopes = {
        'list': 'task_attachments_v',
        'create': 'task_attachments_c',
        'retrieve': "task_attachments_v",
        'update': 'task_attachments_u',
        'partial_update': 'task_attachments_u',
        'destroy': 'task_attachments_d'
    }


class ExpensePermissions(CustomPermissions):
    actions_scopes = {
        'list': 'project_expenses_v',
        'create': 'roles_c',
        'retrieve': "project_expenses_v",
        'update': 'project_expenses_u',
        'partial_update': 'project_expenses_u',
        'destroy': 'project_expenses_d',
        'restore': 'project_expenses_d',
        'trashed': 'project_expenses_d',
        'all': 'project_expenses_v'
    }


class RolePermissions(CustomPermissions):
    actions_scopes = {
        'list': 'roles_v',
        'create': 'roles_c',
        'retrieve': "roles_v",
        'update': 'roles_u',
        'partial_update': 'roles_u',
        'destroy': 'roles_d'
    }
