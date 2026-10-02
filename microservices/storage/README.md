#  Document Storage - extracText

Microservicio encargado de **persistir y gestionar documentos** en MongoDB.

## Responsabilidades

- CRUD completo de documentos (crear, leer, actualizar, eliminar)
- Detección de duplicados mediante checksum SHA-256
- Conexión asíncrona a MongoDB usando Motor
- Arquitectura en capas (Domain, Infrastructure, Application, API)

## Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje principal |
| FastAPI | Framework web |
| Motor | Driver async de MongoDB |
| Pydantic | Validación de datos |
| Uvicorn | Servidor ASGI |

## Estructura del Proyecto

```
storage/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── documents.py   # CRUD de documentos
│   │       └── health.py      # Health check
│   ├── domain/
│   │   ├── document.py        # Entidad Document
│   │   ├── exceptions.py      # Excepciones personalizadas
│   │   └── repository.py      # Interface del repositorio
│   ├── infrastructure/
│   │   └── repositories/
│   │       └── mongo_document_repository.py  # Implementación MongoDB
│   └── main.py                # Punto de entrada FastAPI
├── config/
│   └── settings.py            # Configuración
├── dockerfile
├── pyproject.toml
└── uv.lock
```

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/documents/` | Crear documento |
| GET | `/api/v1/documents/` | Listar todos los documentos |
| GET | `/api/v1/documents/{id}` | Obtener documento por ID |
| PUT | `/api/v1/documents/{id}` | Actualizar contenido de documento |
| DELETE | `/api/v1/documents/{id}` | Eliminar documento |

### Request (Crear documento)

```bash
curl -X POST http://localhost:8000/api/v1/documents/ \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "documento.pdf",
    "content": "Texto extraído del PDF...",
    "checksum": "a1b2c3d4e5f6..."
  }'
```

### Response

```json
{
  "id": "65a1b2c3d4e5f6...",
  "filename": "documento.pdf",
  "content": "Texto extraído del PDF...",
  "checksum": "a1b2c3d4e5f6..."
}
```

## Variables de Entorno

| Variable | Descripción | Default |
|---|---|---|
| `APP_NAME` | Nombre de la aplicación | `extracText Storage` |
| `APP_VERSION` | Versión | `0.1.0` |
| `APP_DEBUG` | Modo debug | `false` |
| `MONGODB_URL` | URL de conexión a MongoDB | `mongodb://mongo:27017` |
| `MONGODB_DB_NAME` | Nombre de la base de datos | `extractext` |

## Desarrollo Local

```bash
# Instalar dependencias
uv sync --all-extras

# Levantar servidor (requires MongoDB running)
uv run uvicorn app.main:app --reload --port 8000
```

## Docker

```bash
# Construir imagen
docker build -f dockerfile -t extractext/storage:latest .

# Levantar contenedor
docker run -p 8000:8000 extractext/storage:latest
```

## Arquitectura en Capas

Este microservicio sigue una **arquitectura en 4 capas**:

1. **API** (FastAPI Routers) — presentación
2. **Application** (Use Cases) — orquestación
3. **Domain** (Entidades, Excepciones) — reglas de negocio
4. **Infrastructure** (MongoDB, Services) — implementaciones concretas
