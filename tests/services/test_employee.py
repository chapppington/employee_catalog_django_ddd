"""Test employee service.

1. Test employees count zero, employee count with existing employees
2. Test employee returns all/paginated employees, filters

"""

from datetime import (
    date,
    timedelta,
)

from django.utils import timezone

import pytest
from tests.factories.employee import EmployeeModelFactory

from core.api.filters import PaginationIn
from core.apps.employee.filters.employee import EmployeeFilters
from core.apps.employee.models.employee import EmployeeModel
from core.apps.employee.services.employee import BaseEmployeeService


@pytest.mark.django_db
def test_get_employees_count_zero(employee_service: BaseEmployeeService):
    """Test employees count zero with no employees."""
    employees_count = employee_service.get_employee_count(EmployeeFilters())
    assert employees_count == 0, f"{employees_count=}"


@pytest.mark.django_db
def test_get_employees_count_existing_employees(employee_service: BaseEmployeeService):
    """Test employees count with existing employees."""
    expected_count = 5
    EmployeeModelFactory.create_batch(size=expected_count)

    employees_count = employee_service.get_employee_count(EmployeeFilters())
    assert employees_count == expected_count, f"{employees_count=}"


@pytest.mark.django_db
def test_get_employees_all(employee_service: BaseEmployeeService):
    """Test get all employees."""
    expected_count = 5
    employees = EmployeeModelFactory.create_batch(size=expected_count)

    employees_ids = {employee.id for employee in employees}

    fetched_employees = employee_service.get_employee_list(
        EmployeeFilters(),
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}

    assert len(fetched_employees_ids) == expected_count, f"{fetched_employees_ids=}"
    assert fetched_employees_ids == employees_ids, f"{fetched_employees_ids=}"


@pytest.mark.django_db
def test_get_employees_filter_by_last_name(employee_service: BaseEmployeeService):
    """Test filter employees by last name."""
    # Создаём сотрудников с разными фамилиями
    employee1 = EmployeeModelFactory(last_name="Иванов")
    employee2 = EmployeeModelFactory(last_name="Петров")
    employee3 = EmployeeModelFactory(last_name="Сидоров")
    employee4 = EmployeeModelFactory(
        last_name="Иванова",
    )  # Должен попасть, т.к. фильтр использует icontains

    # Фильтруем по фамилии "Иванов" (частичное совпадение)
    filters = EmployeeFilters(last_name="Иванов")
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id in fetched_employees_ids
    assert employee4.id in fetched_employees_ids  # "Иванова" содержит "Иванов"
    assert employee2.id not in fetched_employees_ids
    assert employee3.id not in fetched_employees_ids
    assert len(fetched_employees_ids) == 2


@pytest.mark.django_db
def test_get_employees_filter_by_position(employee_service: BaseEmployeeService):
    """Test filter employees by position."""
    employee1 = EmployeeModelFactory(position="Разработчик")
    employee2 = EmployeeModelFactory(position="Менеджер")
    employee3 = EmployeeModelFactory(position="Дизайнер")

    # Фильтруем по должности "Разработчик"
    filters = EmployeeFilters(position="Разработчик")
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id in fetched_employees_ids
    assert employee2.id not in fetched_employees_ids
    assert employee3.id not in fetched_employees_ids
    assert len(fetched_employees_ids) == 1


@pytest.mark.django_db
def test_get_employees_filter_by_search(employee_service: BaseEmployeeService):
    """Test filter employees by search query."""
    employee1 = EmployeeModelFactory(
        first_name="Иван",
        last_name="Иванов",
        position="Разработчик",
    )
    employee2 = EmployeeModelFactory(
        first_name="Петр",
        last_name="Петров",
        position="Менеджер",
    )
    employee3 = EmployeeModelFactory(
        first_name="Сидор",
        last_name="Сидоров",
        position="Дизайнер",
    )

    # Поиск по "Иван" должен найти сотрудника по имени или фамилии
    filters = EmployeeFilters(search="Иван")
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id in fetched_employees_ids
    assert employee2.id not in fetched_employees_ids
    assert employee3.id not in fetched_employees_ids
    assert len(fetched_employees_ids) == 1


@pytest.mark.django_db
def test_get_employees_no_matches(employee_service: BaseEmployeeService):
    """Test filter employees with no matches."""
    EmployeeModelFactory.create_batch(size=3)

    # Фильтр, который не должен найти ни одного сотрудника
    filters = EmployeeFilters(last_name="НесуществующаяФамилия")
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    assert len(list(fetched_employees)) == 0


