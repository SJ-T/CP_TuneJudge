import os
import pandas as pd

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.db import IntegrityError

from app.models import Music


class Command(BaseCommand):
    help = 'Load music data from CSV and associate wav files'

    def handle(self, *args, **kwargs):
        csv_path_ds = settings.DATASET_FEATURES_PATH
        csv_path_exp = settings.EXP_FEATURES_PATH
        wav_dir = settings.WAV_FILE_PATH
        feature_data = pd.concat([pd.read_csv(csv_path_ds), pd.read_csv(csv_path_exp)], ignore_index=True)

        for _, row in feature_data.iterrows():
            wav_file_name = row['genre'] + '_' + os.path.splitext(row['file_name'])[0] + '.wav'
            wav_file_path = os.path.join(wav_dir, row['genre'], wav_file_name)
            if not os.path.exists(wav_file_path):
                self.stdout.write(self.style.WARNING(f"WAV file not found: {wav_file_path}"))
                continue

            file_name = f"{row['genre']}/{wav_file_name}"

            if Music.objects.filter(title=row['file_name'], label=row['genre']).exists():
                self.stdout.write(self.style.SUCCESS(f"Skipping existing entry: {row['file_name']}"))
                continue
            try:
                with open(wav_file_path, 'rb') as file:
                    file_content = File(file)
                    saved_name = default_storage.save(file_name, file_content)
                music = Music.objects.create(
                    title=row['file_name'],
                    label=row['genre'],
                    file=saved_name,
                    key=row.get('key'),
                    npvi=row.get('npvi'),
                    note_density=row.get('note_density'),
                    pitch_range=row.get('pitch_range'),
                    pitch_count=row.get('pitch_count'),
                    pitch_class_count=row.get('pitch_class_count'),
                    pitch_entropy=row.get('pitch_entropy'),
                    pitch_class_entropy=row.get('pitch_class_entropy'),
                    pitch_in_scale_rate=row.get('pitch_in_scale_rate'),
                    scale_consistency=row.get('scale_consistency'),
                    polyphony=row.get('polyphony'),
                    polyphony_rate=row.get('polyphony_rate'),
                    complexity=row.get('complexity'),
                    originality=row.get('originality'),
                    gradus=row.get('gradus'),
                )
                self.stdout.write(self.style.SUCCESS(f"Created Music object: {music}"))
            except IntegrityError:
                self.stdout.write(self.style.WARNING(f"Duplicate entry, skipping: {row['file_name']}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing {row['file_name']}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS('Data import completed successfully'))
