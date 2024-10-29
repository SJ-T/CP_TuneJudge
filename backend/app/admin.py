from django.contrib import admin

from .models import Music, Rating


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'label', 'file')


@admin.register(Rating)
class RateAdmin(admin.ModelAdmin):
    list_display = ('song', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('song__title',)
