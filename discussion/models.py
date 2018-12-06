from django.db import models
from django.conf import settings


class Discussion(models.Model):
    '''Model for managing discussions'''
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=False)
    description = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        '''Returns the URL of the discussion'''
        return "/discussions/%i/" % self.id

    class Meta:
        ordering = ['-created_time']


class DiscussionComment(models.Model):
    '''Model for managing comments on discussions'''
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_time']


class DiscussionParticipant(models.Model):
    '''Model for managing a discussion's participant'''
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)



