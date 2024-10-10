from django.contrib import admin

from .models import Music, Rating

# Register your models here.
@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'label', 'file')

@admin.register(Rating)
class RateAdmin(admin.ModelAdmin):
    list_display = ('song', 'rating')