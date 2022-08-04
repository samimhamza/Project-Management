from django.core.management.base import BaseCommand
from projects.models import ProjectRole
from users.models import User


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
        try:
            user_obj = User.objects.get(pk=user)
            try:
                role_obj = ProjectRole.objects.get(name=role)
                user_obj.prole_users.set([role_obj])
                user_obj.save()
            except ProjectRole.DoesNotExist:
                print('Project role does not exist')
        except User.DoesNotExist:
            print('User does not exist')
