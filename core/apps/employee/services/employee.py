from abc import (
    ABC,
    abstractmethod,
)
from typing import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.apps.employee.entities.employee import EmployeeEntity
from core.apps.employee.filters.employee import EmployeeFilters
from core.apps.employee.models.employee import EmployeeModel


class BaseEmployeeService(ABC):
    @abstractmethod
    def get_employee_count(self, filters: EmployeeFilters) -> int: ...

    @abstractmethod
    def get_employee_list(
        self,
        filters: EmployeeFilters,
        pagination: PaginationIn,
    ) -> Iterable[EmployeeEntity]: ...


class ORMEmployeeService(BaseEmployeeService):
    def _build_get_employee_list_query(self, filters: EmployeeFilters) -> Q:
        query = Q()

        # Фильтр по ID
        if filters.id is not None:
            query &= Q(id=filters.id)

        # Фильтр по списку ID
        if filters.ids is not None:
            query &= Q(id__in=filters.ids)

        # Фильтры по текстовым полям
        if filters.first_name is not None:
            query &= Q(first_name__icontains=filters.first_name)

        if filters.last_name is not None:
            query &= Q(last_name__icontains=filters.last_name)

        if filters.middle_name is not None:
            query &= Q(middle_name__icontains=filters.middle_name)

        if filters.position is not None:
            query &= Q(position__icontains=filters.position)

        # Общий поиск по всем текстовым полям
        if filters.search is not None:
            search_query = (
                Q(first_name__icontains=filters.search)
                | Q(last_name__icontains=filters.search)
                | Q(middle_name__icontains=filters.search)
                | Q(position__icontains=filters.search)
            )
            query &= search_query

        # Фильтр по дате приёма на работу
        if filters.date_hired_from is not None:
            query &= Q(date_hired__gte=filters.date_hired_from)

        if filters.date_hired_to is not None:
            query &= Q(date_hired__lte=filters.date_hired_to)

        # Фильтр по зарплате
        if filters.salary_min is not None:
            query &= Q(salary__gte=filters.salary_min)

        if filters.salary_max is not None:
            query &= Q(salary__lte=filters.salary_max)

        # Фильтр по менеджеру
        if filters.manager_id is not None:
            query &= Q(manager_id=filters.manager_id)

        # Фильтры по дате создания
        if filters.created_at_from is not None:
            query &= Q(created_at__gte=filters.created_at_from)

        if filters.created_at_to is not None:
            query &= Q(created_at__lte=filters.created_at_to)

        # Фильтры по дате обновления
        if filters.updated_at_from is not None:
            query &= Q(updated_at__gte=filters.updated_at_from)

        if filters.updated_at_to is not None:
            query &= Q(updated_at__lte=filters.updated_at_to)

        return query

    def get_employee_list(
        self,
        filters: EmployeeFilters,
        pagination: PaginationIn,
    ) -> Iterable[EmployeeEntity]:
        query = self._build_get_employee_list_query(filters)

        queryset = EmployeeModel.objects.filter(query)[
            pagination.offset : pagination.offset + pagination.limit
        ]

        return [employee.to_entity() for employee in queryset]

    def get_employee_count(self, filters: EmployeeFilters) -> int:
        query = self._build_get_employee_list_query(filters)
        return EmployeeModel.objects.filter(query).count()
