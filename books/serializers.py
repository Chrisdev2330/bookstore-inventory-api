"""
Serializers para la API de libros.

Define cómo se serializan y deserializan los datos del modelo Book.
"""

from rest_framework import serializers
from .models import Book
import re


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer principal para el modelo Book.
    
    Maneja la serialización para operaciones CRUD básicas.
    Incluye validaciones personalizadas para ISBN y otros campos.
    """
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'isbn',
            'cost_usd',
            'selling_price_local',
            'stock_quantity',
            'category',
            'supplier_country',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_isbn(self, value):
        """
        Valida el formato del ISBN y verifica duplicados.
        """
        # Limpiamos el ISBN
        clean_isbn = re.sub(r'[-\s]', '', value)
        
        # Validamos longitud
        if len(clean_isbn) not in [10, 13]:
            raise serializers.ValidationError(
                'ISBN debe tener 10 o 13 dígitos.'
            )
        
        # Validamos que sean dígitos (o X al final para ISBN-10)
        if len(clean_isbn) == 10:
            if not clean_isbn[:9].isdigit():
                raise serializers.ValidationError('ISBN-10 inválido.')
            if not (clean_isbn[9].isdigit() or clean_isbn[9].upper() == 'X'):
                raise serializers.ValidationError('ISBN-10 inválido.')
        else:
            if not clean_isbn.isdigit():
                raise serializers.ValidationError('ISBN-13 debe contener solo dígitos.')
        
        # Verificamos duplicados (excluyendo el registro actual en updates)
        instance = getattr(self, 'instance', None)
        if instance:
            # Es un update, excluimos el registro actual
            exists = Book.objects.exclude(pk=instance.pk).filter(isbn=value).exists()
        else:
            # Es un create
            exists = Book.objects.filter(isbn=value).exists()
        
        if exists:
            raise serializers.ValidationError(
                'Ya existe un libro con este ISBN.'
            )
        
        return value
    
    def validate_cost_usd(self, value):
        """
        Valida que el costo sea mayor a 0.
        """
        if value <= 0:
            raise serializers.ValidationError(
                'El costo debe ser mayor a 0.'
            )
        return value
    
    def validate_stock_quantity(self, value):
        """
        Valida que el stock no sea negativo.
        """
        if value < 0:
            raise serializers.ValidationError(
                'El stock no puede ser negativo.'
            )
        return value
    
    def validate_supplier_country(self, value):
        """
        Valida el código de país del proveedor.
        """
        if len(value) != 2:
            raise serializers.ValidationError(
                'El código de país debe tener 2 caracteres.'
            )
        return value.upper()


class BookListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listados de libros.
    
    Muestra menos campos para mejorar el rendimiento en listados.
    """
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'isbn',
            'cost_usd',
            'selling_price_local',
            'stock_quantity',
            'category',
        ]


class PriceCalculationSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    cost_usd = serializers.DecimalField(max_digits=10, decimal_places=2)
    exchange_rate = serializers.FloatField()
    cost_local = serializers.DecimalField(max_digits=10, decimal_places=2)
    margin_percentage = serializers.IntegerField()
    selling_price_local = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()
    calculation_timestamp = serializers.DateTimeField()
