# Register your models here.
from django.contrib import admin

from core.apps.employee.models import EmployeeModel


@admin.register(EmployeeModel)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "get_full_name",
        "position",
        "date_hired",
        "salary",
        "manager",
    )
    list_filter = ("position", "date_hired", "manager")
    search_fields = ("first_name", "last_name", "middle_name")
    list_per_page = 10
    list_select_related = ("manager",)

    fieldsets = (
        (
            "ФИО",
            {
                "fields": ("last_name", "first_name", "middle_name"),
            },
        ),
        (
            "Информация о работе",
            {
                "fields": ("position", "date_hired", "salary", "manager"),
            },
        ),
    )
