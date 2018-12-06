from django.db import models
from django.contrib.auth.models import AbstractUser

# Generally, each model maps to a single database table.


class SiteUser(AbstractUser):
    """
    This class represents a User of the website, it inherits from AbstractUser
    The variables are self-commented.
    """
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False, unique=True)
    email_verified = models.BooleanField(null=False, default=False)
    phone_number = models.CharField(max_length=15, blank=False)
    address = models.TextField(blank=False)
    bio = models.TextField(blank=True)
    friends = models.ManyToManyField("SiteUser", related_name='user_friends', blank=True)

    def name(self):
        return self.first_name + self.last_name

