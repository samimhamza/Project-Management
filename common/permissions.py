import re
from users.models import UserPermissionList, Permission, Action, SubAction, Role
from users.models import Role, Permission, UserPermissionList, User
from users.api.serializers import PermissionSerializer
from rest_framework import permissions
from django.db.models import Q


def checkScope(user, scope):
    try:
        permissionScopes = UserPermissionList.objects.only(
            'permissions_list').get(user=user)
    except UserPermissionList.DoesNotExist:
        return False

    if scope in permissionScopes.permissions_list:
        return True
    else:
        return False


def addPermissionList(user, permissions_ids=None):
    if permissions_ids is None:
        user_role = Role.objects.only('name').filter(users=user)
        permissions_list = Permission.objects.filter(
            Q(users=user) | Q(roles__in=user_role))
    else:
        permissions_list = Permission.objects.filter(pk__in=permissions_ids)
    serializer = PermissionSerializer(permissions_list, many=True)
    permissions = []
    for permission in serializer.data:
        per = permission['action']['name']
        action = permission['sub_action']['code']
        code = per + "_" + action
        if code not in permissions:
            permissions.append(code)

    userPer, created = UserPermissionList.objects.get_or_create(
        user=user)
    userPer.permissions_list = permissions
    userPer.save()


class CustomPermissions(permissions.BasePermission):
    actions_scopes = {}
    methods_scopes = {}

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            for attr, value in self.actions_scopes.items():
                if value == "pass":
                    return True
                if view.action == attr:
                    return checkScope(request.user, value)
            for attr, value in self.methods_scopes.items():
                if request.method == attr:
                    return checkScope(request.user, value)
        return False


def addPermissionsToUser(permissions, user):
    permissions_list = []
    for key, value in permissions.items():
        action = Action.objects.only('id').get(pk=key)
        sub_actions = SubAction.objects.only('id').filter(pk__in=value)
        permissions_obj = Permission.objects.filter(
            action=action, sub_action__in=sub_actions)
        for per in permissions_obj:
            permissions_list.append(per.id)
    user.permissions_users.set(permissions_list)
    addPermissionList(user, permissions_list)


def addRolesToUser(roles, user):
    roles_obj = Role.objects.only('id').filter(pk__in=roles)
    user.roles_users.set(roles_obj)
    addPermissionList(user)


def addPermissionsToRole(permissions, role):
    permissions_list = []
    for key, value in permissions.items():
        action = Action.objects.only('id').get(pk=key)
        sub_actions = SubAction.objects.only('id').filter(pk__in=value)
        permissions_obj = Permission.objects.filter(
            action=action, sub_action__in=sub_actions)
        for per in permissions_obj:
            permissions_list.append(per.id)
    role.permissions_roles.set(permissions_list)
    users = User.objects.filter(roles_users=role)
    for user in users:
        addPermissionList(user, permissions_list)


def checkCustomPermissions(request, value):
    if request.user.is_authenticated:
        return checkScope(request.user, value)
    return False
