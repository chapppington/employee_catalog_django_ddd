from datetime import (
    date,
    datetime,
)

from pydantic import BaseModel


class EmployeeFilters(BaseModel):
    # ID фильтры
    id: int | None = None
    ids: list[int] | None = None

    # Текстовые поля (поиск по частичному совпадению)
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    position: str | None = None

    # Общий поиск по всем текстовым полям
    search: str | None = None

    # Фильтр по дате приёма на работу (диапазон)
    date_hired_from: date | None = None
    date_hired_to: date | None = None

    # Фильтр по зарплате (диапазон)
    salary_min: float | None = None
    salary_max: float | None = None

    # Фильтр по менеджеру
    manager_id: int | None = None

    # Фильтры по датам создания и обновления (диапазон)
    created_at_from: datetime | None = None
    created_at_to: datetime | None = None
    updated_at_from: datetime | None = None
    updated_at_to: datetime | None = None
