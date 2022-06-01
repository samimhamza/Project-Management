from .permissions import CustomPermissions

TaskPermissions = CustomPermissions
TaskPermissions.actions_scopes = {
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

ProjectPermissions = CustomPermissions
ProjectPermissions.actions_scopes = {
    'list': 'projects_v',
    'create': 'projects_c',
    'retrieve': "projects_v",
    'update': 'projects_u',
    'partial_update': 'projects_u',
    'destroy': 'projects_d',
    'restore': 'projects_d',
    'trashed': 'projects_d',
    'all': 'projects_v'
}

CommentPermissions = CustomPermissions
CommentPermissions.actions_scopes = {
    'list': 'comments_v',
    'create': 'comments_c',
    'retrieve': "comments_v",
    'update': 'comments_u',
    'partial_update': 'comments_u',
    'destroy': 'comments_d'
}

UserPermissions = CustomPermissions
UserPermissions.actions_scopes = {
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
TeamPermissions = CustomPermissions
TeamPermissions.actions_scopes = {
    'list': 'teams_v',
    'create': 'teams_c',
    'retrieve': "teams_v",
    'update': 'teams_u',
    'partial_update': 'teams_u',
    'destroy': 'teams_d',
    'restore': 'teams_d',
    'trashed': 'teams_d',
    'all': 'teams_v',
    'users': 'team_users_v',
    'add_users': 'team_users_c',
    'excluded_users': 'users_v',
    'excluded_projects': 'projects_v',
    'add_project': 'team_projects_c',
    'delete_user': 'team_users_d'
}

HolidayPermissions = CustomPermissions
HolidayPermissions.actions_scopes = {
    'list': 'holidays_v',
    'create': 'holidays_c',
    'retrieve': "holidays_v",
    'update': 'holidays_u',
    'partial_update': 'holidays_u',
    'destroy': 'holidays_d'
}

ReminderPermissions = CustomPermissions
ReminderPermissions.actions_scopes = {
    'list': 'reminders_v',
    'create': 'reminders_c',
    'retrieve': "reminders_v",
    'update': 'reminders_u',
    'partial_update': 'reminders_u',
    'destroy': 'reminders_d'
}

LocationPermissions = CustomPermissions
LocationPermissions.actions_scopes = {
    'list': 'project_locations_v',
    'create': 'project_locations_c',
    'retrieve': "project_locations_v",
    'update': 'project_locations_u',
    'partial_update': 'project_locations_u',
    'destroy': 'project_locations_d'
}

PaymentPermissions = CustomPermissions
PaymentPermissions.actions_scopes = {
    'list': 'project_payments_v',
    'create': 'project_payments_c',
    'retrieve': "project_payments_v",
    'update': 'project_payments_u',
    'partial_update': 'project_payments_u',
    'destroy': 'project_payments_d'
}
FocalPointPermissions = CustomPermissions
FocalPointPermissions.actions_scopes = {
    'list': 'project_focal_points_v',
    'create': 'project_focal_points_c',
    'retrieve': "project_focal_points_v",
    'update': 'project_focal_points_u',
    'partial_update': 'project_focal_points_u',
    'destroy': 'project_focal_points_d'
}
IncomePermissions = CustomPermissions
IncomePermissions.actions_scopes = {
    'list': 'project_incomes_v',
    'create': 'project_incomes_c',
    'retrieve': "project_incomes_v",
    'update': 'project_incomes_u',
    'partial_update': 'project_incomes_u',
    'destroy': 'project_incomes_d'
}

AttachmentPermissions = CustomPermissions
AttachmentPermissions.actions_scopes = {
    'list': 'attachments_v',
    'create': 'attachments_c',
    'retrieve': "attachments_v",
    'update': 'attachments_u',
    'partial_update': 'attachments_u',
    'destroy': 'attachments_d'
}
CategoryPermissions = CustomPermissions
CategoryPermissions.actions_scopes = {
    'list': 'categories_v',
    'create': 'categories_c',
    'retrieve': "categories_v",
    'update': 'categories_u',
    'partial_update': 'categories_u',
    'destroy': 'categories_d',
    'restore': 'categories_d',
    'trashed': 'categories_d',
    'all': 'categories_v'
}

ExpensePermissions = CustomPermissions
ExpensePermissions.actions_scopes = {
    'list': 'project_expenses_v',
    'create': 'project_expenses_c',
    'retrieve': "project_expenses_v",
    'update': 'project_expenses_u',
    'partial_update': 'project_expenses_u',
    'destroy': 'project_expenses_d',
    'restore': 'project_expenses_d',
    'trashed': 'project_expenses_d',
    'all': 'project_expenses_v'
}
