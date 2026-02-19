# 📊 DASHBOARD DE MONITOREO DJANGO - PROMETHEUS & GRAFANA

<p align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django" alt="Django">
  <img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus" alt="Prometheus">
  <img src="https://img.shields.io/badge/Grafana-F2CC0C?style=for-the-badge&logo=grafana" alt="Grafana">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker" alt="Docker">
</p>

**Solución profesional de observabilidad para aplicaciones Django usando Prometheus y Grafana. Completamente dockerizado, listo para producción y con arquitectura empresarial.**

---

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Características](#características)
4. [Requisitos Previos](#requisitos-previos)
5. [Inicio Rápido](#inicio-rápido)
6. [Servicios y Puntos de Acceso](#servicios-y-puntos-de-acceso)
7. [Endpoints de la API](#endpoints-de-la-api)
8. [Métricas Expuestas](#métricas-expuestas)
9. [Dashboard y Visualización](#dashboard-y-visualización)
10. [Configuración](#configuración)
11. [Despliegue en Producción](#despliegue-en-producción)
12. [Resolución de Problemas](#resolución-de-problemas)
13. [Contacto y Autor](#contacto-y-autor)

---

## 🎯 Descripción General

Este proyecto demuestra una **arquitectura de observabilidad lista para producción** para aplicaciones Django. Integra recopilación, almacenamiento y visualización de métricas en tiempo real utilizando herramientas estándar de la industria:

- **Django 4.2** - Framework web con API REST
- **Prometheus** - Base de datos de series de tiempo y sistema de monitoreo
- **Grafana** - Plataforma de visualización y alertas
- **PostgreSQL** - Base de datos de aplicación
- **Docker Compose** - Orquestación de infraestructura

### ¿Por Qué Esta Arquitectura?

✅ **Observabilidad a Escala** - Métricas reales de una aplicación real
✅ **Mejores Prácticas DevOps** - Infraestructura como Código, seguridad, modularidad
✅ **Lista para Producción** - Health checks, logging, políticas de reinicio
✅ **Inteligencia de Monitoreo** - Métricas personalizadas, scraping automatizado, dashboards
✅ **Estándares Empresariales** - Separación de responsabilidades, variables de entorno, documentación

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                    STACK DE MONITOREO                          │
└─────────────────────────────────────────────────────────────────┘

                          ┌──────────────┐
                          │   Grafana    │
                          │  :3000       │
                          │ Dashboard    │
                          └──────┬───────┘
                                 │
                         Consulta/Visualiza
                                 │
                          ┌──────▼───────┐
                          │ Prometheus   │
                          │   :9090      │
                          │ Almacenamiento│
                          └──────┬───────┘
                                 │
              Extrae Métricas (cada 15s)
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
     ┌────▼─────┐          ┌─────▼────┐         ┌──────▼────┐
     │  Django  │          │PostgreSQL│         │Prometheus │
     │  :8000   │          │ :5432    │         │  Self     │
     │ /metrics/│          │Base Datos│         │ Monitoreo │
     └──────────┘          └──────────┘         └───────────┘
          │
          └─ Expone endpoint /metrics/
             - Requests HTTP
             - Conexiones BD
             - Memoria/CPU
             - Métricas personalizadas


┌─────────────────────────────────────────────────────────────────┐
│                 RED INTERNA (Docker)                            │
├─────────────────────────────────────────────────────────────────┤
│ Todos los servicios se comunican por red interna "monitoring"  │
│ Aislada de la máquina host (mejor práctica de seguridad)        │
└─────────────────────────────────────────────────────────────────┘
```

### Comunicación entre Servicios

| Servicio | Host Interno | Puerto Interno | Puerto Externo |
|----------|-------------|-----------------|-----------------|
| Django App | django_app | 8000 | 8000 |
| Prometheus | prometheus | 9090 | 9090 |
| Grafana | grafana | 3000 | 3000 |
| PostgreSQL | postgres_db | 5432 | 5432 |

---

## ✨ Características

### Recopilación de Métricas Reales
- ✅ Conteo y latencia de requests HTTP (por método, endpoint, estatus)
- ✅ Tasas de error y distribución de códigos de estatus
- ✅ Pool de conexiones a base de datos
- ✅ Uso de memoria y CPU de la aplicación
- ✅ Histogramas de tiempo de respuesta (p50, p95, p99)
- ✅ Endpoints de health check (liveness, readiness probes)

### Dashboard Profesional
- 📊 Requests por segundo (promedio 5m)
- 📊 Latencia de respuesta p95 (milisegundos)
- 📊 Tasa de error por código de estatus
- 📊 Conexiones activas a base de datos
- 📊 Tendencias de uso de memoria
- 📊 Porcentaje de uso de CPU
- 📊 Distribución de códigos de estatus HTTP
- 📊 Estado de salud de servicios
- 📊 Tabla de requests totales (ventana de 30m)

### Listo para Producción
- 🔒 Ejecución sin usuario root
- 🔒 Configuración por variables de entorno
- 🔒 Health checks en todos los servicios
- 🔒 Políticas automáticas de reinicio
- 🔒 Logging estructurado
- 🔒 Persistencia de volúmenes
- 🔒 Aislamiento de red

---

## 📦 Requisitos Previos

### Requisitos del Sistema
- Docker Desktop 20.10+ o Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB RAM mínimo (8GB recomendado)
- 10GB espacio en disco

### Software Requerido
```bash
# Verificar instalaciones
docker --version
docker compose version
```

### Para Desarrollo Local (opcional)
```bash
# Python 3.11+
python --version

# Si quieres ejecutar sin Docker
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Inicio Rápido

### 1. Configurar el Repositorio

```bash
# Navega al directorio del proyecto
cd /ruta/a/Docker

# Verifica que Git está inicializado
git status
```

### 2. Configurar Variables de Entorno

```bash
# El archivo .env ya está configurado con valores por defecto
# Para producción, cambia estos valores:
cat .env

# Edita valores sensibles si es necesario:
# DJANGO_SECRET_KEY - ¡cámbialo!
# GRAFANA_ADMIN_PASSWORD - ¡cámbialo!
# DB_PASSWORD - ¡cámbialo!
```

### 3. Construir e Iniciar Servicios

```bash
# Construir e iniciar todos los servicios
docker compose up --build

# Salida esperada:
# ✓ postgres_db está saludable
# ✓ django_app está listo
# ✓ prometheus está recopilando métricas
# ✓ grafana está aceptando conexiones
```

**El primer inicio tarda 1-2 minutos. Los servicios estarán listos cuando veas:**
```
django_app | [*] Running on http://0.0.0.0:8000
prometheus | Server is ready to receive web requests
grafana | HTTP Server Listen
```

### 4. Acceder a los Servicios

| Servicio | URL | Credenciales |
|----------|-----|-------------|
| API Django | http://localhost:8000 | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3000 | admin / grafana_secure_pass_456 |
| PostgreSQL | localhost:5432 | postgres / postgres_secure_password_123 |

### 5. Generar Algunas Métricas

```bash
# Hacer requests para generar métricas
# Terminal 1: Generar tráfico continuo
curl http://localhost:8000/api/health/status/ -s | python -m json.tool

# Terminal 2: Simular carga
curl -X POST http://localhost:8000/api/metrics-info/simulate_load/ \
  -H "Content-Type: application/json" \
  -d '{"iterations": 50}'

# Ver métricas disponibles
curl http://localhost:8000/api/metrics-info/list_available/ -s | python -m json.tool
```

### 6. Ver Métricas en Grafana

1. Abre http://localhost:3000
2. Inicia sesión: `admin` / `grafana_secure_pass_456`
3. Ve a **Dashboards** → Selecciona **Django Monitoring Dashboard**
4. Observa las métricas actualizándose en tiempo real

### 7. Detener Servicios

```bash
# Detener y eliminar contenedores
docker compose down

# Detener pero mantener volúmenes (datos persisten)
docker compose stop

# Eliminar todo incluyendo volúmenes
docker compose down -v
```

---

## 🔌 Servicios y Puntos de Acceso

### Aplicación Django

**URL**: http://localhost:8000

**Health Checks**:
```bash
# Probe de liveness (¿está viva la app?)
curl http://localhost:8000/api/health/live/

# Probe de readiness (¿está lista para servir?)
curl http://localhost:8000/api/health/ready/

# Estado de salud completo con métricas
curl http://localhost:8000/api/health/status/ | python -m json.tool
```

**Ejemplo de Respuesta**:
```json
{
  "status": "healthy",
  "timestamp": 1708331000.123,
  "version": "1.0.0",
  "service": "monitoring-dashboard",
  "metrics": {
    "memory_mb": 125.43,
    "cpu_percent": 2.5,
    "database_connections": 1
  },
  "response_time_ms": 15.23
}
```

### Prometheus

**URL**: http://localhost:9090

**Páginas Clave**:
- **Targets**: http://localhost:9090/targets
- **Configuración**: http://localhost:9090/config
- **Service Discovery**: http://localhost:9090/service-discovery

**Ejemplos de Consultas** (PromQL):
```promql
# Requests por segundo
rate(api_requests_total[5m])

# Latencia promedio en ms
histogram_quantile(0.95, rate(api_request_duration_seconds_bucket[5m])) * 1000

# Tasa de error por estatus
rate(api_errors_total[5m])

# Conexiones activas a BD
database_connections_active

# Uso de memoria en MB
application_memory_usage_bytes / 1024 / 1024

# Porcentaje de CPU
application_cpu_percent
```

### Grafana

**URL**: http://localhost:3000

**Credenciales por Defecto**:
- Usuario: `admin`
- Contraseña: `grafana_secure_pass_456`

**Características del Dashboard**:
- Métricas en tiempo real (refresco cada 30s)
- 10+ paneles de visualización
- Estilo profesional (modo oscuro)
- Capacidad de drill-down
- Selección de rango de tiempo (por defecto: última 1 hora)

### Base de Datos PostgreSQL

**Detalles de Conexión**:
```
Host: localhost
Puerto: 5432
Base de datos: monitoring_db
Usuario: postgres
Contraseña: postgres_secure_password_123
```

**Conectar con psql**:
```bash
psql -h localhost -U postgres -d monitoring_db
# Contraseña: postgres_secure_password_123

# Listar tablas
\dt

# Ver migraciones de Django
SELECT * FROM django_migrations;

# Salir
\q
```

---

## 📡 Endpoints de la API

### Endpoints de Salud

```
GET /api/health/live/
- Probe de liveness para Kubernetes/orquestación de contenedores
- Respuesta: {"alive": true}

GET /api/health/ready/
- Probe de readiness (verifica conectividad con BD)
- Respuesta: {"ready": true}

GET /api/health/status/
- Verificación de salud completa con métricas del sistema
- Retorna: memoria, CPU, conexiones BD, tiempo de respuesta
```

### Información de Métricas

```
GET /api/metrics-info/list_available/
- Lista todas las métricas siendo monitoreadas
- Retorna: nombre, tipo, descripción, labels

POST /api/metrics-info/simulate_load/
- Simula carga de la API para pruebas
- Body: {"iterations": 10}
- Útil para probar funcionalidad del dashboard
```

### Endpoint de Prometheus

```
GET /metrics/
- Métricas compatibles con Prometheus en formato OpenMetrics
- Extraído por Prometheus cada 15 segundos
- Contiene:
  - Métricas personalizadas (api_requests_total, etc.)
  - Métricas de Django-Prometheus
  - Métricas del proceso Python
  - Métricas de cliente Go
```

---

## 📊 Métricas Expuestas

### Métricas de Aplicación (Personalizadas)

#### Contadores
| Métrica | Descripción | Labels |
|---------|-------------|--------|
| `api_requests_total` | Total de requests HTTP | method, endpoint, status |
| `api_errors_total` | Total de errores HTTP | method, endpoint, status |

#### Histogramas
| Métrica | Descripción | Labels |
|---------|-------------|--------|
| `api_request_duration_seconds` | Distribución de latencia | method, endpoint |

#### Gauges
| Métrica | Descripción |
|--------|-------------|
| `database_connections_active` | Conexiones activas a BD |
| `application_memory_usage_bytes` | Uso de memoria del proceso |
| `application_cpu_percent` | Porcentaje de CPU del proceso |

### Métricas de Django-Prometheus

| Métrica | Descripción |
|--------|-------------|
| `django_http_requests_total_by_method` | Requests totales por método |
| `django_http_requests_latency_seconds_by_view_method` | Latencia por vista |
| `django_http_response_status_count` | Conteo por código de estatus |
| `django_db_query_count_total` | Queries de BD ejecutadas |

### Métricas del Sistema

| Métrica | Descripción |
|--------|-------------|
| `process_resident_memory_bytes` | Uso de memoria del proceso |
| `process_cpu_seconds_total` | Tiempo de CPU consumido |
| `up` | Si el target está accesible |

---

## 📈 Dashboard y Visualización

### Nombre del Dashboard
**Django Monitoring Dashboard** (UID: `django-monitoring`)

### Paneles Incluidos

1. **Requests por Segundo (promedio 5m)**
   - Tipo: Gráfico de series de tiempo
   - Consulta: `rate(api_requests_total[5m])`
   - Muestra: Volumen de requests en el tiempo

2. **Latencia de Respuesta p95 (ms)**
   - Tipo: Gráfico de series de tiempo
   - Consulta: Cuantil p95 de histograma
   - Muestra: Tendencias de latencia del p95

3. **Tasa de Error por Estatus (promedio 5m)**
   - Tipo: Gráfico de área apilada
   - Consulta: `rate(api_errors_total[5m])`
   - Muestra: Tasa de error desglosada por estatus HTTP

4. **Conexiones Activas a BD**
   - Tipo: Gauge de estadísticas
   - Consulta: `database_connections_active`
   - Umbral: 5 (amarillo), 10 (rojo)

5. **Uso de Memoria (MB)**
   - Tipo: Gráfico de series de tiempo
   - Consulta: Memoria en megabytes
   - Umbral: 500MB (amarillo), 800MB (rojo)

6. **Uso de CPU (%)**
   - Tipo: Gráfico de series de tiempo
   - Consulta: Porcentaje de CPU
   - Umbral: 50% (amarillo), 80% (rojo)

7. **Distribución de Códigos de Estatus (5m)**
   - Tipo: Gráfico circular
   - Muestra: % de respuestas 2xx, 3xx, 4xx, 5xx

8. **Estado de Salud de Servicios**
   - Tipo: Indicadores de estado
   - Muestra: Disponibilidad de Django App y Prometheus

9. **Total de API Requests (ventana 30m)**
   - Tipo: Tabla
   - Muestra: Requests por código de estatus

### Personalizar el Dashboard

Edita: `grafana/dashboards/django-monitoring.json`

```json
// Agregar nuevo panel:
{
  "id": 11,
  "title": "Mi Métrica Personalizada",
  "targets": [
    {
      "expr": "mi_metrica_personalizada",
      "legendFormat": "{{label}}"
    }
  ],
  "type": "timeseries",
  "gridPos": { "h": 8, "w": 12, "x": 0, "y": 32 }
}
```

Luego reinicia Grafana: `docker compose restart grafana`

---

## ⚙️ Configuración

### Variables de Entorno (`.env`)

```bash
# DJANGO
DJANGO_SECRET_KEY=tu-clave-super-secreta-cambiar-en-produccion
DJANGO_DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,django_app,grafana,prometheus

# BASE DE DATOS
DB_NAME=monitoring_db
DB_USER=postgres
DB_PASSWORD=postgres_secure_password_123
DB_HOST=postgres_db
DB_PORT=5432

# GRAFANA
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=grafana_secure_pass_456

# PROMETHEUS
PROMETHEUS_RETENTION=15d
PROMETHEUS_SCRAPE_INTERVAL=15s

# PUERTOS
DJANGO_PORT=8000
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
```

### Configuración de Prometheus

Edita: `prometheus/prometheus.yml`

Configuraciones clave:
```yaml
scrape_interval: 15s          # Cada cuánto tiempo extraer datos
evaluation_interval: 15s      # Frecuencia de evaluación de alertas
retention_time: 15d           # Tiempo de retención de datos

scrape_configs:
  - job_name: 'django_app'
    metrics_path: '/metrics/'
    static_configs:
      - targets: ['django_app:8000']
```

### Configuración de Django

Edita: `config/settings.py`

Configuraciones clave:
- `DEBUG` - Establecer a False en producción
- `ALLOWED_HOSTS` - Agregar tu dominio
- `SECRET_KEY` - Cambiar a valor único aleatorio
- `DATABASES` - Configuración de conexión a PostgreSQL
- `INSTALLED_APPS` - Incluye `django_prometheus`
- `MIDDLEWARE` - PrometheusBeforeMiddleware y PrometheusAfterMiddleware

### Configuración de Docker Compose

Edita: `docker-compose.yml`

Aspectos personalizables:
- Límites de recursos
- Mapeos de puertos
- Montajes de volúmenes
- Intervalos de health check
- Configuración de logging
- Configuración de red

---

## 🏭 Despliegue en Producción

### Checklist Pre-Producción

- [ ] Cambiar todas las contraseñas en `.env`
- [ ] Establecer `DJANGO_DEBUG=False`
- [ ] Generar nueva `DJANGO_SECRET_KEY` (usar módulo `secrets`)
- [ ] Actualizar `ALLOWED_HOSTS` con tu dominio
- [ ] Configurar `CORS_ALLOWED_ORIGINS` correctamente
- [ ] Usar archivo `.env` específico por ambiente
- [ ] Configurar proxy inverso SSL/TLS (Nginx, Traefik)
- [ ] Configurar volúmenes persistentes en almacenamiento de producción
- [ ] Configurar agregación de logs (ELK, Datadog, etc.)
- [ ] Configurar retención de Prometheus según espacio en disco
- [ ] Configurar reglas de alertas en Prometheus
- [ ] Configurar estrategia de backup para PostgreSQL

### Generar Secretos Seguros

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Bash
openssl rand -base64 32
```

### Escalar para Producción

```yaml
# docker-compose.prod.yml
version: '3.9'

services:
  django_app:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '1'
          memory: 512M
    restart_policy:
      condition: on-failure
      delay: 5s
      max_attempts: 3

  postgres_db:
    environment:
      POSTGRES_INITDB_ARGS: >
        -c shared_buffers=512MB
        -c effective_cache_size=2GB
        -c maintenance_work_mem=128MB
        -c checkpoint_completion_target=0.9
        -c wal_buffers=16MB
```

Iniciar stack de producción:
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## 🔧 Resolución de Problemas

### Los servicios no inician

```bash
# Ver logs
docker compose logs django_app
docker compose logs postgres_db
docker compose logs prometheus
docker compose logs grafana

# Ver servicio específico
docker compose logs -f django_app

# Ver estado de Docker
docker ps -a
docker network ls
```

### Prometheus no está extrayendo métricas

```bash
# Ver targets de Prometheus
curl http://localhost:9090/api/v1/targets | python -m json.tool

# Verificar si Django expone métricas
curl http://localhost:8000/metrics/

# Verificar conectividad de red
docker exec -it monitoring_prometheus ping django_app
```

### Dashboard de Grafana vacío

1. **Verificar conexión de datasource**:
   - Grafana → Configuración → Data Sources → Prometheus
   - Click en botón "Test"

2. **Verificar que existan métricas**:
   - Prometheus → Graph
   - Probar consulta: `api_requests_total`

3. **Verificar rango de tiempo**:
   - Dashboard → Establecer a "Últimos 5 minutos"
   - Asegurar que hay datos recientes

4. **Reiniciar Grafana**:
   ```bash
   docker compose restart grafana
   ```

### Errores de conexión a BD

```bash
# Verificar que PostgreSQL está corriendo
docker ps | grep postgres

# Ver logs de PostgreSQL
docker compose logs postgres_db

# Conectar a PostgreSQL
docker exec -it monitoring_postgres psql -U postgres -d monitoring_db

# Ver migraciones de Django
docker compose exec django_app python manage.py showmigrations
```

### Alto uso de memoria

```bash
# Ver cuál servicio consume memoria
docker stats

# Reducir retención de Prometheus
# Edita docker-compose.yml, cambia parámetro de retención:
# '--storage.tsdb.retention.time=7d'

# Reiniciar
docker compose down && docker compose up -d
```

### Puerto ya está en uso

```bash
# Encontrar qué proceso usa puerto 8000
lsof -i :8000
# O (Windows)
netstat -ano | findstr :8000

# Cambiar puerto en .env y docker-compose.yml
```

---

## 📚 Justificación de Arquitectura

### ¿Por Qué Estas Tecnologías?

**Django**
- Framework maduro y probado en producción
- Excelente ORM y soporte de bases de datos
- Ecosistema fuerte y comunidad activa
- Interfaz admin integrada para gestión de datos

**Prometheus**
- Estándar de la industria para recopilación de métricas
- Base de datos de series temporales optimizada para monitoreo
- Lenguaje PromQL (potente y flexible)
- Integración excelente con Grafana

**Grafana**
- Plataforma de visualización open-source líder
- Dashboards hermosos e interactivos
- Capacidades de integración de alertas
- Soporte multi-usuario con autenticación

**PostgreSQL**
- Base de datos relacional confiable
- Cumplimiento ACID para integridad de datos
- Capacidades ricas de consultas
- Excelente soporte de ORM de Django

**Docker & Docker Compose**
- Infraestructura como Código
- Ambientes reproducibles
- Despliegue y escalado fácil
- Estándar de la industria para containerización

### Mejores Prácticas DevOps Demostradas

✅ **Infraestructura como Código** - Todo definido en YAML/Docker
✅ **Separación de Ambientes** - .env para configuración, no hardcodeada
✅ **Health Checks** - Todos los servicios tienen probes de disponibilidad
✅ **Logging Estructurado** - Logging JSON a stdout
✅ **Seguridad** - Usuario no-root, sin secretos hardcodeados
✅ **Modularidad** - Servicios separados con límites claros
✅ **Observabilidad** - Métricas reales, no datos sintéticos
✅ **Automatización** - Un comando para desplegar toda la pila
✅ **Escalabilidad** - Lista para Kubernetes o Docker Swarm
✅ **Documentación** - Comentarios inline y README completo

---

## 📁 Estructura del Proyecto

```
Docker/
├── Dockerfile                          # Build multi-stage para Django
├── docker-compose.yml                  # Orquestación de servicios
├── manage.py                           # Script de gestión de Django
├── requirements.txt                    # Dependencias Python
├── .env                                # Variables de entorno
├── .gitignore                          # Reglas de Git
├── README.md                           # Este archivo
│
├── config/                             # Configuración de Django
│   ├── __init__.py
│   ├── settings.py                     # Configuración de Django (lista para producción)
│   ├── urls.py                         # Enrutamiento de URLs
│   └── wsgi.py                         # Aplicación WSGI
│
├── api/                                # Aplicación API de Django
│   ├── __init__.py
│   ├── admin.py                        # Configuración admin de Django
│   ├── apps.py                         # Configuración de app
│   ├── models.py                       # Modelos de base de datos
│   ├── views.py                        # Viewsets de API con métricas
│   └── serializers.py                  # Serializadores DRF
│
├── prometheus/                         # Configuración de Prometheus
│   └── prometheus.yml                  # Configuración de scrape, definición de jobs
│
├── grafana/                            # Configuración de Grafana
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── prometheus.yml          # Configuración de datasource
│   │   └── dashboards/
│   │       └── dashboards.yml          # Provisión de dashboards
│   └── dashboards/
│       └── django-monitoring.json      # Dashboard principal (10+ paneles)
│
└── postgres/                           # Inicialización de PostgreSQL
    └── init.sql                        # Script de setup de BD
```

---

## 🧪 Pruebas y Validación

### Verificar que Todos los Servicios Iniciaron Correctamente

```bash
# Ver todos los contenedores
docker compose ps

# Salida esperada:
# NAME              STATUS
# monitoring_postgres   Up (healthy)
# monitoring_django     Up (healthy)
# monitoring_prometheus Up (healthy)
# monitoring_grafana    Up (healthy)
```

### Probar Cada Servicio

```bash
# 1. API Django
curl http://localhost:8000/api/health/status/

# 2. Métricas de Prometheus
curl http://localhost:8000/metrics/ | head -20

# 3. Prometheus UI
curl http://localhost:9090/-/healthy

# 4. Grafana
curl http://localhost:3000/api/health

# 5. PostgreSQL
docker exec -it monitoring_postgres pg_isready -U postgres
```

### Prueba de Carga y Monitoreo

```bash
# Terminal 1: Generador de carga
while true; do
  curl -X POST http://localhost:8000/api/metrics-info/simulate_load/ \
    -H "Content-Type: application/json" \
    -d '{"iterations": 20}' 2>/dev/null
  sleep 5
done

# Terminal 2: Ver métricas en tiempo real
watch -n 1 'curl -s http://localhost:8000/api/health/status/ | python -m json.tool'

# Terminal 3: Abrir Grafana en navegador
# http://localhost:3000
# Ver cómo se actualizan los paneles en tiempo real
```

---

## 🔐 Consideraciones de Seguridad

### Implementación Actual
- ✅ Usuario no-root en Docker
- ✅ Variables de entorno para secretos
- ✅ Health checks y políticas de reinicio
- ✅ Aislamiento de red (bridge de Docker)

### Recomendaciones para Producción
- ⚠️ Usar gestión de secretos (HashiCorp Vault, AWS Secrets Manager)
- ⚠️ Agregar proxy inverso (Nginx) con SSL/TLS
- ⚠️ Implementar rate limiting
- ⚠️ Agregar autenticación a Prometheus/Grafana
- ⚠️ Actualizaciones de seguridad regulares
- ⚠️ Backups de BD y recuperación ante desastres
- ⚠️ Políticas de red y firewalls
- ⚠️ Protección contra DDoS y WAF

---

## 📞 Contacto y Autor

**Desarrollador**: Isaac Esteban Haro Torres

- 📧 **Email**: zackharo1@gmail.com
- 💬 **WhatsApp**: 098805517
- 💻 **GitHub**: https://github.com/ieharo1
- 🌐 **Portafolio**: https://ieharo1.github.io/portafolio-isaac.haro/

© 2026 Isaac Esteban Haro Torres - Todos los derechos reservados

---

## 📄 Licencia

Este proyecto se proporciona tal cual para fines educativos y profesionales.

---

## 🚀 Próximos Pasos

Después de que el setup básico esté funcionando:

1. **Agregar Métricas Personalizadas** - Extender `api/views.py` con métricas de negocio
2. **Configurar Alertas** - Crear reglas de alertas en `prometheus/alert_rules.yml`
3. **Agregar Autenticación** - Implementar OAuth2/JWT para endpoints
4. **Setup de Backups** - Automatizar backups de base de datos
5. **Despliegue en Producción** - Usar Kubernetes o plataforma cloud
6. **Agregar APM** - Integrar Jaeger o Datadog para tracing distribuido
7. **Escalar Horizontalmente** - Agregar múltiples replicas de Django con load balancer

---

**Última Actualización**: 19 de Febrero de 2026
**Versión**: 1.0.0
**Estado**: ✅ Listo para Producción
