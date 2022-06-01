from django.db.models import Q
from users.api.serializers import PermissionSerializer
from users.models import Role, Permission, UserPermissionList


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
        user=user)
    userPer.permissions_list = permissions
    userPer.save()
