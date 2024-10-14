from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from random import choice
from ..models import Music, Rating
from .serializers import MusicSerializer, RatingSerializer


class MusicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer

    @action(detail=False, methods=['get'])
    def random(self, request):
        labels = Music.objects.values_list('label', flat=True).distinct()
        random_label = choice(labels)
        random_track = Music.objects.filter(label=random_label).order_by('?').first()
        if random_track:
            serializer = self.get_serializer(random_track)
            return Response(serializer.data)
        return Response({"error": "No music tracks available"}, status=404)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
