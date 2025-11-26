
from django.apps import AppConfig


class AroniaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aronia'
    label = 'dede'  # keep legacy DB label so migrations/tables stay intact
    verbose_name = 'Aronia'
