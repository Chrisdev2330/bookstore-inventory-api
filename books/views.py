from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Book
from .serializers import (
    BookSerializer,
    BookListSerializer,
    PriceCalculationSerializer
)
from .services import PriceCalculationService

import logging

logger = logging.getLogger(__name__)


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de libros.
    
    Proporciona las acciones:
    - list: GET /books/
    - create: POST /books/
    - retrieve: GET /books/{id}/
    - update: PUT /books/{id}/
    - partial_update: PATCH /books/{id}/
    - destroy: DELETE /books/{id}/
    
    También incluye acciones personalizadas para búsqueda y stock bajo.
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Libro creado: {serializer.data.get('title')}")
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        # Si hay errores de validación, los retornamos
        logger.warning(f"Error al crear libro: {serializer.errors}")
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def update(self, request, *args, **kwargs):
    
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Libro actualizado: {instance.id}")
            return Response(serializer.data)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def destroy(self, request, *args, **kwargs):
    
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        
        logger.info(f"Libro eliminado: {book_title}")
        return Response(
            {'message': f'Libro "{book_title}" eliminado correctamente.'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'], url_path='search')
    def search_by_category(self, request):
        
        category = request.query_params.get('category', None)
        
        if not category:
            return Response(
                {'error': 'El parámetro "category" es requerido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Búsqueda case-insensitive
        books = Book.objects.filter(category__icontains=category)
        
        if not books.exists():
            return Response(
                {'message': f'No se encontraron libros en la categoría "{category}".'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = BookListSerializer(books, many=True)
        return Response({
            'category': category,
            'count': books.count(),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock(self, request):
       
        try:
            threshold = int(request.query_params.get('threshold', 10))
        except ValueError:
            return Response(
                {'error': 'El threshold debe ser un número entero.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if threshold < 0:
            return Response(
                {'error': 'El threshold no puede ser negativo.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        books = Book.objects.filter(stock_quantity__lte=threshold)
        serializer = BookListSerializer(books, many=True)
        
        return Response({
            'threshold': threshold,
            'count': books.count(),
            'results': serializer.data
        })


class CalculatePriceView(APIView):
  
    
    def post(self, request, book_id):

        # Buscamos el libro
        book = get_object_or_404(Book, pk=book_id)
        
        # Obtenemos la moneda objetivo si se especifica
        target_currency = request.query_params.get('currency', None)
        
        try:
            # Usamos el servicio para calcular el precio
            price_service = PriceCalculationService()
            result = price_service.calculate_selling_price(
                book,
                target_currency=target_currency
            )
            
            # Serializamos la respuesta
            serializer = PriceCalculationSerializer(result)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            # Si hay algún error inesperado, lo manejamos
            logger.error(f"Error al calcular precio: {str(e)}")
            
            return Response(
                {
                    'error': 'Error al calcular el precio.',
                    'detail': str(e)
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class BookStatsView(APIView):
 
    def get(self, request):
        
        #Obtiene estadísticas generales del inventario.
        
        from django.db.models import Sum, Avg, Count
        
        stats = Book.objects.aggregate(
            total_books=Count('id'),
            total_stock=Sum('stock_quantity'),
            avg_cost_usd=Avg('cost_usd'),
            books_with_price=Count('id', filter=models.Q(selling_price_local__isnull=False))
        )
        
        # Contamos libros por categoría
        categories = Book.objects.values('category').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        return Response({
            'total_books': stats['total_books'] or 0,
            'total_stock_units': stats['total_stock'] or 0,
            'average_cost_usd': round(stats['avg_cost_usd'] or 0, 2),
            'books_with_calculated_price': stats['books_with_price'] or 0,
            'top_categories': list(categories)
        })


# Importamos models para la vista de stats
from django.db import models
