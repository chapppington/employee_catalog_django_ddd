from ninja import Router

from core.api.v1.employees.handlers import router as employees_router


router = Router(tags=["v1"])


router.add_router("employees/", employees_router)
