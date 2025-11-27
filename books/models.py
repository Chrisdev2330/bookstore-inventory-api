from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import re

def validate_isbn(value):
    # Quitamos guiones y espacios para validar
    clean_isbn = re.sub(r'[-\s]', '', value)
    
    # ISBN-10: 9 dígitos + 1 dígito o X
    # ISBN-13: 13 dígitos
    if len(clean_isbn) == 10:
        # Los primeros 9 deben ser dígitos, el último puede ser X
        if not (clean_isbn[:9].isdigit() and (clean_isbn[9].isdigit() or clean_isbn[9].upper() == 'X')):
            raise ValidationError('ISBN-10 inválido. Debe tener 9 dígitos seguidos de un dígito o X.')
    elif len(clean_isbn) == 13:
        if not clean_isbn.isdigit():
            raise ValidationError('ISBN-13 inválido. Debe contener solo dígitos.')
    else:
        raise ValidationError('ISBN debe tener 10 o 13 dígitos.')


class Book(models.Model):
    """
    
    Campos:
        - title: Título del libro
        - author: Autor del libro
        - isbn: Código ISBN único (10 o 13 dígitos)
        - cost_usd: Costo del libro en dólares americanos
        - selling_price_local: Precio de venta en moneda local (calculado)
        - stock_quantity: Cantidad disponible en inventario
        - category: Categoría del libro
        - supplier_country: País del proveedor (código ISO)
        - created_at: Fecha de creación del registro
        - updated_at: Última actualización del registro
    """
    
    # Campos principales
    title = models.CharField(
        max_length=255,
        verbose_name='Título',
        help_text='Título completo del libro'
    )
    
    author = models.CharField(
        max_length=255,
        verbose_name='Autor',
        help_text='Nombre del autor o autores'
    )
    
    isbn = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_isbn],
        verbose_name='ISBN',
        help_text='Código ISBN del libro (10 o 13 dígitos)'
    )
    
    # Campos de precio
    cost_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, message='El costo debe ser mayor a 0')],
        verbose_name='Costo en USD',
        help_text='Costo de adquisición en dólares americanos'
    )
    
    selling_price_local = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Precio de venta local',
        help_text='Precio de venta calculado en moneda local'
    )
    
    # Inventario
    stock_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='Cantidad en stock',
        help_text='Unidades disponibles en inventario'
    )
    
    # Clasificación
    category = models.CharField(
        max_length=100,
        verbose_name='Categoría',
        help_text='Categoría o género del libro'
    )
    
    supplier_country = models.CharField(
        max_length=2,
        verbose_name='País del proveedor',
        help_text='Código ISO de 2 letras del país proveedor'
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )
    
    class Meta:
        db_table = 'books'
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.author}"
    
    def clean(self):

        super().clean()
        
        # Aseguramos que el costo sea positivo
        if self.cost_usd is not None and self.cost_usd <= 0:
            raise ValidationError({'cost_usd': 'El costo debe ser mayor a 0.'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
