from django.core.management.base import BaseCommand
from users.models import Role, User
from common.permissions import addPermissionList


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
        addPermissionList(user_obj)
