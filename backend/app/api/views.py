from ..data_processing import get_processed_music_data
from django.conf import settings
from django.http import JsonResponse
from ..models import Music, Rating
from random import choice
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .serializers import MusicSerializer, RatingSerializer


@api_view(['GET'])
def music_analysis_data(request):
    """
    Get analyzed music feature data for visualization.

    Returns:
        200: JSON containing:
            - origin_df: Original music data
            - pitch_class_dist: Pitch class distribution
            - pitch_transition_dist: Pitch transition distribution
            - interval_dist: Interval distribution
            - interval_size_dist: Interval size distribution
            - interval_dir_dist: Interval direction distribution
            - interval_transition_dist: Interval transition distribution
        500: Error message if data processing fails

    """
    try:
        data = get_processed_music_data()
        return JsonResponse(data, safe=False)

    except Exception as e:
        if settings.DEBUG:
            error_details = str(e)
        else:
            error_details = 'An unexpected error occurred during data analysis'
        return JsonResponse(
            {'error': 'Internal server error', 'details': error_details},
            status=500
        )


class MusicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving music tracks.

    Endpoints:
        GET /music/ - List all music tracks
        GET /music/<id>/ - Retrieve specific music track
        GET /music/random/ - Get a random music track
    """
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
        return Response({'error': 'No music tracks available'}, status=404)


class RatingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing music ratings.

    Endpoints:
        GET /ratings/ - List all ratings
        GET /ratings/<id>/ - Get ratings information with a specific rating ID
        GET /ratings/song_ratings/ - Get ratings for a specific song
        POST /ratings/rate_song/ - Submit a rating for a song
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @action(detail=False, methods=['post'])
    def rate_song(self, request):
        song_id = request.data.get('song')
        rating = request.data.get('rating')

        if not song_id:
            return Response({'error': 'Song ID is required'}, status=400)
        if not rating:
            return Response({'error': 'Rating is required'}, status=400)

        try:
            Music.objects.get(id=song_id)
        except Music.DoesNotExist:
            return Response({'error': 'Song not found'}, status=404)

        serializer = self.get_serializer(data={'song': song_id, 'rating': rating})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['get'])
    def song_ratings(self, request):
        song_id = request.query_params.get('song')
        if not song_id:
            return Response({'error': 'Song ID is required'}, status=400)

        ratings = Rating.objects.filter(song_id=song_id)
        serializer = self.get_serializer(ratings, many=True)
        return Response(serializer.data)
