import numpy as np
import pandas as pd

from app.models import Music
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populate array fields from string representations'

    def process_array_field(self, value):
        if pd.isna(value):
            return None
        if isinstance(value, str):
            return np.fromstring(value.strip('[]'), sep=' ').tolist()
        return value

    def process_2d_array_field(self, value):
        if pd.isna(value):
            return None
        if isinstance(value, str):
            print([np.fromstring(r.strip('[]'), sep=' ').tolist() for r in value.split(';')])
            return [np.fromstring(r.strip('[]'), sep=' ').tolist() for r in value.split(';')]
        return value

    def handle(self, *args, **options):
        csv_path_ds = settings.DATASET_FEATURES_PATH
        csv_path_exp = settings.EXP_FEATURES_PATH
        df = pd.concat([pd.read_csv(csv_path_ds), pd.read_csv(csv_path_exp)], ignore_index=True)
        for _, row in df.iterrows():
            music, created = Music.objects.get_or_create(
                title=row['file_name'],
                label=row['genre']
            )
            music.duration = row['duration']
            music.pc_dist1 = self.process_array_field(row['pc_dist1'])
            music.pc_dist2 = self.process_2d_array_field(row['pc_dist2'])
            music.iv_dist1 = self.process_array_field(row['iv_dist1'])
            music.ivsize_dist1 = self.process_array_field(row['ivsize_dist1'])
            music.ivdir_dist1 = self.process_array_field(row['ivdir_dist1'])
            music.iv_dist2 = self.process_2d_array_field(row['iv_dist2'])

            music.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created new Music object: {music}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated existing Music object: {music}'))

        self.stdout.write(self.style.SUCCESS('Data import completed successfully'))