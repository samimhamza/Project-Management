from django.core.management.base import BaseCommand
from users.models import Action, Permission, SubAction


class Command(BaseCommand):
    help = 'Create permissions'

    def handle(self, *args, **kwargs):
        actions = Action.objects.all()
        sub_actions = SubAction.objects.all()

        for action in actions:
            for sub_action in sub_actions:
                Permission.objects.get_or_create(
                    action=action,
                    sub_action=sub_action
                )
