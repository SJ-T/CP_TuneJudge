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
        fields = ['id', 'song', 'rating','created_at']
        read_only_fields = ['id', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Rating must be between 1 and 5')
        return value
