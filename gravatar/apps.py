from django.apps import AppConfig


class GravatarConfig(AppConfig):
    """
    Gravatar app is a small app to store our custom template tag that turn user's email
    into profile picture using gravatar service
    """
    name = 'gravatar'
