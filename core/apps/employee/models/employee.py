from datetime import datetime

from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.employee.entities.employee import EmployeeEntity


class EmployeeModel(TimedBaseModel):
    id = models.BigAutoField(primary_key=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=255)
    first_name = models.CharField(verbose_name="Имя", max_length=255)
    middle_name = models.CharField(verbose_name="Отчество", max_length=255)
    position = models.CharField(verbose_name="Должность", max_length=128)
    date_hired = models.DateField(verbose_name="Дата приёма на работу")
    salary = models.DecimalField(
        verbose_name="Размер заработной платы",
        max_digits=12,
        decimal_places=2,
    )
    manager = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="subordinates",
        on_delete=models.SET_NULL,
        verbose_name="Начальник",
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()

    def get_full_name(self) -> str:
        """Возвращает полное ФИО сотрудника."""
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()

    get_full_name.short_description = "ФИО"

    class Meta:
        db_table = "employee"
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def to_entity(self) -> EmployeeEntity:
        return EmployeeEntity(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
            position=self.position,
            date_hired=datetime.combine(self.date_hired, datetime.min.time()),
            salary=float(self.salary),
            manager=self.manager.to_entity() if self.manager else None,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
