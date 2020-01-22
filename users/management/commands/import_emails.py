import pandas as pd
from django.core.management.base import BaseCommand
from users.models import ValidEmail
from os.path import dirname


class Command(BaseCommand):
    help = 'Imports valid emails'

    def handle(self, *args, **options):
        file_path = dirname(dirname(dirname(dirname(__file__)))) + '/production_env/contacts.csv'
        contacts = pd.read_csv(file_path)
        contacts = contacts['email']
        contacts = contacts.str.lower()

        for email in contacts:
            ValidEmail.objects.get_or_create(
                email=email
            )
