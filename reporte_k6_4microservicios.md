# Reporte de pruebas de carga K6 - Arquitectura de 4 microservicios

**Proyecto:** extracText  
**Fecha del reporte:** 14/10/2026  
**Arquitectura evaluada:** `api-gateway -> ingestion -> (storage, extractor)` + MongoDB, expuesta por Traefik en `http://extractext.localhost`.

---

## 1. Objetivo

Comparar el rendimiento del endpoint de subida de documentos antes y después de agregar el microservicio **ingestion** y aplicar las optimizaciones de rendimiento, respetando los 12 factores de Twelve-Factor App.

El flujo evaluado es:

```text
Cliente -> Traefik -> API Gateway -> Ingestion -> (Storage, Extractor) -> MongoDB
```

---

## 2. Escenario de prueba K6

- **Script:** `spike_tests.js`
- **Endpoint:** `POST http://extractext.localhost/api/v1/documents/`
- **Cuerpo:** PDF de ~1 MB (`multipart/form-data`)
- **Carga:** rampa de 0 a 50 VUs en 40 s (`10s` subida, `20s` sostenido, `10s` bajada)
- **Naturaleza de la carga:** mayormente duplicados (mismo checksum)
- **Comando:**

```powershell
cd "C:\Users\camja\Documents\Facu\3RO FACU\Desarrollo de Software\EXTRACTEXT\extracText"
docker compose up -d --build
k6 run spike_tests.js
```

- **Thresholds configurados:**

```javascript
thresholds: {
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
    http_req_duration: ['p(95)<3500'],
}
```

---

## 3. Resultados comparativos

### 3.1 Prueba K6 - POST de subida

| Métrica | Antes (sin optimizar) | Después (4 microservicios optimizados) | Mejora |
|---|---:|---:|---:|
| Tasa de error | 0 % | 0 % | igual |
| Throughput | ~28 req/s | 79.76 req/s | +185 % |
| Mediana (p50) | 1.07 s | 0.132 s | -87.7 % |
| p90 | - | 1.68 s | - |
| p95 | 3.32 s | 1.74 s | -47.6 % |
| Máximo | 6.91 s | 2.09 s | -69.8 % |
| Checks HTTP | - | 100 % (6388/6388) | - |
| `http_req_failed` | 0 % | 0 % | igual |

> Los valores "Antes" provienen de la medición base de la consigna (arquitectura con ingestion recién integrada y sin optimizaciones). Los valores "Después" se midieron en este entorno con `WEB_CONCURRENCY=2`.

### 3.2 Detalle de la corrida K6 posterior

```text
checks_total.......: 6388    159.51/s
checks_succeeded...: 100.00% 6388 out of 6388
checks_failed......: 0.00%   0 out of 6388

http_req_duration..: avg=475.14ms min=8.47ms med=132.12ms max=2.09s p(90)=1.68s p(95)=1.74s
http_req_failed....: 0.00%  0 out of 3194
http_reqs..........: 3194   79.755678/s
data_received......: 5.4 MB
data_sent..........: 3.8 GB

THRESHOLDS
checks  rate>0.99 ......... 100.00%  PASS
p(95)<3500 ................ 1.74s    PASS
http_req_failed rate<0.01 . 0.00%    PASS
```

### 3.3 Prueba complementaria con Vegeta - GET listado

Aunque el foco del reporte es K6, se incluye la comparación ya que el listado fue el otro endpoint crítico (respuestas de ~350 KB).

- **Prueba:** `GET http://extractext.localhost/api/v1/documents/?limit=20&offset=0`, 50 req/s durante 30 s.

| Métrica | Antes | Después | Mejora |
|---|---:|---:|---:|
| Éxito | 100 % | 100 % | igual |
| Throughput real | 43.97 req/s | 50.03 req/s | +13.8 % |
| Mediana | 216 ms | 5.5 ms | -97.5 % |
| Media | 2.25 s | 6.0 ms | -99.7 % |
| p95 | 7.2 s | 8.7 ms | -99.9 % |
| Máximo | 9.7 s | 15.9 ms | -99.8 % |
| Tamaño de respuesta | ~350 KB | 3.58 KB | -99.0 % |

---

## 4. Qué se cambió para lograr la mejora

1. **Cliente HTTP compartido (`httpx.AsyncClient`)** en api-gateway e ingestion, creado en el `lifespan` y cerrado con `aclose()`. Evita abrir una conexión nueva por request.
2. **Passthrough en el gateway**: el listado, el detalle y el POST devuelven el cuerpo aguas abajo sin hacer `response.json()` + validación Pydantic otra vez.
3. **Upload del gateway por streaming**: reenvía `request.stream()` a ingestion sin leer el PDF completo en el gateway.
4. **Rechazo temprano por tamaño (413)**: si el `Content-Length` supera `PDF_MAX_SIZE_MB` + 64 KiB, se corta antes de leer el cuerpo.
5. **Extractor sin bloquear el event loop**: la extracción con pypdf se ejecuta con `run_in_threadpool`.
6. **Workers configurables**: `WEB_CONCURRENCY` en `docker-compose.yml` (2 por servicio), sin `--workers` hardcodeado.
7. **Listado liviano y paginado**: `DocumentSummary` + proyección que excluye `content`, orden por `_id` descendente y `skip/limit`; `limit` por defecto 50 y máximo 100.
8. **Deduplicación por checksum en ingestion**: un PDF duplicado se responde con 200 y no vuelve a llamar al extractor.

---

## 5. Conclusiones

- El **throughput del POST** pasó de ~28 req/s a **~80 req/s** con 0 % de errores.
- El **p95 del POST** bajó de **3.32 s a 1.74 s** y el máximo de **6.91 s a 2.09 s**.
- El **p95 del listado** bajó de **7.2 s a 8.7 ms** y el tamaño de respuesta de **~350 KB a ~3.6 KB**.
- La nueva arquitectura con ingestion y las optimizaciones Twelve-Factor permiten sostener la tasa de 50 req/s en el listado con 100 % de éxito, algo que antes no ocurría.
- Los thresholds configurados en `spike_tests.js` se superan en todas las corridas posteriores a los cambios.

---

## 6. Reproducción

```powershell
# 1. Levantar los 4 microservicios + backing services
cd "C:\Users\camja\Documents\Facu\3RO FACU\Desarrollo de Software\EXTRACTEXT\extracText"
docker compose up -d --build

# 2. Verificar que todos estén healthy
docker compose ps

# 3. Correr la prueba de carga
k6 run spike_tests.js
```

### Notas metodológicas

- Las mediciones se hicieron en un entorno local con Docker Desktop; no representan un entorno productivo.
- La comparación "antes" proviene de la medición base de la consigna con ingestion ya integrado y sin optimizaciones. No existe en el repositorio una medición K6 previa a la creación del microservicio ingestion, por lo que este reporte compara el estado **con ingestion sin optimizar** vs. **con ingestion optimizado**.
- El script `spike_tests.js` fue actualizado para aceptar 200 (duplicado) y 201 (alta nueva); antes esperaba 201 o 409.
