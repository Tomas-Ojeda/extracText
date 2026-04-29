#  extracText - Extractor de Texto PDF

Proyecto desarrollado para la asignatura **Desarrollo de Software** (3er Año - UTN - FRSR). El objetivo es crear una herramienta eficiente en Python para la extracción y procesamiento de texto desde archivos PDF.

## Integrantes
* **Sirotiuk Juliana 10939** 
* **Jamardo Camila 10842**
* **Ojeda Tomas 10882**

##  Características
* Extracción de texto plano de archivos PDF.
* Interfaz de línea de comandos (CLI).
* Gestión de dependencias mediante entornos virtuales.
* Arquitectura orientada a la mantenibilidad y código limpio.

##  Tecnologías y Herramientas
* **Lenguaje:** Python 
* **Librerías:** Pypdf (fitz)
* **Control de Versiones:** Git & GitHub 
* **Entorno de Desarrollo:** Visual Studio Code

## Librerías para el procesamiento de PDFs
* **Si el PDF tiene texto seleccionable** pdfplumber, PyMuPDF, pypdf
    *  pdfplumber  -->  Permite obtener texto de forma estructurada y detectar elementos como tablas y columnas. 
    *  PyMuPDF  -->  Permite extraer textos e imágenes, renderizar pags. y realizar modificaciones sobre archivos.
    *  pypdf  -->  Permite unir, dividir y rotar pags., y gestionar metadatos.
* **Si el PDF esta escaneado (imagenes)** pytesseract + pdf2image  
    *  pytesseract + pdf2image -->  Juntos, permiten procesar archivos PDF escaneados. pdf2image convierte cada pág.
       en una imagen y pytesseract aplica técnicas OCR (reconocimiento óptico de caracteres) para extraer el texto.
* **Si se necesita extraer tablas** pdfplumber, Camelot
    *  Camelot  -->  Permite detectar tablas precisamente cuando estan bien definidas en el doc. y permite exportar 
       los datos a formatos como CSV o DataFrame.

## Requisitos del Proyecto (12 Factor App - sugeridos en clase)
* **Codebase** Se debe contar con una única base de código, versionada en un repositorio.
* **Dependencias** Todas las dependencias deben declararse explícitamente (mediante pyproject.toml, etc).
Se intenta evitar errores cuando muchas personas trabajan en el proyecto.
* **Variables de Entorno** Utilizadas para configurar aspectos sensibles o particulares del entorno de ejecución.
* **Configuraciones** Las configuraciones del sistema deben mantenerse separadas del código, de esta manera, el 
código puede ejecutarse en distintos entornos sin modificaciones.
* **Backing Services** Servicios externos como bases de datos, colas de mensajes, storage, etc, deben tratarse
como recursos intercambiables.
* **Construir, Desplegar, Ejecutar** preparar el proyecto, combinar build + configuracion, ejecutar.
* **Procesos** Ejecutar como uno o mas procesos sin estados persistentes en memoria interna.
* **Asignación de Puertos** La aplicación debe exponer servicios a través de puertos definidos.

## Codigo limpio
* **DRY - Don't Repeat Yoursefl** Evitar duplicación de codigo y lógica innecesaria.
* **KISS - Keep It Simple, Stupid** Mantener el código simple y claro, sin complejidades innecesarias.  
* **YAGANI - You Aren't Gonna Need It** Programar únicamente lo que es necesario.

## extracText - GUÍA DE INSTALACIÓN

Extractor de texto de archivos PDF con persistencia en MongoDB.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.115.0-009688)
![License](https://img.shields.io/badge/license-MIT-green)

## Descripción

Esta aplicación permite a los usuarios:

- **Subir archivos PDF** — Los envía el cliente en formato binario
- **Extraer texto automáticamente** — Lee el contenido directamente en memoria, sin guardar archivos temporales
- **Persistir en MongoDB** — Guarda el documento con su checksum (SHA-256) para detectar duplicados
- **Gestionar documentos** — CRUD completo: obtener, listar, actualizar y eliminar documentos

Está construida siguiendo arquitectura empresarial en capas, TDD (Test-Driven Development), y principios YAGNI, DRY, KISS, SOLID, ya explicados anteoriormente.

## Arquitectura

El proyecto sigue una arquitectura en **4 capas bien separadas**:

```
┌─────────────────────────────────────────┐
│  API (FastAPI Routers)                  │  ← Capa de presentación
├─────────────────────────────────────────┤
│  Application (Use Cases)                │  ← Orquestación de lógica
├─────────────────────────────────────────┤
│  Domain (Entidades, Excepciones)        │  ← Reglas de negocio puro
├─────────────────────────────────────────┤
│  Infrastructure (MongoDB, Services)     │  ← Implementaciones concretas
└─────────────────────────────────────────┘
```

Cada capa tiene responsabilidades claras y se comunica a través de interfaces abstractas.

---

## Requisitos previos

Antes de instalar, nos aseguramos de tener:

### Software requerido:
- **Python 3.12+** — [Descargar](https://www.python.org/downloads/)
- **Docker Desktop** — [Descargar](https://www.docker.com/products/docker-desktop/)
- **Git** — [Descargar](https://git-scm.com/)

### Para verificar la instalación:

```powershell
python --version
docker --version
git --version
```

Deberías ver versiones similares a:
```
Python 3.12.13
Docker version 27.0.0
git version 2.45.0
```

---

## Instalación paso a paso

### **Clonar el repositorio**

```bash
git clone https://github.com/TU_USUARIO/extracText.git
cd extracText
```

### **Instalar gestor de paquetes `uv`**

`uv` es un gestor moderno y rápido de Python (alternativa a pip).

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy BypassCurrent -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Reinicia PowerShell/terminal y verifica:
```bash
uv --version
```

### **Instalar dependencias del proyecto**

```bash
uv sync --all-extras
```

Esto instala:
- FastAPI y Uvicorn (servidor web)
- MongoDB driver (Motor para async)
- pypdf (extracción de texto)
- pytest y pytest-asyncio (testing)
- y más...

El proceso tarda ~30 segundos la primera vez.

### **Configuramos variables de entorno**

```bash
cp .env.example .env
```

El archivo `.env` contiene configuraciones como:
```ini
APP_NAME=extracText
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=extractext
PDF_MAX_SIZE_MB=10
```

Si querés cambiar algo, editá el `.env` (opcional).

### **Levantar MongoDB con Docker**

Abrí Docker Desktop (buscalo en el menú Inicio, esperamos a que la ballena esté corriendo).

Después en PowerShell/terminal:

```bash
docker run -d -p 27017:27017 --name mongo mongo:7
```

Si ya lo corriste antes:
```bash
docker start mongo
```

Verificá que está corriendo:
```bash
docker ps
```

Deberías ver un contenedor llamado `mongo` con estado `Up`.

---

## Ejecutamos la aplicación

### Levantamos el servidor

```bash
uv run uvicorn app.main:app --reload
```

Deberías ver algo como:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**¡La app está corriendo!**

### Acceder a la interfaz web

Abrí tu navegador en:

```
http://127.0.0.1:8000/docs
```

Verás el **Swagger UI** — una interfaz interactiva para probar todos los endpoints.

---

*UTN - Facultad Regional San Rafael - Tercer año - Desarrollo de Software - Ingeniería en Sistemas de Información - 2026*
