from django.apps import AppConfig


class MemberConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapps.member'
    def ready(self):
        from . import signals