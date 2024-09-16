from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .services import init_service

        init_service()

        print(" 🔥 CoreConfig ready!")