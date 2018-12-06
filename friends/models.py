from users.models import SiteUser
from django.db import models


class FriendRequest(models.Model):
    """ This class represents a friend request. When a user send a friend request, an
        ojbect of this class is created

        Args:
            to_user (SiteUser): the user that is the target of the request
            from_user (SiteUser): the user that sent the request
            created: the time that the request is created
        """
    to_user = models.ForeignKey(SiteUser, related_name='to_user', on_delete=models.PROTECT)
    from_user = models.ForeignKey(SiteUser, related_name='from_user', on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """This function is used to print an object of the class in a format: from someone
        to someone

        :return:
            a string

        """
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)

    def get_from_user_id(self):
        """
        This function is used to get the ID of the user that sent the request

        :return:
            a SiteUser id
        """
        return self.from_user_id

    def get_to_user_id(self):
        """
        This function is used to get the ID of the user that receives the request

        :return:
            a SiteUser id
        """
        return self.to_user_id





