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
* **Librerías:** PyMuPDF (fitz)
* **Control de Versiones:** Git & GitHub
* **Entorno de Desarrollo:** Visual Studio Code

## Librerias a tener en cuenta para extraer PDF
* **Si el PDF tiene texto seleccionable** pdfplumber, PyMuPDF, pypdf
* **Si el PDF esta escaneado (imagenes)** pytesseract + pdf2image  
* **Si se necesita extraer tablas** pdfplumber, Camelot, Tabula-py

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


---
*UTN - Facultad Regional San Rafael - Tercer año - Desarrollo de Software - Ingeniería en Sistemas de Información - 2026*
