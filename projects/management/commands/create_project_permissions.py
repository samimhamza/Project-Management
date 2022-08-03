from django.core.management.base import BaseCommand
from users.models import Action, SubAction, Permission
import json


class Command(BaseCommand):
    help = 'Create Project User Permissions'

    def add_arguments(self, parser):
        parser.add_argument('project', type=str,
                            help='Define project id')

        parser.add_argument('user', type=str,
                            help='Define user id')

    def handle(self, *args, **kwargs):
        info = open('json/project_actions.json')
        actions = json.loads(info.read())
        for action in actions:
            action_obj, created = Action.objects.get_or_create(
                name=action['fields']['name'])
            action_obj.codename = action['fields']['codename']
            action_obj.model = action['fields']['model']
            action_obj.order = action['fields']['order']
            action_obj.save()
            for sub_action in action['sub_actions']:
                sub_action_obj, created = SubAction.objects.get_or_create(
                    code=sub_action['code'], name=sub_action['name'])
                permission, created = Permission.objects.get_or_create(
                    action=action_obj, sub_action=sub_action_obj)
