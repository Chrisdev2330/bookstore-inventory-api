# 📚 Bookstore Inventory API

API REST para sistema de gestión de inventario de librerías con validación de precios en tiempo real.

---

## 📋 Tabla de Contenidos

1. [Descripción del Proyecto](#-descripción-del-proyecto)
2. [Stack Tecnológico](#️-stack-tecnológico)
3. [Estructura del Proyecto](#-estructura-del-proyecto)
4. [Instalación y Ejecución con Docker](#-instalación-y-ejecución-con-docker)
5. [Instalación sin Docker](#-instalación-sin-docker-opcional)
6. [Endpoints de la API](#-endpoints-de-la-api)
7. [Ejemplos de Uso con cURL](#-ejemplos-de-uso-con-curl)
8. [Ejemplos de Uso con Postman](#-ejemplos-de-uso-con-postman)
9. [Reglas de Negocio](#-reglas-de-negocio)
10. [Comandos Docker Útiles](#-comandos-docker-útiles)
11. [Solución de Problemas](#-solución-de-problemas)
12. [Tests](#-tests)
13. [Configuración de Variables de Entorno](#️-configuración-de-variables-de-entorno)
14. [Credenciales por Defecto](#-credenciales-por-defecto)

---

## 🎯 Descripción del Proyecto

Este proyecto implementa una API REST completa que permite:

- ✅ Gestionar el inventario de libros (CRUD completo)
- ✅ Validar precios contra tasas de cambio actuales usando API externa
- ✅ Calcular precios de venta sugeridos con margen de ganancia del 40%
- ✅ Buscar libros por categoría
- ✅ Filtrar libros con stock bajo
- ✅ Validación de ISBN (10 y 13 dígitos)
- ✅ Manejo de errores HTTP apropiados (400, 404, 500, 503)

---

## 🛠️ Stack Tecnológico

| Tecnología | Versión | Descripción |
|------------|---------|-------------|
| Python | 3.11 | Lenguaje de programación |
| Django | 4.2.7 | Framework web |
| Django REST Framework | 3.14.0 | API REST |
| MySQL | 8.0 | Base de datos |
| Docker | Latest | Contenedores |
| Docker Compose | 3.8 | Orquestación |

---

## 📁 Estructura del Proyecto

```
bookstore-inventory-api/
│
├── bookstore_project/              # Configuración principal de Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                 # Configuración (MySQL, DRF, etc.)
│   ├── urls.py                     # URLs principales
│   └── wsgi.py
│
├── books/                          # Aplicación de libros
│   ├── __init__.py
│   ├── admin.py                    # Configuración del admin
│   ├── apps.py                     # Configuración de la app
│   ├── models.py                   # Modelo Book
│   ├── serializers.py              # Serializers de DRF
│   ├── services.py                 # Lógica de negocio (Exchange API)
│   ├── tests.py                    # Tests unitarios
│   ├── urls.py                     # URLs de la API
│   └── views.py                    # ViewSet + APIView
│
├── .env                            # Variables de entorno
├── .env.example                    # Ejemplo de configuración
├── .gitignore                      # Archivos ignorados por Git
├── docker-compose.yml              # Orquestación de contenedores
├── Dockerfile                      # Imagen de la API
├── manage.py                       # CLI de Django
├── README.md                       # Este archivo
├── requirements.txt                # Dependencias de Python
└── Bookstore_API.postman_collection.json  # Colección de Postman
```

---

## 🐳 Instalación y Ejecución con Docker

### Requisitos Previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y **ejecutándose**
- Git (opcional, para clonar el repositorio)

### Paso 1: Clonar o Descargar el Proyecto

```bash
# Opción A: Clonar con Git
git clone <url-del-repositorio>
cd bookstore-inventory-api

# Opción B: Descargar ZIP y extraer
# Luego navegar a la carpeta del proyecto
cd bookstore-inventory-api
```

### Paso 2: Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env
```

> **Nota:** El archivo `.env` ya viene configurado para Docker. No necesitas modificar nada.

### Paso 3: Construir y Levantar los Contenedores

```bash
# Construir las imágenes y levantar los servicios
docker-compose up --build
```

Espera a que veas mensajes como:
```
bookstore_mysql  | ready for connections
bookstore_api    | Watching for file changes with StatReloader
```

### Paso 4: Ejecutar las Migraciones (¡IMPORTANTE!)

Abre una **nueva terminal** (sin cerrar la anterior) y ejecuta:

```bash
# Entrar al contenedor de la API
docker-compose exec web bash
```

Una vez dentro del contenedor, ejecuta:

```bash
# Crear las migraciones de la app books
python manage.py makemigrations books

# Aplicar todas las migraciones a la base de datos
python manage.py migrate

# Salir del contenedor
exit
```

### Paso 5: Crear Usuario Administrador (Panel Admin de Django)

Para acceder al panel de administración de Django, necesitas crear un superusuario:

```bash
# Entrar al contenedor
docker-compose exec web bash

# Crear superusuario
python manage.py createsuperuser
```

Te pedirá los siguientes datos (puedes usar estos valores de ejemplo):

```
Username (leave blank to use 'root'): admin
Email address: admin@bookstore.com
Password: admin123
Password (again): admin123
```

> **Nota:** Te mostrará una advertencia porque la contraseña es muy simple. Escribe `y` para confirmar.

```bash
# Salir del contenedor
exit
```

### Paso 6: Acceder a la Aplicación

| Recurso | URL | Credenciales |
|---------|-----|--------------|
| API de Libros | http://localhost:8000/api/books/ | No requiere |
| Panel Admin | http://localhost:8000/admin/ | admin / admin123 |
| Raíz de la API | http://localhost:8000/ | No requiere |

### 🎉 ¡Listo! La API está funcionando.

---

## 📝 Resumen Rápido (Todos los comandos juntos)

```bash
# 1. Levantar contenedores
docker-compose up --build

# 2. En OTRA terminal, ejecutar migraciones y crear admin
docker-compose exec web bash

# Dentro del contenedor:
python manage.py makemigrations books
python manage.py migrate
python manage.py createsuperuser
# Username: admin
# Email: admin@bookstore.com
# Password: admin123
exit

# 3. Acceder a:
# API: http://localhost:8000/api/books/
# Admin: http://localhost:8000/admin/ (admin / admin123)
```

---

## 💻 Instalación sin Docker (Opcional)

Si prefieres no usar Docker, sigue estos pasos:

### Requisitos Previos

- Python 3.11+
- MySQL 8.0
- pip

### Paso 1: Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Linux/Mac)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate
```

### Paso 2: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Configurar MySQL

Conecta a MySQL y ejecuta:

```sql
CREATE DATABASE bookstore_db;
CREATE USER 'bookstore_user'@'localhost' IDENTIFIED BY 'bookstore_pass_123';
GRANT ALL PRIVILEGES ON bookstore_db.* TO 'bookstore_user'@'localhost';
FLUSH PRIVILEGES;
```

### Paso 4: Configurar Variables de Entorno

Edita el archivo `.env` y cambia:

```env
DB_HOST=localhost
```

### Paso 5: Ejecutar Migraciones

```bash
python manage.py makemigrations books
python manage.py migrate
```

### Paso 6: Crear Superusuario

```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@bookstore.com
# Password: admin123
```

### Paso 7: Iniciar el Servidor

```bash
python manage.py runserver
```

---

## 📡 Endpoints de la API

### URL Base: `http://localhost:8000/api/`

### CRUD de Libros

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/books/` | Listar todos los libros (paginado) |
| `POST` | `/books/` | Crear un nuevo libro |
| `GET` | `/books/{id}/` | Obtener un libro por ID |
| `PUT` | `/books/{id}/` | Actualizar libro completo |
| `PATCH` | `/books/{id}/` | Actualizar libro parcialmente |
| `DELETE` | `/books/{id}/` | Eliminar un libro |

### Endpoints Especiales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/books/{id}/calculate-price/` | Calcular precio de venta con tasa de cambio |
| `POST` | `/books/{id}/calculate-price/?currency=MXN` | Calcular precio en moneda específica |
| `GET` | `/books/search/?category=Literatura` | Buscar libros por categoría |
| `GET` | `/books/low-stock/` | Libros con stock ≤ 10 |
| `GET` | `/books/low-stock/?threshold=5` | Libros con stock ≤ 5 |
| `GET` | `/books/stats/` | Estadísticas del inventario |

---

## 🧪 Ejemplos de Uso con cURL

### Crear un Libro

```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "El Quijote",
    "author": "Miguel de Cervantes",
    "isbn": "978-84-376-0494-7",
    "cost_usd": 15.99,
    "stock_quantity": 25,
    "category": "Literatura Clásica",
    "supplier_country": "ES"
  }'
```

### Crear Otro Libro (para pruebas)

```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cien años de soledad",
    "author": "Gabriel García Márquez",
    "isbn": "9780060883287",
    "cost_usd": 12.50,
    "stock_quantity": 8,
    "category": "Realismo Mágico",
    "supplier_country": "CO"
  }'
```

### Crear Libro con Stock Bajo

```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "1984",
    "author": "George Orwell",
    "isbn": "9780451524935",
    "cost_usd": 9.99,
    "stock_quantity": 3,
    "category": "Ciencia Ficción",
    "supplier_country": "GB"
  }'
```

### Listar Todos los Libros

```bash
curl http://localhost:8000/api/books/
```

### Obtener un Libro por ID

```bash
curl http://localhost:8000/api/books/1/
```

### Actualizar Stock de un Libro (PATCH)

```bash
curl -X PATCH http://localhost:8000/api/books/1/ \
  -H "Content-Type: application/json" \
  -d '{"stock_quantity": 50}'
```

### Actualizar Libro Completo (PUT)

```bash
curl -X PUT http://localhost:8000/api/books/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Don Quijote de la Mancha",
    "author": "Miguel de Cervantes Saavedra",
    "isbn": "978-84-376-0494-7",
    "cost_usd": 18.99,
    "stock_quantity": 30,
    "category": "Clásicos Españoles",
    "supplier_country": "ES"
  }'
```

### Eliminar un Libro

```bash
curl -X DELETE http://localhost:8000/api/books/1/
```

### 🔥 Calcular Precio de Venta (Endpoint Principal)

```bash
# Calcular con moneda por defecto (EUR)
curl -X POST http://localhost:8000/api/books/1/calculate-price/

# Calcular en Pesos Mexicanos
curl -X POST "http://localhost:8000/api/books/1/calculate-price/?currency=MXN"

# Calcular en Euros
curl -X POST "http://localhost:8000/api/books/1/calculate-price/?currency=EUR"
```

**Respuesta esperada:**
```json
{
    "book_id": 1,
    "cost_usd": "15.99",
    "exchange_rate": 0.85,
    "cost_local": "13.59",
    "margin_percentage": 40,
    "selling_price_local": "19.03",
    "currency": "EUR",
    "calculation_timestamp": "2025-01-15T10:30:00Z"
}
```

### Buscar por Categoría

```bash
curl "http://localhost:8000/api/books/search/?category=Literatura"
```

### Obtener Libros con Stock Bajo

```bash
# Stock menor o igual a 10 (default)
curl http://localhost:8000/api/books/low-stock/

# Stock menor o igual a 5
curl "http://localhost:8000/api/books/low-stock/?threshold=5"
```

### Obtener Estadísticas

```bash
curl http://localhost:8000/api/books/stats/
```

---

## 📮 Ejemplos de Uso con Postman

1. **Importar la Colección:**
   - Abre Postman
   - Click en "Import"
   - Selecciona el archivo `Bookstore_API.postman_collection.json`

2. **La colección incluye:**
   - Todas las operaciones CRUD
   - Endpoint de cálculo de precio
   - Búsqueda por categoría
   - Filtro de stock bajo
   - Pruebas de validación y errores

3. **Variable de entorno:**
   - `{{base_url}}` = `http://localhost:8000/api`

---

## ✅ Reglas de Negocio

| Regla | Implementación |
|-------|----------------|
| `cost_usd` debe ser mayor a 0 | Validación en serializer y modelo |
| `stock_quantity` no puede ser negativo | PositiveIntegerField en modelo |
| `isbn` debe tener formato válido | Validador personalizado (10 o 13 dígitos) |
| No permitir libros duplicados | Constraint unique en ISBN |
| Si API de cambio falla, usar tasa default | Try/catch en service con fallback |
| Margen de ganancia del 40% | Configurable en settings |
| Manejo de errores HTTP | 400, 404, 500, 503 implementados |

---

## 🐳 Comandos Docker Útiles

### Gestión de Contenedores

```bash
# Levantar contenedores (modo normal)
docker-compose up

# Levantar contenedores (en background)
docker-compose up -d

# Levantar y reconstruir
docker-compose up --build

# Detener contenedores
docker-compose down

# Detener y eliminar volúmenes (borra la BD)
docker-compose down -v

# Ver contenedores activos
docker-compose ps

# Ver logs
docker-compose logs

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f web
docker-compose logs -f db
```

### Ejecución de Comandos

```bash
# Entrar al contenedor de la API
docker-compose exec web bash

# Ejecutar migraciones directamente
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Ejecutar tests
docker-compose exec web python manage.py test

# Abrir shell de Django
docker-compose exec web python manage.py shell

# Conectar a MySQL
docker-compose exec db mysql -u bookstore_user -p bookstore_db
```

### Limpieza

```bash
# Eliminar contenedores parados
docker container prune

# Eliminar imágenes no usadas
docker image prune

# Eliminar todo lo no usado
docker system prune -a
```

---

## 🔧 Solución de Problemas

### Error: "Table 'bookstore_db.books' doesn't exist"

**Causa:** Las migraciones no se han ejecutado.

**Solución:**
```bash
docker-compose exec web bash
python manage.py makemigrations books
python manage.py migrate
exit
```

### Error: "Unable to get image" o "Cannot connect to Docker daemon"

**Causa:** Docker Desktop no está ejecutándose.

**Solución:**
1. Abre Docker Desktop
2. Espera a que diga "Docker Desktop is running"
3. Vuelve a ejecutar `docker-compose up --build`

### Error: "Port 8000 already in use"

**Causa:** Otro proceso está usando el puerto 8000.

**Solución:**
```bash
# En Windows (PowerShell como administrador)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# En Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Error: "MySQL connection refused"

**Causa:** El contenedor de MySQL no está listo.

**Solución:**
1. Espera unos segundos más
2. Verifica con: `docker-compose logs db`
3. Si persiste: `docker-compose down -v` y luego `docker-compose up --build`

### Los cambios en el código no se reflejan

**Solución:**
```bash
docker-compose down
docker-compose up --build
```

### No puedo acceder al Admin de Django

**Causa:** No has creado un superusuario.

**Solución:**
```bash
docker-compose exec web bash
python manage.py createsuperuser
# Username: admin
# Email: admin@bookstore.com  
# Password: admin123
exit
```

Luego accede a: http://localhost:8000/admin/

---

## 🧪 Tests

### Ejecutar todos los tests

```bash
# Con Docker
docker-compose exec web python manage.py test

# Sin Docker
python manage.py test
```

### Ejecutar tests específicos

```bash
# Tests del modelo
docker-compose exec web python manage.py test books.tests.BookModelTest

# Tests de la API
docker-compose exec web python manage.py test books.tests.BookAPITest

# Tests de cálculo de precio
docker-compose exec web python manage.py test books.tests.PriceCalculationTest
```

---

## ⚙️ Configuración de Variables de Entorno

El archivo `.env` contiene las siguientes variables:

| Variable | Descripción | Valor Default |
|----------|-------------|---------------|
| `DEBUG` | Modo debug de Django | `True` |
| `SECRET_KEY` | Clave secreta de Django | (generada) |
| `ALLOWED_HOSTS` | Hosts permitidos | `localhost,127.0.0.1` |
| `DB_NAME` | Nombre de la base de datos | `bookstore_db` |
| `DB_USER` | Usuario de MySQL | `bookstore_user` |
| `DB_PASSWORD` | Contraseña de MySQL | `bookstore_pass_123` |
| `DB_HOST` | Host de MySQL | `db` (Docker) / `localhost` |
| `DB_PORT` | Puerto de MySQL | `3306` |
| `DEFAULT_EXCHANGE_RATE` | Tasa de cambio por defecto | `0.85` |
| `DEFAULT_CURRENCY` | Moneda por defecto | `EUR` |
| `PROFIT_MARGIN` | Margen de ganancia (%) | `40` |

---

## 🔐 Credenciales por Defecto

### Panel de Administración de Django

| Campo | Valor |
|-------|-------|
| URL | http://localhost:8000/admin/ |
| Usuario | `admin` |
| Email | `admin@bookstore.com` |
| Contraseña | `admin123` |

> **⚠️ IMPORTANTE:** El superusuario NO se crea automáticamente. Debes crearlo manualmente con el comando:
> ```bash
> docker-compose exec web bash
> python manage.py createsuperuser
> # Ingresa: admin / admin@bookstore.com / admin123
> exit
> ```

### Base de Datos MySQL

| Campo | Valor |
|-------|-------|
| Host | `localhost` (sin Docker) / `db` (con Docker) |
| Puerto | `3306` (interno) / `3307` (externo con Docker) |
| Base de datos | `bookstore_db` |
| Usuario | `bookstore_user` |
| Contraseña | `bookstore_pass_123` |
| Usuario root | `root` |
| Contraseña root | `root_password_123` |

---

## 📝 Notas Adicionales

- El proyecto usa **ViewSet** para el CRUD básico y **APIView** para el cálculo de precio, demostrando ambos enfoques de DRF.
- La lógica de negocio está separada en `services.py` para mejor mantenibilidad.
- Los logs están configurados para debugging.
- La API incluye paginación por defecto (10 items por página).

---

## 📄 Licencia

MIT License

---

## 👤 Autor

Desarrollado como prueba técnica para Nextep Innovation.

---

¡Gracias por revisar este proyecto! 🚀 
