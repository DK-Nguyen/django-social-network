
from django.contrib import admin
from users.models import SiteUser, Profile

# Register the models
admin.site.register(SiteUser)
admin.site.register(Profile)


