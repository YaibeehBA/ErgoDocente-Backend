# ErgoDocente Backend

API REST para la aplicación de ergonomía y bienestar docente. Desarrollada con FastAPI, SQLAlchemy async y PostgreSQL.

---
## Requisitos del sistema

- Python 3.13
- PostgreSQL 14 o superior
- pip

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-repositorio>
cd ergodocente-backend
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

Activar en Windows:
```bash
venv\Scripts\activate
```

Activar en Linux/macOS:
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con los valores del entorno local. Ver la sección de variables de entorno más abajo.

### 5. Crear la base de datos

Conectarse a PostgreSQL y crear la base de datos:

```sql
CREATE DATABASE ergodocente;
```

### 6. Ejecutar migraciones

```bash
alembic upgrade head
```

### 7. Cargar datos iniciales

```bash
python -m seeders.run_seeders
```

### 8. Iniciar el servidor

Desarrollo:
```bash
uvicorn app.main:app --reload 
```
---


## Estructura del proyecto

```
ergodocente-backend/
├── app/
│   ├── core/
│   │   ├── config.py           # Configuracion y variables de entorno
│   │   ├── database.py         # Engine async y sesion de BD
│   │   ├── exceptions.py       # Jerarquia de excepciones y handlers
│   │   ├── logging_config.py   # Logging estructurado con structlog
│   │   └── security.py         # Hashing de passwords y device_id
│   ├── dependencies/
│   │   └── __init__.py         # get_db, get_device_id
│   ├── models/                 # Modelos SQLAlchemy (20 modelos)
│   ├── schemas/                # Schemas Pydantic v2 (validacion)
│   ├── repositories/           # Capa de acceso a datos
│   ├── services/               # Logica de negocio
│   ├── routers/
│   │   └── v1/                 # Endpoints REST bajo /api/v1
│   ├── utils/
│   │   ├── cloudinary_client.py
│   │   └── file_validators.py
│   └── main.py                 # FastAPI app factory
├── alembic/                    # Migraciones de base de datos
├── seeders/                    # Datos iniciales
├── tests/                      # Tests unitarios e integration
├── requirements.txt
├── .env.example
└── alembic.ini
```

---

## Arquitectura

El proyecto sigue una arquitectura en capas:

```
Router  ->  Service  ->  Repository  ->  Model
            (logica)     (queries)       (ORM)
Schemas (validacion en entrada y salida)
```

- **Routers**: reciben y validan la request con Pydantic, llaman al Service
- **Services**: contienen la logica de negocio, hacen commit de transacciones
- **Repositories**: ejecutan queries a la base de datos, hacen flush
- **Models**: definen las tablas con SQLAlchemy

---

## Autenticacion

### V1 (actual)

La identificacion del usuario se realiza mediante el header `X-Device-ID` en cada request. El dispositivo debe registrarse previamente en `POST /api/v1/dispositivos/registrar`.

```
X-Device-ID: uuid-del-dispositivo
```

### V2 (preparado)

La base de codigo tiene los stubs para JWT en `app/core/security.py`. La migracion a JWT Bearer token esta preparada para implementarse sin cambios en la logica de negocio.

---

## Endpoints principales

La documentacion interactiva esta disponible en modo desarrollo:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Resumen de endpoints

