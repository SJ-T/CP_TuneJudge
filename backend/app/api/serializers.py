from rest_framework import serializers
from ..models import Music, Rating


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = [
            'id', 'title', 'label', 'file', 'key',
            'npvi', 'note_density', 'pitch_range',
            'pitch_count', 'pitch_class_count',
            'pitch_entropy', 'pitch_class_entropy',
            'pitch_in_scale_rate', 'scale_consistency',
            'polyphony', 'polyphony_rate',
            'complexity', 'originality', 'gradus'
        ]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'song', 'rating']