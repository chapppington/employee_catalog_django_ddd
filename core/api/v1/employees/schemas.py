from datetime import datetime

from ninja import Schema


class EmployeeSchema(Schema):
    id: int
    full_name: str
    position: str
    date_hired: datetime
    salary: float
    manager: int | None
    created_at: datetime
    updated_at: datetime | None = None


EmployeeListSchema = list[EmployeeSchema]
