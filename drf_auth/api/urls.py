from django.contrib import admin
from django.urls import path
from django.urls import include
from .views import AuthStatusView

app_name = 'api'


urlpatterns = [
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/auth/status/', AuthStatusView.as_view(), name='auth-status')
]
