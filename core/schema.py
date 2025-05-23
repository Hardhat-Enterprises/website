from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Hardhat Website API",
        default_version="v1",
        description="API documentation for the Hardhat Website",
        terms_of_service="https://www.hardhatenterprises.com/terms/",
        contact=openapi.Contact(email="support@hardhatenterprises.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
