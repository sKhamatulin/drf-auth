from django.urls import path, include
from .views import AuthStatusView, UserViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/auth/status/',
         AuthStatusView.as_view(),
         name='auth-status'),
    path('v1/auth/me/',
         UserViewSet.as_view({'get': 'retrieve'}),
         name='user-me'),
    path('', include(router.urls)),
]
