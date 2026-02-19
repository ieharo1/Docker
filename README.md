# Dashboard de Monitoreo Django con Prometheus y Grafana

Stack de observabilidad para una API Django con:
- Django + Django REST Framework
- Prometheus para scraping y almacenamiento de métricas
- Grafana para visualización
- PostgreSQL como base de datos
- Docker Compose para orquestación

## Vista del sistema

### Grafana
![Grafana Dashboard](./grafana.png)

### Prometheus
![Prometheus Targets](./prometheus.png)

## Requisitos

- Docker Desktop (o Docker Engine)
- Docker Compose v2

Verifica:

```bash
docker --version
docker compose version
```

## Variables de entorno

El proyecto usa `.env`. Si vas a producción, cambia al menos:
- `DJANGO_SECRET_KEY`
- `DB_PASSWORD`
- `GRAFANA_ADMIN_PASSWORD`
- `ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`

## Levantar contenedores

Desde la raíz del repo (`C:\Users\Nabetse\Downloads\Docker`):

```bash
docker compose up -d --build
```

Verifica estado:

```bash
docker compose ps
```

Debes ver `healthy` en:
- `monitoring_postgres`
- `monitoring_django`
- `monitoring_prometheus`
- `monitoring_grafana`

## URLs de acceso

- Django API: http://localhost:8000
- Métricas Django: http://localhost:8000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

Credenciales Grafana por defecto:
- Usuario: `admin`
- Password: `grafana_secure_pass_456`

## Generar datos de ejemplo (para ver gráficas)

### Opción rápida (PowerShell)

```powershell
Invoke-WebRequest -UseBasicParsing http://localhost:8000/api/health/live/ | Out-Null
Invoke-WebRequest -UseBasicParsing http://localhost:8000/api/health/status/ | Out-Null

1..30 | ForEach-Object {
  Invoke-WebRequest -UseBasicParsing -Method Post -Uri http://localhost:8000/api/metrics-info/simulate_load/ `
    -ContentType "application/json" `
    -Body '{"iterations":10}' | Out-Null
  Start-Sleep -Milliseconds 300
}
```

### Opción curl

```bash
curl http://localhost:8000/api/health/live/
curl http://localhost:8000/api/health/status/

for i in {1..30}; do
  curl -X POST http://localhost:8000/api/metrics-info/simulate_load/ \
    -H "Content-Type: application/json" \
    -d '{"iterations":10}'
  sleep 0.3
done
```

## Validar pipeline de métricas

### 1. Prometheus está scrapeando

Abre:
- http://localhost:9090/targets

Debe aparecer `UP` para:
- `django_app`
- `prometheus`

### 2. Consultas PromQL de prueba

En Prometheus (`/graph`) prueba:

```promql
up
```

```promql
rate(django_http_requests_total_by_method_total[5m])
```

```promql
process_resident_memory_bytes / 1024 / 1024
```

### 3. Dashboard en Grafana

1. Abre http://localhost:3000
2. Login con `admin` / `grafana_secure_pass_456`
3. Ve a `Dashboards` -> `Django Monitoring Dashboard`
4. Rango recomendado: `Last 15 minutes`

## Operación diaria

Ver logs:

```bash
docker compose logs -f django_app
docker compose logs -f prometheus
docker compose logs -f grafana
```

Reiniciar servicios:

```bash
docker compose restart
```

Parar todo:

```bash
docker compose down
```

Parar y borrar volúmenes:

```bash
docker compose down -v
```

## Despliegue a producción

Base mínima recomendada:
1. Configura secretos reales en `.env`.
2. Usa dominio real en `ALLOWED_HOSTS` y `CORS_ALLOWED_ORIGINS`.
3. Publica detrás de un reverse proxy con TLS (Nginx/Traefik).
4. Mantén persistencia de volúmenes de `postgres`, `prometheus`, `grafana`.
5. Activa backups de PostgreSQL y snapshots de volúmenes.

Comando típico en servidor:

```bash
git pull
docker compose up -d --build
docker compose ps
```

## Estructura

```text
Docker/
├── api/
├── config/
├── grafana/
│   ├── dashboards/
│   └── provisioning/
├── postgres/
├── prometheus/
├── docker-compose.yml
├── Dockerfile
├── README.md
├── grafana.png
└── prometheus.png
```
