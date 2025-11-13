from django.http import HttpRequest
from ninja import (
    Query,
    Router,
)

from core.api.filters import (
    PaginationIn,
    PaginationOut,
)
from core.api.schemas import (
    ApiResponse,
    ListPaginatedResponse,
)
from core.api.v1.employees.schemas import EmployeeSchema
from core.apps.employee.filters.employee import EmployeeFilters
from core.apps.employee.services.employee import (
    BaseEmployeeService,
    ORMEmployeeService,
)


router = Router(tags=["employees"])


@router.get("", response=ApiResponse[ListPaginatedResponse[EmployeeSchema]])
def get_employees_list_handler(
    request: HttpRequest,
    filters: Query[EmployeeFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[EmployeeSchema]]:
    service: BaseEmployeeService = ORMEmployeeService()
    employee_list = service.get_employee_list(filters=filters, pagination=pagination_in)
    employee_count = service.get_employee_count(filters=filters)

    items = [EmployeeSchema.from_entity(employee) for employee in employee_list]

    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=employee_count,
    )

    return ApiResponse[ListPaginatedResponse[EmployeeSchema]](
        data=ListPaginatedResponse[EmployeeSchema](
            items=items,
            pagination=pagination_out,
        ),
    )
