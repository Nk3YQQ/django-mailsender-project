from django.core.management import BaseCommand
from main.cron import send_email


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_email()