@pytest.mark.django_db
def test_get_employees_pagination(employee_service: BaseEmployeeService):
    """Test pagination for employees."""
    expected_count = 10
    EmployeeModelFactory.create_batch(size=expected_count)

    # Первая страница (первые 5)
    pagination = PaginationIn(offset=0, limit=5)
    fetched_employees = employee_service.get_employee_list(
        EmployeeFilters(),
        pagination,
    )

    assert len(list(fetched_employees)) == 5

    # Вторая страница (следующие 5)
    pagination = PaginationIn(offset=5, limit=5)
    fetched_employees = employee_service.get_employee_list(
        EmployeeFilters(),
        pagination,
    )

    assert len(list(fetched_employees)) == 5


@pytest.mark.django_db
def test_get_employees_filter_by_id(employee_service: BaseEmployeeService):
    """Test filter employees by id."""
    employee1 = EmployeeModelFactory()
    employee2 = EmployeeModelFactory()
    employee3 = EmployeeModelFactory()

    filters = EmployeeFilters(id=employee1.id)
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id in fetched_employees_ids
    assert employee2.id not in fetched_employees_ids
    assert employee3.id not in fetched_employees_ids
    assert len(fetched_employees_ids) == 1


@pytest.mark.django_db
def test_get_employees_filter_by_ids(employee_service: BaseEmployeeService):
    """Test filter employees by list of ids."""
    employee1 = EmployeeModelFactory()
    employee2 = EmployeeModelFactory()
    employee3 = EmployeeModelFactory()
    employee4 = EmployeeModelFactory()

    filters = EmployeeFilters(ids=[employee1.id, employee3.id])
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id in fetched_employees_ids
    assert employee2.id not in fetched_employees_ids
    assert employee3.id in fetched_employees_ids
    assert employee4.id not in fetched_employees_ids
    assert len(fetched_employees_ids) == 2


@pytest.mark.django_db
def test_get_employees_filter_by_first_name(employee_service: BaseEmployeeService):
    """Test filter employees by first name."""
    employee1 = EmployeeModelFactory(first_name="Иван")
    employee2 = EmployeeModelFactory(first_name="Петр")
    employee3 = EmployeeModelFactory(first_name="Сидор")

    filters = EmployeeFilters(first_name="Иван")
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id in fetched_employees_ids
    assert employee2.id not in fetched_employees_ids
    assert employee3.id not in fetched_employees_ids
    assert len(fetched_employees_ids) == 1


@pytest.mark.django_db
def test_get_employees_filter_by_middle_name(employee_service: BaseEmployeeService):
    """Test filter employees by middle name."""
    employee1 = EmployeeModelFactory(middle_name="Иванович")
    employee2 = EmployeeModelFactory(middle_name="Петрович")
    employee3 = EmployeeModelFactory(middle_name="Сидорович")

    filters = EmployeeFilters(middle_name="Иванович")
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id in fetched_employees_ids
    assert employee2.id not in fetched_employees_ids
    assert employee3.id not in fetched_employees_ids
    assert len(fetched_employees_ids) == 1


@pytest.mark.django_db
def test_get_employees_filter_by_date_hired_from(employee_service: BaseEmployeeService):
    """Test filter employees by date_hired_from."""
    date1 = date(2020, 1, 1)
    date2 = date(2021, 1, 1)
    date3 = date(2022, 1, 1)

    employee1 = EmployeeModelFactory(date_hired=date1)
    employee2 = EmployeeModelFactory(date_hired=date2)
    employee3 = EmployeeModelFactory(date_hired=date3)

    # Фильтр: дата приёма >= 2021-01-01
    filters = EmployeeFilters(date_hired_from=date2)
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id not in fetched_employees_ids
    assert employee2.id in fetched_employees_ids
    assert employee3.id in fetched_employees_ids
    assert len(fetched_employees_ids) == 2


@pytest.mark.django_db
def test_get_employees_filter_by_date_hired_to(employee_service: BaseEmployeeService):
    """Test filter employees by date_hired_to."""
    date1 = date(2020, 1, 1)
    date2 = date(2021, 1, 1)
    date3 = date(2022, 1, 1)

    employee1 = EmployeeModelFactory(date_hired=date1)
    employee2 = EmployeeModelFactory(date_hired=date2)
    employee3 = EmployeeModelFactory(date_hired=date3)

    # Фильтр: дата приёма <= 2021-01-01
    filters = EmployeeFilters(date_hired_to=date2)
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id in fetched_employees_ids
    assert employee2.id in fetched_employees_ids
    assert employee3.id not in fetched_employees_ids
    assert len(fetched_employees_ids) == 2


