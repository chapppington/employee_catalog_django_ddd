from django.http import HttpRequest
from django.urls import path
from ninja import NinjaAPI

from core.api.schemas import PingResponseSchema
from core.api.v1.urls import router as v1_router


api = NinjaAPI(
    title="Django Example API",
    description="API for Django Example Project",
    version="1.0.0",
)


@api.get("/ping", response=PingResponseSchema)
def ping(request: HttpRequest) -> PingResponseSchema:
    return PingResponseSchema(response=True)


api.add_router("v1/", v1_router)


urlpatterns = [
    path("", api.urls),
]
