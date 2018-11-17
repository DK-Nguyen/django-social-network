from django.db import models
from django.conf import settings


class Status(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return "From {} on {}:{}/{}/{}".format(self.owner.username, self.created_time.hour,
                                               self.created_time.minute, self.created_time.month, self.created_time.day)

# class StatusComment(models.Model):
#     discussion = models.ForeignKey(Status, on_delete=models.CASCADE)
#     commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     content = models.TextField(blank=False)
#     created_time = models.DateTimeField(auto_now_add=True)
