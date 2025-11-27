from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    return JsonResponse({
        'message': 'Bienvenido a la API de Inventario de Librería',
        'version': '1.0.0',
        'endpoints': {
            'books': '/api/books/',
            'admin': '/admin/',
        }
    })


urlpatterns = [
    # Vista raíz
    path('', api_root, name='api-root'),
    
    # Panel de administración de Django
    path('admin/', admin.site.urls),
    
    # Rutas de la aplicación de libros
    path('api/', include('books.urls')),
]
