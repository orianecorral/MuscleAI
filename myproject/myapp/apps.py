from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'  # Assure-toi que c’est bien le nom de ton app

    def ready(self):
        import myapp.signals  # Assure-toi que le fichier existe
