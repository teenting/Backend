from django.apps import AppConfig


class AssignmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assignment'
    def ready(self) -> None:
        import assignment.signals
        return super().ready()
