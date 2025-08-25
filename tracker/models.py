# tracker/models.py
from django.db import models
import uuid # ¡Añade esta importación!

class TrackerURL(models.Model):
    name = models.CharField(max_length=200)
    tracker_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) # ¡CAMBIADO!
    image_to_show = models.ImageField(upload_to='tracker_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Tracker: {self.name} ({self.tracker_id})"

class Visit(models.Model):
    tracker_url = models.ForeignKey(TrackerURL, on_delete=models.CASCADE, related_name='visits')
    ip_address = models.GenericIPAddressField(null = True, blank = True)
    user_agent = models.TextField(null = True, blank = True)
    referer = models.TextField(null = True, blank = True)

    country = models.CharField(max_length = 100, null = True, blank = True)
    city = models.CharField(max_length = 100, null = True, blank = True)
    latitude = models.FloatField(null = True, blank = True)
    longitude = models.FloatField(null = True, blank = True)

    timestamp = models.DateTimeField(auto_now_add = True)