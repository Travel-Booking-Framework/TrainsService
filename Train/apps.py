from django.apps import AppConfig


class TrainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Train'

    def ready(self):
        # Import signals to ensure they're loaded
        import Train.signals