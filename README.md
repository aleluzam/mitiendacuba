# MiTiendaCuba - Backend

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue.svg" alt="Python 3.13">
  <img src="https://img.shields.io/badge/Flask-3.1.1-green.svg" alt="Flask 3.1.1">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License MIT">
</p>

> Backend de comercio electrónico desarrollado en Python con Flask. API REST completa para gestionar productos, usuarios, ventas, notificaciones y alertas de inventario.

## Tabla de Contenidos

- [Descripción](#descripción)
- [Tecnologías](#tecnologías)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Modelos de Datos](#modelos-de-datos)
- [API Endpoints](#api-endpoints)
  - [Autenticación](#autenticación)
  - [Administración](#administración)
  - [Usuario](#usuario)
  - [Notificaciones](#notificaciones)
- [Autenticación y Seguridad](#autenticación-y-seguridad)
- [Servicios](#servicios)
- [Configuración](#configuración)
- [Despliegue](#despliegue)
- [Características Especiales](#características-especiales)

---

## Descripción

**MiTiendaCuba** es una plataforma de comercio electrónico completa desarrollada en Python utilizando el framework **Flask**. Este backend proporciona una API RESTful para gestionar todos los aspectos de una tienda en línea:

- **Gestión de productos** con soporte para subproductos (variantes)
- **Sistema de usuarios** con roles (administrador y cliente)
- **Procesamiento de ventas** con control de inventario
- **Sistema de alertas** automáticas de inventario bajo
- **Notificaciones** a usuarios
- **Gestión de secciones** (categorías)
- **Almacenamiento de imágenes** en la nube

El sistema sigue una arquitectura modular basada en **Blueprints de Flask**, garantizando un código escalable y mantenible.

---

## Tecnologías

### Frameworks y Librerías Principales

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| Flask | 3.1.1 | Framework web principal |
| Flask-SQLAlchemy | 3.1.1 | ORM para gestión de base de datos |
| Flask-CORS | 6.0.1 | Manejo de CORS |
| Flask-Mail | 0.10.0 | Envío de correos electrónicos |
| Flask-JWT-Extended | 4.7.1 | Autenticación JWT |

### Base de Datos

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| SQLAlchemy | 2.0.40 | ORM principal |
| PyMySQL | 1.1.1 | Driver para MySQL |
| psycopg2-binary | 2.9.10 | Driver para PostgreSQL |

### Validación y Serialización

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| Pydantic | 2.11.3 | Validación de datos |
| pydantic-core | 2.33.1 | Core de validación |

### Servicios Externos

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| Cloudinary | 1.44.1 | Almacenamiento de imágenes |

### Utilidades

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| PyJWT | 2.10.1 | Manejo de tokens JWT |
| python-dotenv | 1.1.0 | Variables de entorno |
| Werkzeug | 3.1.3 | Utilidades web y hash |
| Pillow | 11.3.0 | Procesamiento de imágenes |
| requests | 2.32.4 | Cliente HTTP |
| email-validator | 2.2.0 | Validación de emails |
| pytest | 8.4.1 | Framework de pruebas |

---

## Estructura del Proyecto

```
mitiendacuba/
├── app/
│   ├── __init__.py
│   ├── app.py                    # Punto de entrada principal
│   ├── config.py                 # Configuraciones generales
│   ├── database.py              # Configuración de base de datos
│   ├── dependencies.py          # Funciones auxiliares y dependencias
│   ├── security.py              # Funciones de seguridad y autenticación
│   ├── models/
│   │   ├── users_models.py      # Modelo de usuarios
│   │   ├── products_models.py  # Modelo de productos
│   │   ├── subproducts_models.py  # Modelo de subproductos
│   │   ├── sales_models.py     # Modelo de ventas e items
│   │   ├── alerts_models.py    # Modelo de alertas de inventario
│   │   ├── codes_models.py     # Modelo de códigos de recuperación
│   │   ├── notifications_models.py  # Modelo de notificaciones
│   │   └── sections_models.py  # Modelo de secciones
│   ├── routes/
│   │   ├── auth.py             # Rutas de autenticación
│   │   ├── mail_codes.py       # Rutas de códigos de recuperación
│   │   ├── notifications.py    # Rutas de notificaciones
│   │   ├── admin_routes/
│   │   │   ├── admin_users.py      # Gestión de usuarios
│   │   │   ├── admin_products.py   # Gestión de productos
│   │   │   ├── admin_subproducts.py  # Gestión de subproductos
│   │   │   ├── admin_sales.py      # Gestión de ventas
│   │   │   ├── admin_alerts.py     # Gestión de alertas
│   │   │   ├── admin_sections.py   # Gestión de secciones
│   │   └── user_routes/
│   │       ├── user_users.py       # Perfil de usuario
│   │       ├── user_products.py    # Productos para usuarios
│   │       └── user_sales.py       # Ventas para usuarios
│   ├── services/
│   │   ├── mail_services.py       # Servicios de correo electrónico
│   │   └── image_manager.py       # Gestor de imágenes
│   └── test/
│       └── test_web.py             # Pruebas unitarias
├── .venv/                          # Entorno virtual
├── requirements.txt                # Dependencias
├── vercel.json                    # Configuración de Vercel
├── .gitignore                     # Archivos ignorados
└── README.md                       # Documentación
```

---

## Modelos de Datos

### UserTable (Usuarios)

Gestiona la información de los usuarios del sistema.

- **Campos**: username, password_hash, name, last_name, mobile, is_active, mail, role
- **Roles**: `admin` | `user`
- **Métodos**: `to_dict()` (sin contraseña), `to_public()` (sin datos sensibles)

### ProductTable (Productos)

Representa los artículos disponibles en la tienda.

- **Campos**: name, price, description, stock, subproducts, limit_stock, featured, img_url, section_id
- **Relaciones**: Sección, Subproductos, Items de venta
- **Métodos**: `to_dict()` (admin), `to_public()` (cliente), `to_all()` (con subproductos)

### SubproductTable (Subproductos)

Variantes de un producto (tallas, colores, etc.).

- **Campos**: subproduct_id, product_id, sub_name, sub_stock
- **Relación**: Producto padre

### SaleTable (Ventas)

Registra todas las transacciones.

- **Campos**: sale_id, user_id, total_amount, created_at, completed
- **Relaciones**: Usuario, Items

### ItemsTable (Items de Venta)

Detalles de cada producto en una venta.

- **Campos**: item_id, sale_id, product_id, product_name, product_price, quantity, total_amount, sub_name

### AlertTable (Alertas)

Alertas automáticas de inventario bajo.

- **Campos**: product_id, product_name, message, actual_stock, limit_stock, created_at

### CodeTable (Códigos)

Códigos de recuperación de contraseña.

- **Campos**: code_id, user_id, code, created_at, expires_at, used
- **Expiración**: 15 minutos

### NotificationTable / NotificationUserTable (Notificaciones)

Sistema de notificaciones a usuarios.

- **Campos**: notification_id, title, message, created_at (NotificationTable)
- **Relación**: Usuario, estado de lectura

### SectionTable (Secciones)

Categorías para organizar productos.

- **Campos**: name, img, description

---

## API Endpoints

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/register` | Registra un nuevo usuario |
| POST | `/auth/login` | Inicia sesión y retorna token JWT |
| GET | `/auth/all_codes` | Lista todos los códigos de recuperación |
| POST | `/auth/send_code` | Envía código de recuperación por correo |
| PUT | `/auth/verify_code` | Verifica código y cambia contraseña |

### Administración

#### Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/admin/all_users` | Lista todos los usuarios |
| GET | `/admin/user/{data_id}` | Obtiene usuario por ID |
| DELETE | `/admin/user/delete/{data_id}` | Elimina usuario |

#### Productos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/admin/all_products` | Lista todos los productos |
| GET | `/admin/product/{data_id}` | Obtiene producto por ID |
| POST | `/admin/product/create` | Crea nuevo producto |
| PUT | `/admin/product/edit/{product_id}` | Actualiza producto |
| DELETE | `/admin/product/delete/{data_id}` | Elimina producto |
| GET | `/admin/featured_products/all` | Lista productos destacados |
| PUT | `/admin/featured_products/to_featured/{product_id}` | Marca como destacado |
| PUT | `/admin/featured_products/to_regular/{product_id}` | Quita destacado |

#### Subproductos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/admin/all_subproducts` | Lista todos los subproductos |
| GET | `/admin/subproduct/{subproduct_id}` | Obtiene subproducto por ID |
| GET | `/admin/subproducts/{product_id}` | Lista subproductos de un producto |
| POST | `/admin/subproduct/create` | Crea nuevo subproducto |
| PUT | `/admin/subproduct/edit/{subproduct_id}` | Actualiza subproducto |

#### Secciones

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/admin/section/create` | Crea nueva sección |
| PUT | `/admin/section/edit/{id}` | Actualiza sección |
| GET | `/admin/section/all` | Lista todas las secciones |
| DELETE | `/admin/section/delete/{id}` | Elimina sección |

#### Ventas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/admin/sales/all` | Lista todas las ventas |
| GET | `/admin/sales/pending_sales` | Lista ventas pendientes |
| GET | `/admin/sales/completed_sales` | Lista ventas completadas |
| PUT | `/admin/sales/complete_sale/{sale_id}` | Marca venta como completada |

#### Alertas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/admin/all_alerts` | Lista todas las alertas |

#### Imágenes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/admin/image_manager/upload_image` | Sube imagen a Cloudinary |

#### Notificaciones

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/admin/all_notifications` | Lista todas las notificaciones |
| GET | `/admin/all_users_notifications` | Lista notificaciones por usuario |
| POST | `/admin/create_notification` | Crea nueva notificación |

### Usuario

#### Perfil

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/user/my_profile` | Obtiene datos del perfil |
| PUT | `/user/my_profile/edit` | Actualiza perfil |
| DELETE | `/user/my_profile/delete` | Elimina cuenta |
| PUT | `/user/my_profile/change_password` | Cambia contraseña |

#### Productos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/user/all_products` | Lista productos disponibles |
| GET | `/user/product/{product_id}` | Obtiene producto con subproductos |
| GET | `/user/featured_products/all` | Lista productos destacados |
| GET | `/user/products/section/{section_name}` | Filtra por sección |

#### Ventas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/user/my_profile/my_purchases` | Historial de compras |
| POST | `/user/sales/new` | Procesa nueva venta |

#### Notificaciones

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/user/my_profile/my_notifications` | Notificaciones del usuario |

---

## Autenticación y Seguridad

### JWT (JSON Web Tokens)

- Tokens con vigencia de **24 horas**
- Algoritmo de firma: **HS256**
- Información del token: `user_id`, `username`
- Formato del header: `Authorization: Bearer {token}`

### Control de Acceso

- **`@login_required`**: Protege rutas que requieren autenticación
- **`@admin_only`**: Restringe acceso solo a administradores
- **`@user_only`**: Restringe acceso solo a usuarios regulares

### Seguridad de Contraseñas

- Hash utilizando **Werkzeug** (`generate_password_hash`)
- Verificación segura con `check_password_hash`
- Validación de longitud: 8-128 caracteres

### Validación de Datos

- Modelos **Pydantic** para validación de entrada
- Validación de imágenes:
  - Extensiones permitidas: png, jpg, jpeg, gif, webp, bmp, tiff
  - Tamaño: 1KB - 10MB
  - Dimensiones: 10x10 - 5000x5000 píxeles

### CORS

- Configuración flexible para permitir solicitudes cross-origin
- Métodos permitidos: GET, POST, PUT, PATCH, DELETE

---

## Servicios

### Envío de Correos (Flask-Mail)

- Servidor SMTP configurable
- Soporte para TLS y SSL
- **Envío asíncrono** mediante hilos (mejora tiempos de respuesta)
- Uso principal: Recuperación de contraseñas

### Almacenamiento en la Nube (Cloudinary)

- Gestión completa de imágenes
- Validación antes de subida
- URLs seguras para imágenes

---

## Configuración

### Variables de Entorno

#### Base de Datos

```env
DATABASE_URL=mysql+pymysql://user:password@host:port/dbname
# o
DATABASE_URL=postgresql://user:password@host:port/dbname
```

#### Seguridad

```env
SECRET_KEY=tu_clave_secreta_aqui
```

#### Correo Electrónico

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_password
MAIL_DEFAULT_SENDER=tu_email@gmail.com
```

#### Cloudinary

```env
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
```

### Ejecución Local

```bash
# 1. Crear entorno virtual
python -m venv .venv

# 2. Activar entorno virtual
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\Activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear archivo .env con las variables

# 5. Ejecutar la aplicación
python app/app.py
```

El servidor estará disponible en `http://localhost:8080`

---

## Despliegue

### Vercel (Serverless)

El proyecto incluye configuración para despliegue en **Vercel**:

```json
{
  "routes": [{ "src": "/(.*)", "dest": "/app/app.py" }],
  "builds": [
    {
      "src": "/app/app.py",
      "use": "@vercel/python"
    }
  ]
}
```

### Requisitos para Producción

- Servidor de base de datos dedicado (MySQL o PostgreSQL)
- SSL/TLS para todas las comunicaciones
- Variables de entorno de manera segura
- Dominio personalizado con HTTPS
- Sistema de logs para monitoreo
- Copias de seguridad periódicas

---

## Características Especiales

### Sistema de Alertas de Inventario

- Monitoreo automático del stock
- Alertas cuando el stock cae por debajo del **10%** del inicial
- Información: producto afectado, stock actual, límite, fecha

### Gestión de Subproductos

- Variantes de productos (tallas, colores, etc.)
- Control de inventario individual por variante
- Stock del producto padre = suma de subproductos

### Productos Destacados

- Marcado de productos para promoción
- Endpoints específicos para listarlos

### Sistema de Secciones

- Organización de productos en categorías
- Filtrado de productos por sección
- Imagen y descripción por sección

### Procesamiento de Ventas

- Validación automática de stock
- Actualización inmediata del inventario
- Soporte para productos simples y subproductos
- Historial completo de compras por usuario

---

## Licencia

MIT License - Copyright (c) 2025 MiTiendaCuba

---

## Contribuciones

Las contribuciones son bienvenidas. Por favor, Abre un issue o pull request para sugerencias y mejoras.
