from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import (
    SpinViewSet, SymbolViewSet
)

router = DefaultRouter()
router.register(r'spins', SpinViewSet, basename='spin')
router.register(r'symbols', SymbolViewSet, basename='symbol')

urlpatterns = [
    path('', include(router.urls)),
]