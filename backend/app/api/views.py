import numpy as np

from ..data_processing import get_processed_music_data
from django.db.models import Avg, F, Count
from django.http import JsonResponse
from ..models import Music, Rating
from random import choice
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MusicSerializer, RatingSerializer


def music_analysis_data(request):
    try:
        data = get_processed_music_data()
        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


class MusicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer

    @action(detail=False, methods=['get'])
    def random(self, request):
        labels = Music.objects.values_list('label', flat=True).distinct()
        random_label = choice(labels)
        random_track = Music.objects.filter(label=random_label, complexity__isnull=False, originality__isnull=False,
                                            gradus__isnull=False).order_by('?').first()
        if random_track:
            serializer = self.get_serializer(random_track)
            return Response(serializer.data)
        return Response({"error": "No music tracks available"}, status=404)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @action(detail=False, methods=['post'])
    def rate_song(self, request):
        song_id = request.data.get('song')
        rating = request.data.get('rating')

        if not song_id:
            return Response({"error": "Song ID is required"}, status=400)
        if not rating:
            return Response({"error": "Rating is required"}, status=400)

        try:
            Music.objects.get(id=song_id)
        except Music.DoesNotExist:
            return Response({"error": "Song not found"}, status=404)

        serializer = self.get_serializer(data={'song': song_id, 'rating': rating})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    @action(detail=False, methods=['get'])
    def song_ratings(self, request):
        song_id = request.query_params.get('song')
        if not song_id:
            return Response({"error": "Song ID is required"}, status=400)

        ratings = Rating.objects.filter(song_id=song_id)
        serializer = self.get_serializer(ratings, many=True)
        return Response(serializer.data)
