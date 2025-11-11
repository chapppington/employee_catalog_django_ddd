from datetime import datetime

from django.http import HttpRequest
from ninja import Router

from core.api.v1.employees.schemas import EmployeeSchema


router = Router(tags=["employees"])


@router.get("", response=EmployeeSchema)
def get_employees_list_handler(request: HttpRequest) -> EmployeeSchema:
    return EmployeeSchema(
        id=1,
        full_name="John Doe",
        position="Software Engineer",
        date_hired=datetime.now(),
        salary=100000,
        manager=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
