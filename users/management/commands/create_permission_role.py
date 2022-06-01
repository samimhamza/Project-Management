from django.core.management.base import BaseCommand
from users.models import Role, Permission


class Command(BaseCommand):
    help = 'Create permission roles'

    def add_arguments(self, parser):
        parser.add_argument('role', type=str,
                            help='Indicates role')

    def handle(self, *args, **kwargs):
        role = kwargs['role']
        role_obj = Role.objects.get(name=role)
        if role == 'Admin':
            permissions = Permission.objects.all()
            role_obj.permissions_roles.set(permissions)
            role_obj.save()
