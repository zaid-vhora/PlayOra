from django.apps import AppConfig


class RentalappConfig(AppConfig):
    name = 'app_modules.rentalapp'


class AuthAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_modules.rentalapp"