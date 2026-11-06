#  extracText - Extractor de Texto PDF

Proyecto desarrollado para la asignatura **Desarrollo de Software** (3er Año - UTN - FRSR). El objetivo es crear una herramienta eficiente en Python para la extracción y procesamiento de texto desde archivos PDF.

## Integrantes
* **Sirotiuk Juliana 10939** 
* **Jamardo Camila 10842**
* **Ojeda Tomas 10882**

## Características
* Extracción de texto plano de archivos PDF.
* Interfaz de línea de comandos (CLI).
* Gestión de dependencias mediante entornos virtuales.
* Arquitectura orientada a la mantenibilidad y código limpio.
* **Arquitectura de Microservicios** para escalabilidad y trabajo en equipo.

---

## Dos versiones del sistema

El proyecto tiene dos implementaciones de la misma funcionalidad:

| Versión | Dónde vive | Cómo se ejecuta |
| --- | --- | --- |
| **Monolito** | Este repositorio (`app/`) | Con `uv` (ver "Ejecutar el monolito") |
| **Microservicios** | 4 repositorios independientes, orquestados desde el `docker-compose.yml` de este repo | Con `docker compose up -d --build` |

## Arquitectura de microservicios

El sistema se divide en 4 servicios, cada uno con **su propio repositorio**:

