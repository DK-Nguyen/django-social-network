from django.db import models
from django.contrib.auth.models import AbstractUser

# Generally, each model maps to a single database table.


class SiteUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False)
    email_verified = models.BooleanField(null=False)
    phone_number = models.CharField(max_length=15, blank=False)
    address = models.TextField(blank=False)
    bio = models.TextField(blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email_verified = False

    def name(self):
        return self.first_name + self.last_name


class Profile(models.Model):
    # when a user is deleted, also delete the profile, but not otherwise
    user = models.OneToOneField(SiteUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pictures/')

    def __str__(self):
        return f'{self.user.username} Profile'