@pytest.mark.django_db
def test_get_employees_filter_by_date_hired_range(
    employee_service: BaseEmployeeService,
):
    """Test filter employees by date_hired range."""
    date1 = date(2020, 1, 1)
    date2 = date(2021, 1, 1)
    date3 = date(2022, 1, 1)
    date4 = date(2023, 1, 1)

    employee1 = EmployeeModelFactory(date_hired=date1)
    employee2 = EmployeeModelFactory(date_hired=date2)
    employee3 = EmployeeModelFactory(date_hired=date3)
    employee4 = EmployeeModelFactory(date_hired=date4)

    # Фильтр: дата приёма от 2021-01-01 до 2022-01-01
    filters = EmployeeFilters(date_hired_from=date2, date_hired_to=date3)
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id not in fetched_employees_ids
    assert employee2.id in fetched_employees_ids
    assert employee3.id in fetched_employees_ids
    assert employee4.id not in fetched_employees_ids
    assert len(fetched_employees_ids) == 2


@pytest.mark.django_db
def test_get_employees_filter_by_salary_min(employee_service: BaseEmployeeService):
    """Test filter employees by salary_min."""
    employee1 = EmployeeModelFactory(salary=50000)
    employee2 = EmployeeModelFactory(salary=75000)
    employee3 = EmployeeModelFactory(salary=100000)

    # Фильтр: зарплата >= 75000
    filters = EmployeeFilters(salary_min=75000)
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id not in fetched_employees_ids
    assert employee2.id in fetched_employees_ids
    assert employee3.id in fetched_employees_ids
    assert len(fetched_employees_ids) == 2


@pytest.mark.django_db
def test_get_employees_filter_by_salary_max(employee_service: BaseEmployeeService):
    """Test filter employees by salary_max."""
    employee1 = EmployeeModelFactory(salary=50000)
    employee2 = EmployeeModelFactory(salary=75000)
    employee3 = EmployeeModelFactory(salary=100000)

    # Фильтр: зарплата <= 75000
    filters = EmployeeFilters(salary_max=75000)
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id in fetched_employees_ids
    assert employee2.id in fetched_employees_ids
    assert employee3.id not in fetched_employees_ids
    assert len(fetched_employees_ids) == 2


@pytest.mark.django_db
def test_get_employees_filter_by_salary_range(employee_service: BaseEmployeeService):
    """Test filter employees by salary range."""
    employee1 = EmployeeModelFactory(salary=50000)
    employee2 = EmployeeModelFactory(salary=75000)
    employee3 = EmployeeModelFactory(salary=100000)
    employee4 = EmployeeModelFactory(salary=125000)

    # Фильтр: зарплата от 75000 до 100000
    filters = EmployeeFilters(salary_min=75000, salary_max=100000)
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id not in fetched_employees_ids
    assert employee2.id in fetched_employees_ids
    assert employee3.id in fetched_employees_ids
    assert employee4.id not in fetched_employees_ids
    assert len(fetched_employees_ids) == 2


@pytest.mark.django_db
def test_get_employees_filter_by_manager_id(employee_service: BaseEmployeeService):
    """Test filter employees by manager_id."""
    manager = EmployeeModelFactory()
    employee1 = EmployeeModelFactory(manager=manager)
    employee2 = EmployeeModelFactory(manager=manager)
    employee3 = EmployeeModelFactory()  # Без менеджера

    filters = EmployeeFilters(manager_id=manager.id)
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id in fetched_employees_ids
    assert employee2.id in fetched_employees_ids
    assert employee3.id not in fetched_employees_ids
    assert manager.id not in fetched_employees_ids
    assert len(fetched_employees_ids) == 2


@pytest.mark.django_db
def test_get_employees_filter_by_created_at_from(employee_service: BaseEmployeeService):
    """Test filter employees by created_at_from."""
    now = timezone.now()
    employee1 = EmployeeModelFactory()
    # Обновляем created_at напрямую через модель
    EmployeeModel.objects.filter(id=employee1.id).update(
        created_at=now - timedelta(days=3),
    )

    employee2 = EmployeeModelFactory()
    EmployeeModel.objects.filter(id=employee2.id).update(
        created_at=now - timedelta(days=1),
    )

    employee3 = EmployeeModelFactory()
    EmployeeModel.objects.filter(id=employee3.id).update(created_at=now)

    # Фильтр: created_at >= now - 2 days
    filters = EmployeeFilters(created_at_from=now - timedelta(days=2))
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id not in fetched_employees_ids
    assert employee2.id in fetched_employees_ids
    assert employee3.id in fetched_employees_ids
    assert len(fetched_employees_ids) == 2


