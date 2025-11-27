"""
Tests para la aplicación de libros.

Incluye tests para el modelo, serializers y endpoints.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal

from .models import Book
from .serializers import BookSerializer


class BookModelTest(TestCase): 
    def setUp(self):
        #Configuración inicial para los tests
        self.book_data = {
            'title': 'El Quijote',
            'author': 'Miguel de Cervantes',
            'isbn': '978-84-376-0494-7',
            'cost_usd': Decimal('15.99'),
            'stock_quantity': 25,
            'category': 'Literatura Clásica',
            'supplier_country': 'ES',
        }
    
    def test_create_book(self):
        #Test: Crear un libro correctamente
        book = Book.objects.create(**self.book_data)
        
        self.assertEqual(book.title, 'El Quijote')
        self.assertEqual(book.author, 'Miguel de Cervantes')
        self.assertIsNotNone(book.created_at)
    
    def test_isbn_unique(self):
        #Test: No permitir ISBN duplicado
        Book.objects.create(**self.book_data)
        
        with self.assertRaises(Exception):
            Book.objects.create(**self.book_data)
    
    def test_cost_must_be_positive(self):
        #Test: El costo debe ser mayor a 0
        self.book_data['cost_usd'] = Decimal('-10.00')
        
        with self.assertRaises(Exception):
            Book.objects.create(**self.book_data)
    
    def test_stock_cannot_be_negative(self):
        #Test: El stock no puede ser negativo
        # PositiveIntegerField ya maneja esto
        self.book_data['stock_quantity'] = -5
        
        with self.assertRaises(Exception):
            Book.objects.create(**self.book_data)


class BookAPITest(APITestCase):
    
    #Tests para los endpoints de la API.
    
    
    def setUp(self):
        #Configuración inicial
        self.book = Book.objects.create(
            title='Cien años de soledad',
            author='Gabriel García Márquez',
            isbn='9780060883287',
            cost_usd=Decimal('12.50'),
            stock_quantity=15,
            category='Realismo Mágico',
            supplier_country='CO',
        )
        
        self.valid_book_data = {
            'title': 'Don Quijote',
            'author': 'Miguel de Cervantes',
            'isbn': '9788420412146',
            'cost_usd': '18.99',
            'stock_quantity': 30,
            'category': 'Clásicos',
            'supplier_country': 'ES',
        }
    
    def test_list_books(self):
        #Test: Listar todos los libros
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_book(self):
        #Test: Crear un libro via API
        url = reverse('book-list')
        response = self.client.post(url, self.valid_book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_retrieve_book(self):
        #Test: Obtener un libro por ID.
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Cien años de soledad')
    
    def test_update_book(self):
        #Test: Actualizar un libro
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        update_data = {'title': 'Cien años de soledad (Edición especial)'}
        
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertIn('Edición especial', self.book.title)
    
    def test_delete_book(self):
        #Test: Eliminar un libro
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.count(), 0)
    
    def test_search_by_category(self):
        #Test: Buscar libros por categoría
        url = reverse('book-search-by-category')
        response = self.client.get(url, {'category': 'Realismo'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_low_stock(self):
        #Test: Obtener libros con stock bajo
        url = reverse('book-low-stock')
        response = self.client.get(url, {'threshold': 20})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_duplicate_isbn_rejected(self):
        #Test: Rechazar ISBN duplicado
        url = reverse('book-list')
        duplicate_data = self.valid_book_data.copy()
        duplicate_data['isbn'] = self.book.isbn  # ISBN ya existente
        
        response = self.client.post(url, duplicate_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PriceCalculationTest(APITestCase):
    
    #Tests para el cálculo de precios.
    
    
    def setUp(self):
        #Configuración inicial
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890',
            cost_usd=Decimal('10.00'),
            stock_quantity=5,
            category='Test',
            supplier_country='US',
        )
    
    def test_calculate_price_endpoint(self):
        #Test: Endpoint de cálculo de precio
        url = reverse('calculate-price', kwargs={'book_id': self.book.id})
        response = self.client.post(url)
        
        # El endpoint debe responder correctamente
        # (puede ser 200 o 503 si la API externa falla)
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_503_SERVICE_UNAVAILABLE]
        )
    
    def test_calculate_price_book_not_found(self):
        #Test: Error 404 si el libro no existe
        url = reverse('calculate-price', kwargs={'book_id': 99999})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
