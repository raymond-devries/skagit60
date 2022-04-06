from os.path import dirname

import pandas as pd
from django.core.management.base import BaseCommand

from tracker.models import Peak


class Command(BaseCommand):
    help = "Imports peak data"

    def handle(self, *args, **options):
        file_path = dirname(__file__) + "/final_list.csv"
        peaks_df = pd.read_csv(file_path)

        for index, row in peaks_df.iterrows():
            Peak.objects.get_or_create(
                name=row["Mountain"],
                display_name=row["Cleaned Name"],
                elevation=row["Elevation"],
                lat=row["Latitude"],
                long=row["Longitude"],
                peakbagger_link=row["Peakbagger Link"],
            )