@pytest.mark.django_db
def test_get_employees_filter_by_created_at_to(employee_service: BaseEmployeeService):
    """Test filter employees by created_at_to."""
    now = timezone.now()
    employee1 = EmployeeModelFactory()
    EmployeeModel.objects.filter(id=employee1.id).update(
        created_at=now - timedelta(days=3),
    )

    employee2 = EmployeeModelFactory()
    EmployeeModel.objects.filter(id=employee2.id).update(
        created_at=now - timedelta(days=1),
    )

    employee3 = EmployeeModelFactory()
    EmployeeModel.objects.filter(id=employee3.id).update(created_at=now)

    # Фильтр: created_at <= now - 2 days
    filters = EmployeeFilters(created_at_to=now - timedelta(days=2))
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id in fetched_employees_ids
    assert employee2.id not in fetched_employees_ids
    assert employee3.id not in fetched_employees_ids
    assert len(fetched_employees_ids) == 1


@pytest.mark.django_db
def test_get_employees_filter_by_updated_at_from(employee_service: BaseEmployeeService):
    """Test filter employees by updated_at_from."""
    now = timezone.now()
    employee1 = EmployeeModelFactory()
    EmployeeModel.objects.filter(id=employee1.id).update(
        updated_at=now - timedelta(days=3),
    )

    employee2 = EmployeeModelFactory()
    EmployeeModel.objects.filter(id=employee2.id).update(
        updated_at=now - timedelta(days=1),
    )

    employee3 = EmployeeModelFactory()
    EmployeeModel.objects.filter(id=employee3.id).update(updated_at=now)

    # Фильтр: updated_at >= now - 2 days
    filters = EmployeeFilters(updated_at_from=now - timedelta(days=2))
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id not in fetched_employees_ids
    assert employee2.id in fetched_employees_ids
    assert employee3.id in fetched_employees_ids
    assert len(fetched_employees_ids) == 2


@pytest.mark.django_db
def test_get_employees_filter_by_updated_at_to(employee_service: BaseEmployeeService):
    """Test filter employees by updated_at_to."""
    now = timezone.now()
    employee1 = EmployeeModelFactory()
    EmployeeModel.objects.filter(id=employee1.id).update(
        updated_at=now - timedelta(days=3),
    )

    employee2 = EmployeeModelFactory()
    EmployeeModel.objects.filter(id=employee2.id).update(
        updated_at=now - timedelta(days=1),
    )

    employee3 = EmployeeModelFactory()
    EmployeeModel.objects.filter(id=employee3.id).update(updated_at=now)

    # Фильтр: updated_at <= now - 2 days
    filters = EmployeeFilters(updated_at_to=now - timedelta(days=2))
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id in fetched_employees_ids
    assert employee2.id not in fetched_employees_ids
    assert employee3.id not in fetched_employees_ids
    assert len(fetched_employees_ids) == 1


@pytest.mark.django_db
def test_get_employees_filter_combined(employee_service: BaseEmployeeService):
    """Test combined filters."""
    manager = EmployeeModelFactory()
    employee1 = EmployeeModelFactory(
        first_name="Иван",
        last_name="Иванов",
        position="Разработчик",
        salary=100000,
        manager=manager,
    )
    employee2 = EmployeeModelFactory(
        first_name="Петр",
        last_name="Петров",
        position="Менеджер",
        salary=150000,
        manager=manager,
    )
    employee3 = EmployeeModelFactory(
        first_name="Иван",
        last_name="Сидоров",
        position="Разработчик",
        salary=80000,
    )

    # Комбинированный фильтр: имя "Иван", должность "Разработчик", зарплата >= 90000
    filters = EmployeeFilters(
        first_name="Иван",
        position="Разработчик",
        salary_min=90000,
    )
    fetched_employees = employee_service.get_employee_list(
        filters,
        PaginationIn(),
    )

    fetched_employees_ids = {employee.id for employee in fetched_employees}
    assert employee1.id in fetched_employees_ids
    assert employee2.id not in fetched_employees_ids
    assert employee3.id not in fetched_employees_ids
    assert len(fetched_employees_ids) == 1
