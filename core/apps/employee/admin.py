# Register your models here.
from django.contrib import admin

from core.apps.employee.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "position", "date_hired", "salary", "manager")
    list_filter = ("position", "date_hired")
    search_fields = ("full_name",)
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)
