from django.core.exceptions import ValidationError
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

    def get_manager_depth(self):
        """Вычисляет глубину иерархии начальников для текущего сотрудника."""
        depth = 0
        current = self.manager
        visited = set()

        # Добавляем текущий объект в посещенные (если он уже сохранен)
        if self.pk:
            visited.add(self.pk)

        while current:
            depth += 1
            if depth > 5:
                return depth
            # Проверка на циклические зависимости
            if current.pk and current.pk in visited:
                return -1  # Обнаружен цикл
            if current.pk:
                visited.add(current.pk)
            # Для новых объектов используем сравнение по идентичности
            elif current == self or current is self:
                return -1
            current = current.manager

        return depth

    def clean(self):
        super().clean()

        # Проверка: сотрудник не может быть своим начальником
        if self.manager and (self.manager == self or self.manager is self):
            raise ValidationError(
                {"manager": "Сотрудник не может быть своим собственным начальником."},
            )

        # Проверка глубины иерархии (максимум 5 уровней)
        if self.manager:
            depth = self.get_manager_depth()
            if depth == -1:
                raise ValidationError(
                    {
                        "manager": "Обнаружена циклическая зависимость в иерархии начальников.",
                    },
                )
            if depth > 5:
                raise ValidationError(
                    {
                        "manager": f"Превышена максимальная глубина иерархии (5 уровней). "
                        f"Текущая глубина: {depth}.",
                    },
                )

    def get_hierarchy_level(self):
        """Возвращает уровень сотрудника в иерархии (0 - самый верхний уровень)."""
        level = 0
        current = self.manager
        visited = set()

        if self.pk:
            visited.add(self.pk)

        while current:
            level += 1
            if current.pk and current.pk in visited:
                # Обнаружен цикл, возвращаем None
                return None
            if current.pk:
                visited.add(current.pk)
            elif current == self or current is self:
                return None
            current = current.manager

        return level

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
