# extracText

Extractor de texto de archivos PDF con persistencia en MongoDB.
Proyecto universitario - Desarrollo de Software 2026 - UTN Facultad Regional San Rafael.

## Tecnologías

- **Python 3.12** con `uv` como gestor de paquetes
- **FastAPI** como framework web
- **MongoDB** con **Motor** (async) como base de datos
- **pypdf** para extracción de texto en memoria
- **pytest** con TDD

## Arquitectura

El proyecto sigue una arquitectura en capas (Enterprise Application Architecture):

```
app/
├── api/            # Capa de presentación: routers FastAPI, schemas
│   └── v1/
├── application/    # Casos de uso: orquesta el flujo de negocio
│   └── use_cases/
├── domain/         # Entidades, repositorio abstracto, excepciones
└── infrastructure/ # Implementaciones concretas: MongoDB, extractor PDF
    ├── repositories/
    └── services/
config/             # Settings con pydantic-settings (12-factor app)
tests/              # Tests unitarios e integración
```

## Setup rápido

```bash
# 1. Instalar uv
curl -Lsf https://astral.sh/uv/install.sh | sh

# 2. Instalar dependencias
uv sync --all-extras

# 3. Copiar y editar variables de entorno
cp .env.example .env

# 4. Levantar MongoDB (con Docker)
docker run -d -p 27017:27017 --name mongo mongo:7

# 5. Correr la aplicación
uv run uvicorn app.main:app --reload

# 6. Correr los tests
uv run pytest
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/v1/documents/` | Subir PDF y extraer texto |
| GET | `/api/v1/documents/` | Listar todos los documentos |
| GET | `/api/v1/documents/{id}` | Obtener documento por ID |
| PUT | `/api/v1/documents/{id}` | Actualizar contenido |
| DELETE | `/api/v1/documents/{id}` | Eliminar documento |
| GET | `/api/v1/health` | Health check |

Documentación interactiva disponible en `/docs` una vez levantada la app.

## Principios aplicados

- **SOLID**: cada clase tiene una única responsabilidad; el repositorio usa inversión de dependencias
- **DRY**: lógica de extracción y checksum en servicios reutilizables
- **KISS**: flujo simple sin abstracciones innecesarias
- **YAGNI**: solo se implementa lo requerido
- **TDD**: tests escritos antes que la implementación
- **12-Factor App**: configuración desde entorno, dependencias explícitas, codebase único
