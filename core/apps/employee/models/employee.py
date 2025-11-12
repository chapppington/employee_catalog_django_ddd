from django.db import models

from core.apps.common.models import TimedBaseModel


class Employee(TimedBaseModel):
    full_name = models.CharField(verbose_name="ФИО", max_length=255)
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
        return self.full_name

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
