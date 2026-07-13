from django.apps import AppConfig

class UserappConfig(AppConfig):
    name = 'app_modules.userapp'

class AuthAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_modules.userapp"