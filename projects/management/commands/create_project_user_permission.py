from django.core.management.base import BaseCommand
from projects.models import ProjectPermissionUser, ProjectPermission, Project
from users.models import User


class Command(BaseCommand):
    help = 'Create project permission user'

    def add_arguments(self, parser):
        parser.add_argument('project', type=str,
                            help='Define project id')

        parser.add_argument('user', type=str,
                            help='Define user id')

    def handle(self, *args, **kwargs):
        project = kwargs['project']
        project_obj = Project.objects.get(pk=project)
        user = kwargs['user']
        user_obj = User.objects.get(pk=user)
        permissions = ProjectPermission.objects.all()
        for permission in permissions:
            p, created = ProjectPermissionUser.objects.get_or_create(
                user=user_obj, project_permission=permission, project=project_obj)
