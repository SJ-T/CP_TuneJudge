from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import default_storage
from django.core.validators import MinValueValidator, MaxValueValidator


class Music(models.Model):
    LABEL_CHOICES = [
        ('classical', 'Classical'),
        ('pop', 'Pop'),
        ('exp1', 'trained with pop'),
        ('exp2', 'trained with pop and classical'),
        ('exp3', 'trained with pop and classical(CnG major)'),
    ]
    title = models.CharField(max_length=255)
    label = models.CharField(choices=LABEL_CHOICES, max_length=50)
    file = models.FileField(storage=default_storage, null=True, blank=True, max_length=255)
    key = models.CharField(max_length=3, null=True, blank=True)
    npvi = models.FloatField(null=True, blank=True)
    note_density = models.FloatField(null=True, blank=True)
    pitch_range = models.IntegerField(null=True, blank=True)
    pitch_count = models.IntegerField(null=True, blank=True)
    pitch_class_count = models.IntegerField(null=True, blank=True)
    pitch_entropy = models.FloatField(null=True, blank=True)
    pitch_class_entropy = models.FloatField(null=True, blank=True)
    pitch_in_scale_rate = models.FloatField(null=True, blank=True)
    scale_consistency = models.FloatField(null=True, blank=True)
    polyphony = models.FloatField(null=True, blank=True)
    polyphony_rate = models.FloatField(null=True, blank=True)
    complexity = models.FloatField(null=True, blank=True)
    originality = models.FloatField(null=True, blank=True)
    gradus = models.FloatField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    pc_dist1 = ArrayField(models.FloatField(), size=12, null=True, blank=True)
    pc_dist2 = ArrayField(ArrayField(models.FloatField(), size=12), size=12, null=True, blank=True)
    iv_dist1 = ArrayField(models.FloatField(), size=25, null=True, blank=True)
    ivsize_dist1 = ArrayField(models.FloatField(), size=13, null=True, blank=True)
    ivdir_dist1 = ArrayField(models.FloatField(), size=12, null=True, blank=True)
    iv_dist2 = ArrayField(ArrayField(models.FloatField(), size=25), size=25, null=True, blank=True)

    class Meta:
        verbose_name = "Music Track"
        verbose_name_plural = "Music Tracks"
        constraints = [
            models.UniqueConstraint(fields=['title', 'label'], name='unique_music_title_label')
        ]

    def __str__(self):
        return f"{self.label}, {self.title}"


class Rating(models.Model):
    song = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Rating {self.rating} for {self.song.file}"
