from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import (
    RegistrationView, UserViewSet,
    SpinViewSet, SymbolViewSet
)

router = DefaultRouter()
router.register(r'spins', SpinViewSet, basename='spin')
router.register(r'symbols', SymbolViewSet, basename='symbol')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistrationView.as_view(), name='register'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]