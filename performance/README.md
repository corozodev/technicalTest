# Performance Testing Module (Bonus)

Este módulo implementa la prueba de rendimiento solicitada como **BONUS** para la evaluación técnica de QA, evaluando la API pública de [ReqRes](https://reqres.in/).

---

## Tool & Target API

- **Herramienta:** [k6](https://k6.io/) (v2.2.0) ejecutado en contenedor Docker oficial (`grafana/k6:latest`) para máxima portabilidad y reproducibilidad sin requerir instalación local.
- **Base URL:** `https://reqres.in`
- **Endpoints evaluados:**
  - `GET /api/users?page=2`: Obtención de lista paginada de usuarios.
  - `GET /api/users/2`: Consulta de detalle de un usuario específico.
- **Autenticación / Header:**
  - `x-api-key: ${REQRES_API_KEY}`
  - La clave se inyecta dinámicamente desde la variable de entorno `REQRES_API_KEY`, garantizando que ninguna credencial quede escrita en archivos versionados.

---

## Scenario & Test Criteria

- **Virtual Users (VUs):** 10 usuarios concurrentes en bucle continuo.
- **Duración:** 30 segundos.
- **Pacing / Think Time:** Pausas controladas entre peticiones (`sleep(0.5s)` y `sleep(1s)`) para generar un flujo de tráfico constante y realista sin saturar agresivamente una API pública compartida.
- **Validaciones funcionales (Checks):**
  - Código de estado HTTP 200 en cada llamada.
  - Estructura y consistencia de datos (página esperada, lista de usuarios no vacía y correspondencia de identificador de usuario).
- **Thresholds configurados:**
  - `http_req_failed`: `rate < 0.01` (tasa de error inferior al 1%).
  - `http_req_duration`: `p(95) < 1000ms` (el 95% de las peticiones debe responder en menos de 1 segundo).
  - `checks`: `rate > 0.99` (más del 99% de aserciones funcionales exitosas).

> *Aclaración:* Los umbrales anteriores son criterios de aceptación definidos para este ejercicio técnico de QA y no representan SLAs oficiales de la plataforma ReqRes.

---

## How to Run

### Opción 1: Mediante Docker (Recomendada)
No requiere instalar k6 en el host:

```bash
# Con API key configurada
export REQRES_API_KEY="your_api_key_here"
docker run --rm -i -v "$PWD/performance:/performance" -e REQRES_API_KEY grafana/k6 run /performance/reqres.js

# O en una sola línea
docker run --rm -i -v "$PWD/performance:/performance" -e REQRES_API_KEY="your_api_key_here" grafana/k6 run /performance/reqres.js
```

### Opción 2: Con k6 instalado localmente
```bash
REQRES_API_KEY="your_api_key_here" k6 run performance/reqres.js
```

---

## Real Execution Results

Resultados obtenidos en la ejecución real controlada:

| Métrica | Valor Obtenido | Criterio / Threshold | Estado |
|---------|----------------|----------------------|--------|
| **Total Requests** | 400 peticiones (12.92 req/s) | N/A | Completado |
| **Failed Requests** | 0 peticiones (0.00%) | `rate < 1%` | PASS |
| **Checks Exitosos** | 800 / 800 (100%) | `rate > 99%` | PASS |
| **Average Response Time** | 16.56 ms | N/A | Informativo |
| **Median Response Time** | 10.42 ms | N/A | Informativo |
| **p90 Response Time** | 12.21 ms | N/A | Informativo |
| **p95 Response Time** | 18.77 ms | `< 1000 ms` | PASS |
| **Max Response Time** | 430.51 ms | N/A | Informativo |

### Interpretación Objetiva
Bajo las condiciones y el ritmo de carga configurados (10 VUs durante 30 segundos con pacing controlado), la API respondió con estabilidad, manteniendo una tasa de error de 0% y tiempos de respuesta ampliamente por debajo del umbral de 1000 ms establecido para esta prueba.
