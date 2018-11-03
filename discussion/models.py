from django.db import models

class Discussion(models.Model):
    id = models.PositiveSmallIntegerField(unique = True, blank = False)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 150, blank = False)
    description = models.TextField(blank = True)
    created_date = models.DateTimeField(blank = False)

class DiscussionComment(models.Model):
    id = models.PositiveSmallIntegerField(unique = True, blank = False)
    discussion_id = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    commenter_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = TextField(blank = False)
    created_date = models.DateTimeField(blank = False)
