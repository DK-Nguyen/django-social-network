from django.db import models
from django.conf import settings


class Event(models.Model):
    """
        This model is for a single Event in the application. The events are sorted by newest first
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False)
    description = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=False)
    location = models.CharField(max_length=150)

    def get_absolute_url(self):
        """
        This method return the relative url for viewing a single event
        :return: the relative url as string
        """
        return "/events/%i/" % self.id

    class Meta:
        ordering = ['-created_time']


class EventParticipant(models.Model):
    """
    This model is for saving event's participants. Everytime an user is invited, a new object is created and
    by default they didn't accept it yet.
    """
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inviter')
    invitee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitee')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

