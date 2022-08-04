from django.core.management.base import BaseCommand
from users.models import Action, SubAction, Permission
from projects.models import Project, ProjectRole
import json


class Command(BaseCommand):
    help = 'Create Project Permissions'

    def add_arguments(self, parser):
        parser.add_argument('role', type=str,
                            help='Indicates role')

        parser.add_argument('project', type=str,
                            help='Define Project id', )

    def handle(self, *args, **kwargs):
        info = open('json/project_actions.json')
        actions = json.loads(info.read())
        permissions_list = []
        for action in actions:
            action_obj, created = Action.objects.get_or_create(
                name=action['fields']['name'])
            action_obj.codename = action['fields']['codename']
            action_obj.model = action['fields']['model']
            action_obj.save()
            for sub_action in action['sub_actions']:
                sub_action_obj, created = SubAction.objects.get_or_create(
                    code=sub_action['code'], name=sub_action['name'])
                permission, created = Permission.objects.get_or_create(
                    action=action_obj, sub_action=sub_action_obj)
                permissions_list.append(permission)

        role = kwargs['role']
        project = kwargs['project']
        project_obj = Project.objects.get(pk=project)
        role_obj, created = ProjectRole.objects.get_or_create(
            name=role, project=project_obj)
        role_obj.projects_permissions.set(permissions_list)
        role_obj.save()
