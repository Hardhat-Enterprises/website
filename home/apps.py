import sys
from django.apps import AppConfig

class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home"

    def ready(self):
        import home.signals
        import home.audit_signals
        if 'runserver' in sys.argv:
                try:
                    print("[App Ready] Triggering inserts...")
                    from home.insert_defaults import insert_default_projects, insert_default_courses
                    insert_default_projects()
                    insert_default_courses()
                except Exception as e:
                    print(f"[ERROR] insert_defaults failed: {e}")