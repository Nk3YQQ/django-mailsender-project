from django.contrib.auth.models import Group
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        group_name = 'Модератор'

        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" was created'))

        else:
            self.stdout.write(f'Group "{group_name}" already exists')
