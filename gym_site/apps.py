from django.apps import AppConfig

class GymSiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # ← исправлено
    name = 'gym_site'
    verbose_name = 'Фитнес сайт'