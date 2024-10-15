from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'music', views.MusicViewSet)
router.register(r'ratings', views.RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('rate-song/', views.RatingViewSet.as_view({'post': 'rate_song'}), name='rate-song'),
    path('song-ratings/', views.RatingViewSet.as_view({'get': 'song_ratings'}), name='song-ratings'),
]
