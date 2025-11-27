from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    BookViewSet,
    CalculatePriceView,
    BookStatsView,
)

# Creamos el router para el ViewSet
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    # Rutas del ViewSet (CRUD + acciones personalizadas)
    path('', include(router.urls)),
    
    # Endpoint para calcular precio (APIView)
    path(
        'books/<int:book_id>/calculate-price/',
        CalculatePriceView.as_view(),
        name='calculate-price'
    ),
    
    # Endpoint de estadísticas (bonus)
    path(
        'books/stats/',
        BookStatsView.as_view(),
        name='book-stats'
    ),
]
