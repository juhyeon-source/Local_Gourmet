from django.apps import AppConfig

class ScrappersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "scrappers"
    
    def ready(self):
        from local_gourmet.tasks import start_scheduler
        start_scheduler()