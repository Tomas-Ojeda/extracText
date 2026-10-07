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

## 🏗️ Arquitectura de Microservicios

El proyecto está dividido en **3 microservicios** independientes, cada uno en su propio subdirectorio:

```
extracText/
├── microservices/
│   ├── api-gateway/          # Microservicio 1: API Gateway (FastAPI)
│   │   ├── app/
│   │   ├── config/
│   │   ├── dockerfile
│   │   ├── pyproject.toml
│   │   └── uv.lock
│   ├── extractor/            # Microservicio 2: PDF Extractor (FastAPI + pypdf)
│   │   ├── app/
│   │   ├── config/
│   │   ├── dockerfile
│   │   ├── pyproject.toml
│   │   └── uv.lock
│   └── storage/              # Microservicio 3: Document Storage (FastAPI + MongoDB)
│       ├── app/
│       ├── config/
│       ├── dockerfile
│       ├── pyproject.toml
│       └── uv.lock
├── docker-compose.yml        # Orquestación de microservicios
├── dockerfile                # Dockerfile legacy (monolito)
├── pyproject.toml            # Dependencias del monolito
└── README.md
```

### **1. API Gateway** (`microservices/api-gateway/`)
- **Responsabilidad:** Recibir todas las requests HTTP y enrutarlas a los microservicios correspondientes.
- **Tecnología:** FastAPI + httpx
- **Función:** Punto de entrada único, manejo de autenticación, rate limiting.
- **Integrante asignado:** Por definir

### **2. PDF Extractor** (`microservices/extractor/`)
- **Responsabilidad:** Extraer texto de los archivos PDF.
- **Tecnología:** FastAPI + pypdf
- **Función:** Recibir PDF, procesarlo, devolver texto plano y checksum SHA-256.
- **Integrante asignado:** Por definir

### **3. Document Storage** (`microservices/storage/`)
- **Responsabilidad:** Persistir documentos en MongoDB.
- **Tecnología:** FastAPI + Motor (async MongoDB)
- **Función:** CRUD de documentos, checksum SHA-256, detección de duplicados.
- **Integrante asignado:** Por definir

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

Esto levanta **5 contenedores** conectados entre sí por una **red Docker compartida** (`extractext_net`).

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

# Prueba de carga básica
echo "GET http://extractext.localhost/api/v1/documents" | vegeta attack -duration=30s -rate=50 | vegeta report
```

### **K6**

```bash
# Instalar K6
winget install k6

# Crear script de prueba
# k6 run load_test.js
```

---

## 📚 Librerías para el procesamiento de PDFs

* **Si el PDF tiene texto seleccionable**
    *  pypdf  -->  Permite unir, dividir y rotar pags., y gestionar metadatos.

---

## 📋 Requisitos del Proyecto (12 Factor App)

* **Codebase** Se debe contar con una única base de código, versionada en un repositorio.
* **Dependencias** Todas las dependencias deben declararse explícitamente (mediante pyproject.toml, etc).
* **Variables de Entorno** Utilizadas para configurar aspectos sensibles o particulares del entorno de ejecución.
* **Configuraciones** Las configuraciones del sistema deben mantenerse separadas del código.
* **Backing Services** Servicios externos como bases de datos, colas de mensajes, storage, etc, deben tratarse como recursos intercambiables.
* **Construir, Desplegar, Ejecutar** preparar el proyecto, combinar build + configuracion, ejecutar.
* **Procesos** Ejecutar como uno o mas procesos sin estados persistentes en memoria interna.
* **Asignación de Puertos** La aplicación debe exponer servicios a través de puertos definidos.

---

## 🧹 Código limpio

* **DRY - Don't Repeat Yourself** Evitar duplicación de codigo y lógica innecesaria.
* **KISS - Keep It Simple, Stupid** Mantener el código simple y claro, sin complejidades innecesarias.  
* **YAGANI - You Aren't Gonna Need It** Programar únicamente lo que es necesario.
* **SOLID -** Busca que el código sea como un juego de LEGO: piezas independientes que encajan perfectamente y que puedas cambiar sin tener que romper toda la estructura.

---

*UTN - Facultad Regional San Rafael - Tercer año - Desarrollo de Software - Ingeniería en Sistemas de Información - 2026*
