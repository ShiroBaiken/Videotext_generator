from django.db import models

class Video(models.Model):
    text = models.CharField(max_length=255)
    image = models.CharField(max_length=255, null=True, blank=True)
    video_file = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

