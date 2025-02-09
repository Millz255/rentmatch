from django.apps import AppConfig


class RentappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rentapp'

    def ready(self):
        import rentapp.signals  # Ensure signals are imported when app is ready
