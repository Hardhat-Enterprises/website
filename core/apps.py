from django.contrib.admin.apps import AdminConfig



class CustomAdminConfig(AdminConfig):
    default_site = "core.admin_config.CustomAdminSite"


from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
