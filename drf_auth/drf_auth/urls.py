from django.contrib import admin
from django.urls import path
from django.urls import include
from user.views import AuthStatusView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/status/', AuthStatusView.as_view(), name='auth-status')
]
