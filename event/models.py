from django.db import models
from django.conf import settings


class Event(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False)
    description = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=False)
    location = models.CharField(max_length=150)

    def get_absolute_url(self):
        return "/events/%i/" % self.id

    class Meta:
        ordering = ['created_time']


class EventParticipant(models.Model):
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inviter')
    invitee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitee')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

