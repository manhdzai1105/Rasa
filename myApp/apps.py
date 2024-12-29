from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myApp'

    def ready(self):
        import myApp.connectDb  # Nạp file connectDb.py