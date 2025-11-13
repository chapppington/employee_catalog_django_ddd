import pytest

from core.apps.employee.services.employee import (
    BaseEmployeeService,
    ORMEmployeeService,
)


@pytest.fixture
def employee_service() -> BaseEmployeeService:
    return ORMEmployeeService()
