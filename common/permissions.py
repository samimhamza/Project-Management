from django.db.models import Q
from users.api.serializers import PermissionSerializer
from users.models import Role, Permission, UserPermissionList
from users.models import UserPermissionList
from rest_framework import permissions


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


def addPermissionList(user):
    user_role = Role.objects.only('name').filter(user=user)
    permissions_list = Permission.objects.filter(
        Q(user=user) | Q(role__in=user_role))
    serializer = PermissionSerializer(permissions_list, many=True)
    permissions = []
    for permission in serializer.data:
        per = permission['action']['name']
        action = permission['sub_action']['code']
        permissions.append(per + "_" + action)

    userPer, created = UserPermissionList.objects.get_or_create(
        user=user, permissions_list=permissions)
    userPer.permissions_list = permissions
    userPer.save()


class CustomPermissions(permissions.BasePermission):
    actions_scopes = {}

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            for attr, value in self.actions_scopes.items():
                if view.action == attr:
                    return checkScope(request.user, value)
        return False
