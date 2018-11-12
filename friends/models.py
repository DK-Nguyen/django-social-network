from users.models import SiteUser
from django.db import models


class FriendRequest(models.Model):
    to_user = models.ForeignKey(SiteUser, related_name='to_user', on_delete=models.PROTECT)
    from_user = models.ForeignKey(SiteUser, related_name='from_user', on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)

    def get_from_user_id(self):
        return self.from_user_id

    def get_to_user_id(self):
        return self.to_user_id





