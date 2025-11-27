import requests
import logging
from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.utils import timezone

# Logger para este módulo
logger = logging.getLogger(__name__)


class ExchangeRateService:
    
    # URL de la API de tasas de cambio
    API_URL = 'https://api.exchangerate-api.com/v4/latest/USD'
    
    # Timeout para las peticiones (en segundos)
    REQUEST_TIMEOUT = 10
    
    def __init__(self):
        self.default_rate = settings.DEFAULT_EXCHANGE_RATE
        self.default_currency = settings.DEFAULT_CURRENCY
    
    def get_exchange_rate(self, target_currency=None):
        
        currency = target_currency or self.default_currency
        
        try:
            logger.info(f"Consultando tasa de cambio USD -> {currency}")
            
            response = requests.get(
                self.API_URL,
                timeout=self.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            rates = data.get('rates', {})
            
            if currency in rates:
                rate = rates[currency]
                logger.info(f"Tasa obtenida: 1 USD = {rate} {currency}")
                return (rate, currency, True)
            else:
                # La moneda no está en la respuesta
                logger.warning(
                    f"Moneda {currency} no encontrada. Usando tasa por defecto."
                )
                return (self.default_rate, self.default_currency, False)
                
        except requests.exceptions.Timeout:
            logger.error("Timeout al consultar API de tasas de cambio")
            return (self.default_rate, self.default_currency, False)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al consultar API: {str(e)}")
            return (self.default_rate, self.default_currency, False)
            
        except (KeyError, ValueError) as e:
            logger.error(f"Error al parsear respuesta de API: {str(e)}")
            return (self.default_rate, self.default_currency, False)


class PriceCalculationService:
    
    def __init__(self):
        self.exchange_service = ExchangeRateService()
        self.profit_margin = settings.PROFIT_MARGIN
    
    def calculate_selling_price(self, book, target_currency=None):
        # Obtenemos la tasa de cambio
        exchange_rate, currency, is_live_rate = self.exchange_service.get_exchange_rate(
            target_currency
        )
        
        # Convertimos a Decimal para precisión en cálculos monetarios
        cost_usd = Decimal(str(book.cost_usd))
        rate = Decimal(str(exchange_rate))
        margin = Decimal(str(self.profit_margin)) / Decimal('100')
        
        # Calculamos el costo en moneda local
        cost_local = cost_usd * rate
        
        # Aplicamos el margen de ganancia (40%)
        # Fórmula: precio_venta = costo_local * (1 + margen)
        selling_price = cost_local * (Decimal('1') + margin)
        
        # Redondeamos a 2 decimales
        cost_local = cost_local.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        selling_price = selling_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Actualizamos el libro en la base de datos
        book.selling_price_local = selling_price
        book.save(update_fields=['selling_price_local', 'updated_at'])
        
        # Preparamos la respuesta
        calculation_result = {
            'book_id': book.id,
            'cost_usd': cost_usd,
            'exchange_rate': float(exchange_rate),
            'cost_local': cost_local,
            'margin_percentage': self.profit_margin,
            'selling_price_local': selling_price,
            'currency': currency,
            'calculation_timestamp': timezone.now(),
            'is_live_rate': is_live_rate,  # Info adicional útil
        }
        
        logger.info(
            f"Precio calculado para libro {book.id}: "
            f"{selling_price} {currency} (margen: {self.profit_margin}%)"
        )
        
        return calculation_result
