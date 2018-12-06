from django.db import models
from django.conf import settings


class Status(models.Model):
    """
    This class represents a status. When a user creates a status, an object of this class is created

    Args:
        owner (SiteUser): the owner of the status
        content (TextField): the content of the status
        created_time (DateTimeField): the time that the status is created
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    created_time = models.DateTimeField(auto_now_add=True, editable=False)

    def get_absolute_url(self):
        """
        This function returns the url of the status
        :return:
            an url ends with the id of the status
        """
        return "/status/%i/" % self.id

    class Meta:
        """
        This function makes the order of the status reverses to the created time
        e.g. the newest status will be on the top
        """
        ordering = ['-created_time']

    def __str__(self):
        """
        This function returns the information about an object of this class in a string

        :return:
            a string
        """
        return "From {} at {}:{}/{}/{}".format(self.owner.username, self.created_time.hour,
                                               self.created_time.minute, self.created_time.month,
                                               self.created_time.day)


class StatusComment(models.Model):
    """
        This class represents a comment of a status

        Args:
            status: the status that owns the comment
            commenter: the user that writes the comment
            content: the content of the comment
            created_time: the time that the comment is created
    """
    # one status can have a lot of comments
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    # one user can have a lot of comments
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        """
        This function returns the information about an object of this class in a string

        :return:
            a string
        """
        return "From {} on {} at {}:{}/{}/{}".format(self.commenter.username, self.status_id,
                                                     self.created_time.hour, self.created_time.minute,
                                                     self.created_time.month, self.created_time.day)
