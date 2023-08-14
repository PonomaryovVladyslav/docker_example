"""File to config app."""
from django.apps import AppConfig


class AppConf(AppConfig):
    """Class to config app."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
