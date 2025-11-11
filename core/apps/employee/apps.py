from django.apps import AppConfig


class EmployeeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.apps.employee"
    verbose_name = "Сотрудники"