| Servicio | Repositorio | Responsabilidad |
| --- | --- | --- |
| API Gateway | [extractext-api-gateway](https://github.com/Tomas-Ojeda/extractext-api-gateway) | Único punto de entrada. Valida y reenvía las peticiones; no tiene lógica de negocio |
| Ingestion | [extractext-ingestion](https://github.com/Tomas-Ojeda/extractext-ingestion) | Orquesta la subida: calcula el checksum, verifica duplicados y coordina al extractor y a storage |
| Extractor | [extractext-extractor](https://github.com/Tomas-Ojeda/extractext-extractor) | Valida el PDF y extrae el texto (pypdf). No guarda nada |
| Storage | [extractext-storage](https://github.com/Tomas-Ojeda/extractext-storage) | Único servicio que accede a MongoDB. CRUD de documentos e índice único sobre el checksum |

### Flujo de una subida

```
Cliente → Traefik → API Gateway → Ingestion ─┬→ Storage  (¿ya existe el checksum?)
                                             ├→ Extractor (extrae el texto)
                                             └→ Storage  (guarda el documento) → MongoDB
```

- Si el PDF **ya existe**, ingestion devuelve el documento guardado (subida idempotente) y no vuelve a extraer.
- Si dos usuarios suben el mismo PDF a la vez, el **índice único** de MongoDB deja pasar solo una inserción.
- Los servicios se comunican por **HTTP**, y se encuentran por **URLs configuradas con variables de entorno** (`INGESTION_URL`, `EXTRACTOR_URL`, `STORAGE_URL`).

### Cómo se conectan los repositorios con este proyecto

Este repositorio no contiene el código de los microservicios. El `docker-compose.yml` le indica a Docker que **construya cada imagen directamente desde el repositorio de GitHub** del servicio:

```yaml
pdf-extractxt-storage:
  build:
    context: https://github.com/Tomas-Ojeda/extractext-storage.git#main
    dockerfile: dockerfile
```


Esto cumple el Factor I (Codebase) de 12 Factor App: cada microservicio es una aplicación con su propia base de código, historial, tests y `dockerfile`. Este repositorio se encarga solo del monolito y de la **orquestación** (compose, Traefik, MongoDB y Consul).

## Infraestructura (docker-compose)

| Servicio | Descripción |
| --- | --- |
| `traefik` | Reverse proxy: enruta `extractext.localhost` hacia el API Gateway |
| `mongo` | Base de datos MongoDB (con volumen persistente) |
| `consul` | Descubrimiento de servicios (UI en el puerto 8500) |
| `pdf-extractxt-api` | API Gateway |
| `pdf-extractxt-ingestion` | Servicio de ingestion |
| `pdf-extractxt-extractor` | Servicio de extracción de texto |
| `pdf-extractxt-storage` | Servicio de persistencia (3 réplicas) |

Todos los contenedores comparten la red Docker `extractext_net`.

## Estructura del proyecto (monolito)

```
extracText/
├── app/
│   ├── api/                 # Routers de FastAPI (capa de presentación)
│   ├── application/         # Casos de uso (orquestación)
│   ├── domain/              # Entidades y excepciones (reglas de negocio)
│   └── infrastructure/      # MongoDB y servicios concretos
├── config/                  # Configuración de la app
├── tests/                   # Tests automatizados (unitarios e integración)
├── docker-compose.yml       # Orquestación de microservicios + mongo + traefik + consul
├── dockerfile               # Imagen del monolito
├── .env.example             # Variables de entorno de ejemplo
├── pyproject.toml           # Dependencias y configuración
└── README.md
```

### Arquitectura en capas

```
┌─────────────────────────────────────────┐
│  API (FastAPI Routers)                  │  ← Capa de presentación
├─────────────────────────────────────────┤
│  Application (Use Cases)                │  ← Orquestación de lógica
├─────────────────────────────────────────┤
│  Domain (Entidades, Excepciones)        │  ← Reglas de negocio puras
├─────────────────────────────────────────┤
│  Infrastructure (MongoDB, Services)     │  ← Implementaciones concretas
└─────────────────────────────────────────┘
```


## Librerías para el procesamiento de PDFs

- **Si el PDF tiene texto seleccionable:** `pypdf`, para extraer el texto página por página.

## 12 Factor App: cómo se aplica en el proyecto

| # | Factor | Aplicación en extracText |
| --- | --- | --- |
| I | **Codebase** | Una base de código por aplicación: el monolito tiene su repositorio y cada microservicio el suyo |
| II | **Dependencias** | Declaradas explícitamente en `pyproject.toml` y bloqueadas con `uv.lock` |
| III | **Configuración** | Variables de entorno (`.env.example`, bloque `environment` del compose), separadas del código |
| IV | **Backing services** | MongoDB se accede por `MONGODB_URL`, y cada servicio se trata como un recurso accesible por URL |
| V | **Build, release, run** | Se construye la imagen (`dockerfile`), se combina con la configuración (compose) y se ejecuta |
| VI | **Procesos** | Procesos sin estado: el PDF se procesa en memoria y la persistencia queda en MongoDB |
| VII | **Port binding** | Cada servicio expone su propio puerto (8000) |
| VIII | **Concurrencia** | Escala con procesos: `WEB_CONCURRENCY` y réplicas (`replicas: 3` en storage) |
| IX | **Disposability** | Contenedores descartables, con `restart: unless-stopped` |
| X | **Paridad dev/prod** | Mismas imágenes y mismo MongoDB en desarrollo y despliegue, con Docker |
| XI | **Logs** | Los servicios escriben en stdout (`docker compose logs`) |
| XII | **Admin processes** | Scripts puntuales `seed.py` y `migrate.py` en el servicio storage |

## Código limpio

- **DRY - Don't Repeat Yourself:** evitar duplicación de código y lógica innecesaria.
- **KISS - Keep It Simple, Stupid:** mantener el código simple y claro, sin complejidades innecesarias.
- **YAGNI - You Aren't Gonna Need It:** programar únicamente lo que es necesario.
- **SOLID:** busca que el código sea como un juego de LEGO: piezas independientes que encajan y se pueden cambiar sin romper toda la estructura.
  - **S (Responsabilidad única):** una clase debe hacer una sola cosa.
  - **O (Abierto/Cerrado):** el código se puede ampliar, pero no modificar.
  - **L (Sustitución de Liskov):** una clase hija debe poder usarse en lugar de su padre sin romper nada.
  - **I (Segregación de interfaces):** es mejor tener muchas interfaces pequeñas que una gigante con métodos que no se usan.
  - **D (Inversión de dependencias):** no se depende de clases concretas, sino de abstracciones (interfaces).

---

## 🔧 Herramientas de Testing de Carga

### **Vegeta**
- Herramienta CLI escrita en Go para mandar muchos requests HTTP de manera simultánea.
- Mide: latencia, RPS (requests por segundo), % de requests fallidas, errores.
- Resultado en texto plano.

### **K6**
- Framework moderno de pruebas de carga con scripts en JavaScript.
- Simula usuarios reales, mide tiempos de respuesta, datos procesados, % de fallos, usuarios simultáneos.
- Genera gráficos.

---

## 🐳 Docker Compose

### **Servicios orquestados:**

| Servicio | Descripción | Réplicas |
|---|---|---|
| `traefik` | Reverse proxy / enrutamiento local | 1 |
| `mongo` | Base de datos MongoDB | 1 |
| `pdf-extractxt-api` | API Gateway (FastAPI) | 1 |
| `pdf-extractxt-extractor` | PDF Extractor (FastAPI + pypdf) | 1 |
| `pdf-extractxt-ingestion` | Ingestion (orquestación de subida) | 1 |
| `pdf-extractxt-storage` | Document Storage (FastAPI + MongoDB) | 3 |

### **Comandos útiles:**

| Acción | Comando |
|---|---|
| Levantar todo | `docker compose up -d --build` |
| Apagar todo | `docker compose down` |
| Apagar y borrar datos de Mongo | `docker compose down -v` |
| Ver contenedores corriendo | `docker compose ps` |
| Ver logs de todo | `docker compose logs -f` |
| Ver logs de un servicio | `docker compose logs -f pdf-extractxt-api` |
| Reiniciar un servicio | `docker compose restart pdf-extractxt-api` |
| Dashboard de Traefik | `http://localhost:8080` |

### **Variables de entorno configurables**

Todas las variables se documentan en `.env.example`. Las principales:

| Variable | Servicio | Descripción | Default |
|---|---|---|---|
| `WEB_CONCURRENCY` | todos | Procesos uvicorn por contenedor | `2` |
| `INGESTION_URL` | api-gateway | URL de Ingestion | `http://pdf-extractxt-ingestion:8000` |
| `STORAGE_URL` | api-gateway / ingestion | URL de Storage | `http://pdf-extractxt-storage:8000` |
| `EXTRACTOR_URL` | ingestion | URL del Extractor | `http://pdf-extractxt-extractor:8000` |
| `STORAGE_TIMEOUT_SECONDS` | api-gateway / ingestion | Timeout hacia Storage | `10` |
| `INGESTION_TIMEOUT_SECONDS` | api-gateway | Timeout hacia Ingestion | `45` |
| `EXTRACTOR_TIMEOUT_SECONDS` | ingestion | Timeout hacia Extractor | `30` |
| `PDF_MAX_SIZE_MB` | api-gateway / extractor | Tamaño máximo de PDF | `10` |
| `LIST_DEFAULT_LIMIT` | storage | `limit` por defecto del listado | `50` |
| `LIST_MAX_LIMIT` | storage | `limit` máximo del listado | `100` |

---

## 📋 Requisitos previos

### Software requerido:
- **Docker Desktop** — [Descargar](https://www.docker.com/products/docker-desktop/)
- **Git** — [Descargar](https://git-scm.com/)
- **mkcert** — para generar certificados HTTPS locales

---

## 🚀 Instalación paso a paso

### **1. Clonar el repositorio**

```bash
git clone https://github.com/TU_USUARIO/extracText.git
cd extracText
```

### **2. Instalar mkcert**

Windows:
```powershell
winget install Filosottile.mkcert
```

Verificar:
```powershell
mkcert -version
```

### **3. Generar el certificado HTTPS local**

```bash
mkcert -install
mkcert -cert-file certs/cert.pem -key-file certs/key.pem "extractext.localhost"
```

### **4. Agregar el dominio local al archivo hosts**

Abrir como **administrador** el Bloc de notas, abrir:
```
C:\Windows\System32\drivers\etc\hosts
```

Agregar al final:
```
127.0.0.1    extractext.localhost
```

### **5. Configurar variables de entorno**

```bash
cp .env.example .env
```

### **6. Levantar el proyecto completo**

Abrir Docker Desktop, luego en PowerShell/terminal:

```bash
docker compose up -d --build
```

Esto levanta **6 contenedores** conectados entre sí por una **red Docker compartida** (`extractext_net`).

### **7. Verificar que todo está corriendo**

```bash
docker compose ps
```

Todos los servicios deben figurar con estado `Up`.

### **8. Acceder a la interfaz web**

Abrir el navegador en:
```
http://extractext.localhost/docs
```

Verás el **Swagger UI** — una interfaz interactiva para probar todos los endpoints.

---

## 📊 Diagrama de la Arquitectura

```
                    ┌─────────────────┐
                    │   Traefik       │
                    │  (Reverse Proxy)│
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
    ┌─────────▼─────┐ ┌─────▼──────┐ ┌────▼────────┐
    │ API Gateway   │ │ PDF        │ │ Document    │
    │ (FastAPI)     │ │ Extractor  │ │ Storage     │
    │               │ │ (pypdf)    │ │ (MongoDB)   │
    └─────────┬─────┘ └─────┬──────┘ └────┬────────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────▼────────┐
                    │   MongoDB       │
                    │   (Shared DB)   │
                    └─────────────────┘
```

---

## 🧪 Testing de Cargar

### **INSTALACION DE GO**
``` CMD
winget install GoLang.Go

```

### **Vegeta**

```bash
# Instalar Vegeta
go install github.com/tsenart/vegeta/v12@latest

# Prueba de carga básica. En Git Bash (usar barra final para evitar el 307 de FastAPI)
echo "GET http://extractext.localhost/api/v1/documents/?limit=20&offset=0" | vegeta attack -duration=30s -rate=50 | vegeta report
```

### **K6**

```bash
# Instalar K6
winget install k6

# Crear script de prueba
# k6 run spike_tests.js
```

---


*UTN - Facultad Regional San Rafael - Tercer año - Desarrollo de Software - Ingeniería en Sistemas de Información - 2026*
