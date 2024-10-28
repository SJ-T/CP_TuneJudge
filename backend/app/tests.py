import json

from app.api.serializers import MusicSerializer, RatingSerializer
from app.models import Music, Rating
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status



# test models
class MusicModelTests(TestCase):
    def setUp(self):
        self.music_data = {'title': 'Test Song', 'label': 'pop', 'key': 'C'}

    def test_music_creation(self):
        music = Music.objects.create(**self.music_data)
        self.assertEqual(music.title, 'Test Song')
        self.assertEqual(music.label, 'pop')

    def test_unique_constraint(self):
        Music.objects.create(**self.music_data)
        with self.assertRaises(IntegrityError):
            Music.objects.create(**self.music_data)

    def test_label_choices(self):
        self.music_data['label'] = 'invalid_label'
        with self.assertRaises(ValidationError):
            music = Music.objects.create(**self.music_data)
            music.full_clean()


class RatingModelTests(TestCase):
    def setUp(self):
        self.music = Music.objects.create(title='Test Song', label='pop')

    def test_rating_creation(self):
        rating = Rating.objects.create(song=self.music, rating=4)
        self.assertEqual(rating.rating, 4)

    def test_rating_validation(self):
        with self.assertRaises(ValidationError):
            rating = Rating.objects.create(song=self.music, rating=6)
            rating.full_clean()

    def test_cascading(self):
        rating = Rating.objects.create(song=self.music, rating=4)
        self.music.delete()
        self.assertFalse(Rating.objects.filter(id=rating.id).exists())

# test views
class MusicViewSetTests(TestCase):
    def setUp(self):
        self.expected_fields = [
            'id', 'title', 'label', 'file', 'key',
            'npvi', 'note_density', 'pitch_range',
            'pitch_count', 'pitch_class_count',
            'pitch_entropy', 'pitch_class_entropy',
            'pitch_in_scale_rate', 'scale_consistency',
            'polyphony', 'polyphony_rate',
            'complexity', 'originality', 'gradus'
        ]
        self.music_data = [{'title': 'Test Song', 'label': 'pop'},
                           {'title': 'Test Song', 'label': 'classical'},
                           {'title': 'Test Song', 'label': 'exp1'},]
        for data in self.music_data:
            Music.objects.create(**data)

    def test_random_music_endpoint(self):
        response = self.client.get(reverse('music-random'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in self.expected_fields:
            self.assertIn(field, response.json())

    def test_music_list_endpoint(self):
        response = self.client.get(reverse('music-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), len(self.music_data))


class RatingViewSetTests(TestCase):

    def setUp(self):
        self.music = Music.objects.create(title='Test Song', label='pop')
        self.rating_data = {'song': self.music.id, 'rating': 3}

    def create_rating(self, rating_data):
        return self.client.post(
            reverse('rate-song'),
            data=json.dumps(rating_data),
            content_type='application/json'
        )

    def test_rate_song_endpoint(self):
        response = self.create_rating(self.rating_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_song_ratings_endpoint(self):
        self.test_rate_song_endpoint()
        response = self.client.get(reverse('song-ratings'), {'song': self.music.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['rating'], 3)

    def test_get_song_ratings_without_song_id(self):
        response = self.client.get(reverse('song-ratings'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Song ID is required'})

    def test_invalid_rating(self):
        self.rating_data['rating'] = 6
        response = self.create_rating(self.rating_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rate_without_song_id(self):
        del self.rating_data['song']
        response = self.create_rating(self.rating_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Song ID is required'})

    def test_rate_without_rating_score(self):
        del self.rating_data['rating']
        response = self.create_rating(self.rating_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Rating is required'})

    def test_rate_non_existent_music(self):
        self.rating_data['song'] = 99999999
        response = self.create_rating(self.rating_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'error': 'Song not found'})


class MusicAnalysisDataTests(TestCase):
    fixtures = ['test_music_data.json']
    def setUp(self):
        self.fields = ['origin_df', 'pitch_class_dist', 'pitch_transition_dist', 'interval_dist', 'interval_size_dist',
                       'interval_dir_dist', 'interval_transition_dist']
    def test_music_analysis_data_success(self):
        response = self.client.get(reverse('feature-analysis'))
        self.assertEqual(response.status_code, 200)
        for field in self.fields:
            self.assertIn(field, response.json())

    def test_data_processing(self):
        response = self.client.get(reverse('feature-analysis'))
        for field in self.fields:
            field_data = response.json().get(field)
            if field == 'origin_df':
                self.assertFalse(any(item['label'].startswith('exp') for item in field_data))
                self.assertTrue(any(item['label'] == 'pop' for item in field_data))
                self.assertTrue(any(item['label'] == 'classical' for item in field_data))
            else:
                self.assertIn('pop', field_data)
                self.assertIn('classical', field_data)


# test serializers
class RatingSerializerTests(TestCase):
    def setUp(self):
        self.music = Music.objects.create(title='Test Song', label='pop')
        self.rating_data = {'song': self.music.id, 'rating': 4}

    def test_valid_rating(self):
        serializer = RatingSerializer(data=self.rating_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_rating(self):
        self.rating_data['rating'] = 6
        serializer = RatingSerializer(data=self.rating_data)
        self.assertFalse(serializer.is_valid())
        self.rating_data['rating'] = 0
        serializer = RatingSerializer(data=self.rating_data)
        self.assertFalse(serializer.is_valid())
