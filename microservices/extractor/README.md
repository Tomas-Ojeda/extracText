#  PDF Extractor - extracText

Microservicio encargado de **extraer texto desde archivos PDF** y calcular su checksum SHA-256.

## Responsabilidades

- Recibir archivos PDF en bytes
- Validar que el archivo sea un PDF válido
- Extraer texto plano usando pypdf
- Calcular checksum SHA-256 para detección de duplicados
- Devolver texto y checksum al API Gateway

## Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje principal |
| FastAPI | Framework web |
| pypdf | Extracción de texto de PDFs |
| Uvicorn | Servidor ASGI |

## Estructura del Proyecto

```
extractor/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── extract.py     # Endpoint de extracción
│   ├── services/
│   │   ├── pdf_extractor.py   # Lógica de extracción
│   │   └── checksum_service.py # Cálculo SHA-256
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
| POST | `/api/v1/extract` | Extraer texto de un PDF |

### Request

```bash
curl -X POST http://localhost:8000/api/v1/extract \
  -F "file=@documento.pdf"
```

### Response

```json
{
  "content": "Texto extraído del PDF...",
  "checksum": "a1b2c3d4e5f6..."
}
```

## Variables de Entorno

| Variable | Descripción | Default |
|---|---|---|
| `APP_NAME` | Nombre de la aplicación | `extracText Extractor` |
| `APP_VERSION` | Versión | `0.1.0` |
| `APP_DEBUG` | Modo debug | `false` |
| `PDF_MAX_SIZE_MB` | Tamaño máximo de PDF en MB | `10` |

## Desarrollo Local

```bash
# Instalar dependencias
uv sync --all-extras

# Levantar servidor
uv run uvicorn app.main:app --reload --port 8000
```

## Docker

```bash
# Construir imagen
docker build -f dockerfile -t extractext/extractor:latest .

# Levantar contenedor
docker run -p 8000:8000 extractext/extractor:latest
```
