from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views


schema_view = get_schema_view(
   openapi.Info(
      title="intizar API",
      default_version='v1',
      description="Documentation for project intizar",
      contact=openapi.Contact(email="dontWriteME@intizar.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('swagger(?P<format>\.json|\.yaml)',
         schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
