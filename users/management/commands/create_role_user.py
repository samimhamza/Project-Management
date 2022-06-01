from django.core.management.base import BaseCommand
from users.models import Role, User, Permission, UserPermissionList
from django.db.models import Q
from users.api.serializers import PermissionSerializer


class Command(BaseCommand):
    help = 'Create permission roles'

    def add_arguments(self, parser):
        parser.add_argument('role', type=str,
                            help='Indicates role')

        parser.add_argument('user', type=str,
                            help='Define user id', )

    def handle(self, *args, **kwargs):
        role = kwargs['role']
        user = kwargs['user']
        user_obj = User.objects.get(pk=user)
        role_obj = Role.objects.get(name=role)
        user_obj.roles_users.set([role_obj])
        user_obj.save()

        user_role = Role.objects.only('codename').filter(user=user_obj)
        permissions_list = Permission.objects.filter(
            Q(user=user_obj) | Q(role__in=user_role))
        serializer = PermissionSerializer(permissions_list, many=True)
        permissions = []
        for permission in serializer.data:
            per = permission['action']['codename']
            action = permission['sub_action']['code']
            permissions.append(per + "" + action)

        userPer, created = UserPermissionList.objects.get_or_create(
            user=user_obj)
        userPer.permissions_list = permissions
        userPer.save()
