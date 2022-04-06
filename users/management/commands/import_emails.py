from os.path import dirname

import pandas as pd
from django.core.management.base import BaseCommand

from users.models import ValidEmail


class Command(BaseCommand):
    help = "Imports valid emails"

    def handle(self, *args, **options):
        file_path = dirname(dirname(dirname(dirname(__file__)))) + "/contacts.csv"
        contacts = pd.read_csv(file_path)
        contacts = contacts["E-mail 1 - Value"]
        contacts = contacts.str.lower()

        for email in contacts:
            ValidEmail.objects.get_or_create(email=email)
