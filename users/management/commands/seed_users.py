from django_seed import Seed
from users.models import User
from django.core.management.base import BaseCommand
import random
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create Countries with States'

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()
        seeder.add_entity(User, 10, {
            'first_name': lambda x: seeder.faker.name(),
            'last_name': lambda x: seeder.faker.name(),
            'phone': lambda x: seeder.faker.phone_number(),
            'profile': lambda x:  seeder.faker.file_extension(category='image'),
            'whatsapp': lambda x: seeder.faker.phone_number(),
            'position': lambda x: seeder.faker.job(),
            'username': lambda x: seeder.faker.user_name(),
            'email': lambda x: seeder.faker.email(),
            'date_joined': lambda x: seeder.faker.date_time(),
            'created_at': lambda x: seeder.faker.date_time(),
            'deleted_at': lambda x: seeder.faker.date_time(),
            'is_active': lambda x: seeder.faker.boolean(chance_of_getting_true=100),
        })
        seeder.execute()
