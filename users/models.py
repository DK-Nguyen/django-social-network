from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class SiteUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False)
    email_verified = models.BooleanField(null=False)
    phone_number = models.CharField(max_length=15, blank=False)
    address = models.TextField(blank=False)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email_verified = False

    def name(self):
        return self.first_name + self.last_name
