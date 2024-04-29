from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        superuser = User.objects.create(
            email='admin@mail.ru',
            first_name='Admin',
            last_name='Adminov',
            is_staff=True,
            is_superuser=True
        )

        superuser.set_password('908poi543tre')
        superuser.save()