| Prefijo | Descripcion |
|---------|-------------|
| `POST /api/v1/dispositivos/registrar` | Registrar dispositivo (sin header requerido) |
| `GET /api/v1/dispositivos/mi-dispositivo` | Datos del dispositivo actual |
| `GET /api/v1/ejercicios` | Catalogo de ejercicios |
| `GET /api/v1/rutinas` | Rutinas de pausas activas |
| `GET /api/v1/emociones` | Catalogo de emociones |
| `POST /api/v1/registros-emocionales` | Registrar estado emocional |
| `GET /api/v1/registros-emocionales/estadisticas` | Resumen emocional 24h |
| `POST /api/v1/progreso` | Registrar actividad completada |
| `GET /api/v1/progreso/puntos` | Puntos y nivel del usuario |
| `GET /api/v1/recordatorios` | Recordatorios del dispositivo |
| `GET /api/v1/contenidos` | Contenidos ergonomicos |
| `GET /api/v1/enfermedades` | Catalogo de enfermedades ocupacionales |
| `GET /api/v1/consejos` | Consejos de salud |
| `GET /api/v1/mensajes-motivacionales/aleatorio` | Mensaje motivacional aleatorio |
| `POST /api/v1/archivos-media/subir` | Subir archivo a Cloudinary |
| `GET /api/v1/idiomas` | Idiomas disponibles |
| `GET /api/v1/preferencias/mi-dispositivo` | Preferencias del dispositivo |
| `GET /api/v1/health` | Estado de la API |

---

## Sistema de traducciones

El contenido textual esta disponible en Español y Kichwa. El sistema usa una tabla polimorfica `traducciones` que almacena las traducciones de cualquier entidad.

El idioma se controla desde las preferencias del dispositivo. Por defecto se usa Español.

---

## Subida de archivos

Los archivos se almacenan en Cloudinary. Los tipos y limites permitidos son:

| Tipo | Formatos | Limite |
|------|----------|--------|
| `image` | JPEG, PNG, WEBP, GIF | 5 MB |
| `video` | MP4, MOV, AVI, WEBM | 100 MB |
| `audio` | MP3, WAV, OGG, AAC, M4A | 20 MB |
| `raw` | PDF, MP3, WAV, OGG | 10 MB |

Endpoint: `POST /api/v1/archivos-media/subir`

Requiere header `X-Device-ID` y campos de formulario: `archivo` (file) y `tipo_recurso` (image/video/raw).

---

## Gamificacion

El sistema registra el progreso del usuario y calcula un nivel basado en puntos acumulados:

| Nivel | Puntos requeridos |
|-------|------------------|
| Principiante | 0 - 99 |
| Intermedio | 100 - 499 |
| Avanzado | 500 - 999 |
| Experto | 1000 o mas |

Cada actividad completada otorga 10 puntos. Las actividades parciales otorgan puntos proporcionales al porcentaje completado.

---

## Migraciones

Crear nueva migracion despues de cambios en modelos:

```bash
alembic revision --autogenerate -m "descripcion del cambio"
alembic upgrade head
```

Revertir ultima migracion:

```bash
alembic downgrade -1
```

---

## Seeders

Los seeders cargan datos iniciales necesarios para el funcionamiento de la aplicacion: idiomas, emociones, categorias, ejercicios, rutinas, contenidos, enfermedades, consejos, mensajes motivacionales y recomendaciones emocionales.

```bash
python -m seeders.run_seeders
```

Los seeders son idempotentes: pueden ejecutarse multiples veces sin duplicar datos.

---

## Dependencias principales

| Libreria | Version | Uso |
|----------|---------|-----|
| FastAPI | 0.115.5 | Framework web |
| SQLAlchemy | 2.0.36 | ORM async |
| Pydantic | 2.10.3 | Validacion de datos |
| asyncpg | 0.30.0 | Driver PostgreSQL async |
| Alembic | 1.14.0 | Migraciones |
| Cloudinary | 1.41.0 | Almacenamiento de medios |
| structlog | 24.4.0 | Logging estructurado |
| passlib | 1.7.4 | Hashing de passwords |
| python-jose | 3.3.0 | JWT (preparado para V2) |

---

## Notas de desarrollo

- El proyecto usa UUIDs como primary keys en todos los modelos.
- El soft delete esta implementado en todos los modelos que lo requieren. Los registros eliminados no aparecen en los listados por defecto.
- El commit de transacciones se realiza en la capa de Services, no en Repositories.
- Los logs en produccion se emiten en formato JSON para facilitar la ingesta en sistemas de monitoreo.
