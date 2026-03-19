# 🚀 Deployment Guide

Guía completa para desplegar el modelo de machine learning en diferentes entornos.

## 📋 Tabla de Contenidos

- [Pre-requisitos](#pre-requisitos)
- [Configuración de Entorno](#configuración-de-entorno)
- [Despliegue Local](#despliegue-local)
- [Despliegue en Staging](#despliegue-en-staging)
- [Despliegue en Producción](#despliegue-en-producción)
- [API Endpoints](#api-endpoints)
- [Monitoreo Post-Despliegue](#monitoreo-post-despliegue)
- [Rollback](#rollback)
- [Troubleshooting](#troubleshooting)

---

## Pre-requisitos

### Software Requerido

- **Python**: 3.11+
- **Docker**: 20.10+
- **Kubernetes**: 1.25+ (para producción)
- **Git**: 2.30+

### Dependencias del Proyecto

```bash
pip install -r requirements.txt
```

### Variables de Entorno Requeridas

Crear un archivo `.env` con las siguientes variables:

```bash
# Modelo
MODEL_PATH=/path/to/model.pkl
MODEL_VERSION=1.0.0

# Base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ml_db
DB_USER=ml_user
DB_PASSWORD=secure_password

# API
API_KEY_SECRET=your_secret_key_here
ALLOWED_ORIGINS=http://localhost:3000,https://app.empresa.com

# Monitoreo
PROMETHEUS_ENABLED=true
GRAFANA_URL=https://grafana.empresa.com

# Notificaciones
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### Accesos Necesarios

- [ ] Acceso al repositorio de modelos (S3/GCS/Azure Blob)
- [ ] Credenciales de base de datos
- [ ] API keys para servicios externos
- [ ] Acceso al cluster de Kubernetes (producción)
- [ ] Permisos en el registry de Docker

---

## Configuración de Entorno

### 1. Clonar el Repositorio

```bash
git clone https://github.com/empresa/ml-churn-predictor.git
cd ml-churn-predictor
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Descargar el Modelo

```bash
# Desde S3
aws s3 cp s3://ml-models/churn-predictor/v1.0.0/model.pkl models/

# O desde el registro interno
python scripts/download_model.py --version 1.0.0
```

### 5. Configurar Variables de Entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales
```

---

## Despliegue Local

### Opción 1: Servidor de Desarrollo

```bash
# Iniciar servidor FastAPI
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Acceder a:
- API: http://localhost:8000
- Documentación interactiva: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

### Opción 2: Docker Local

```bash
# Construir imagen
docker build -t churn-predictor:local .

# Ejecutar contenedor
docker run -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/models:/app/models \
  churn-predictor:local
```

### Verificar Funcionamiento

```bash
# Health check
curl http://localhost:8000/health

# Predicción de prueba
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{
    "edad": 35,
    "ingreso_mensual": 50000,
    "score_crediticio": 720,
    "num_productos": 2,
    "antiguedad_meses": 24
  }'
```

---

## Despliegue en Staging

### 1. Construir y Subir Imagen Docker

```bash
# Tag de staging
VERSION=1.0.0
REGISTRY=registry.empresa.com

# Build
docker build -t ${REGISTRY}/ml-models/churn-predictor:${VERSION}-staging .

# Push
docker push ${REGISTRY}/ml-models/churn-predictor:${VERSION}-staging
```

### 2. Desplegar en Kubernetes (Staging)

```bash
# Aplicar configuración
kubectl apply -f k8s/staging/

# Verificar deployment
kubectl get pods -n ml-staging
kubectl logs -f deployment/churn-predictor -n ml-staging

# Verificar servicio
kubectl get svc -n ml-staging
```

### 3. Pruebas de Integración

```bash
# Ejecutar suite de tests
pytest tests/integration/ --env=staging

# Pruebas de carga
locust -f tests/load/locustfile.py --host=https://staging-api.empresa.com
```

### 4. Validación de Métricas

Verificar en Grafana:
- Latencia < 50ms (p95)
- Error rate < 1%
- Throughput > 100 req/s

---

## Despliegue en Producción

### Pre-Deployment Checklist

- [ ] Todos los tests pasan en staging
- [ ] Métricas de performance validadas
- [ ] Documentación actualizada
- [ ] Configuración de alertas verificada
- [ ] Plan de rollback preparado
- [ ] Stakeholders notificados
- [ ] Ventana de mantenimiento aprobada

### 1. Crear Release Tag

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 2. Build de Producción

```bash
# Build con optimizaciones
docker build \
  --build-arg ENV=production \
  --build-arg VERSION=1.0.0 \
  -t ${REGISTRY}/ml-models/churn-predictor:1.0.0 \
  -t ${REGISTRY}/ml-models/churn-predictor:latest \
  .

# Push
docker push ${REGISTRY}/ml-models/churn-predictor:1.0.0
docker push ${REGISTRY}/ml-models/churn-predictor:latest
```

### 3. Despliegue Canary (Recomendado)

```bash
# Desplegar versión canary (10% del tráfico)
kubectl apply -f k8s/production/canary/

# Monitorear métricas por 30 minutos
# Si todo OK, incrementar tráfico gradualmente

# 50% tráfico
kubectl patch deployment churn-predictor-canary \
  -n ml-production \
  --patch '{"spec":{"replicas":5}}'

# 100% tráfico (full rollout)
kubectl apply -f k8s/production/
```

### 4. Despliegue Blue-Green (Alternativa)

```bash
# Desplegar nueva versión (green)
kubectl apply -f k8s/production/green/

# Verificar que green está healthy
kubectl get pods -n ml-production -l version=green

# Switch de tráfico
kubectl patch service churn-predictor \
  -n ml-production \
  --patch '{"spec":{"selector":{"version":"green"}}}'

# Mantener blue por 24h para posible rollback
```

### 5. Verificación Post-Despliegue

```bash
# Smoke tests
pytest tests/smoke/ --env=production

# Verificar métricas en tiempo real
# - Dashboard: https://grafana.empresa.com/d/model-production
# - Logs: https://kibana.empresa.com/app/logs

# Verificar alertas configuradas
curl https://prometheus.empresa.com/api/v1/rules
```

---

## API Endpoints

### Health Check

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model_version": "1.0.0",
  "uptime_seconds": 3600
}
```

### Predicción Individual

```bash
POST /predict
Content-Type: application/json
X-API-Key: your_api_key

{
  "edad": 35,
  "ingreso_mensual": 50000,
  "score_crediticio": 720,
  "num_productos": 2,
  "antiguedad_meses": 24
}
```

**Response:**
```json
{
  "prediction": 0,
  "prediction_label": "no_churn",
  "confidence": 0.87,
  "model_version": "1.0.0",
  "timestamp": "2024-03-15T10:30:00Z"
}
```

### Predicción por Lotes

```bash
POST /predict/batch
Content-Type: application/json
X-API-Key: your_api_key

{
  "instances": [
    {"edad": 35, "ingreso_mensual": 50000, ...},
    {"edad": 42, "ingreso_mensual": 75000, ...}
  ]
}
```

### Información del Modelo

```bash
GET /model/info
```

**Response:**
```json
{
  "name": "churn_predictor",
  "version": "1.0.0",
  "algorithm": "RandomForest",
  "trained_at": "2024-03-15T10:00:00Z",
  "metrics": {
    "accuracy": 0.89,
    "precision": 0.85,
    "recall": 0.82
  }
}
```

### Métricas (Prometheus)

```bash
GET /metrics
```

---

## Monitoreo Post-Despliegue

### Dashboards Principales

1. **Model Performance**
   - URL: https://grafana.empresa.com/d/model-performance
   - Métricas: Accuracy, Precision, Recall, F1
   - Alertas configuradas

2. **System Health**
   - URL: https://grafana.empresa.com/d/system-health
   - Latencia, throughput, error rate
   - Uso de recursos

3. **Data Quality**
   - URL: https://grafana.empresa.com/d/data-quality
   - Data drift, feature distributions
   - Missing values

### Alertas Críticas

Configuradas en `docs/config/monitoring_config.yaml`:

- Error rate > 5% → PagerDuty + Slack
- Latency p95 > 1s → Slack warning
- Model accuracy drop > 5% → Email + Slack

### Logs

```bash
# Kubernetes logs
kubectl logs -f deployment/churn-predictor -n ml-production

# Elasticsearch/Kibana
https://kibana.empresa.com/app/logs

# Filtrar por errores
kubectl logs deployment/churn-predictor -n ml-production | grep ERROR
```

---

## Rollback

### Rollback Automático

Configurado en `deployment_config.yaml`:
- Error rate > 10% → Rollback automático
- Health check failures > 5 → Rollback automático

### Rollback Manual

#### Opción 1: Kubernetes Rollback

```bash
# Ver historial de deployments
kubectl rollout history deployment/churn-predictor -n ml-production

# Rollback a versión anterior
kubectl rollout undo deployment/churn-predictor -n ml-production

# Rollback a versión específica
kubectl rollout undo deployment/churn-predictor \
  -n ml-production \
  --to-revision=3
```

#### Opción 2: Blue-Green Rollback

```bash
# Switch de vuelta a blue
kubectl patch service churn-predictor \
  -n ml-production \
  --patch '{"spec":{"selector":{"version":"blue"}}}'
```

#### Opción 3: Canary Rollback

```bash
# Eliminar canary deployment
kubectl delete -f k8s/production/canary/

# Escalar deployment estable
kubectl scale deployment churn-predictor-stable \
  -n ml-production \
  --replicas=10
```

### Post-Rollback

1. Investigar causa raíz
2. Documentar en incident report
3. Crear issue para fix
4. Actualizar tests para prevenir regresión

---

## Troubleshooting

### Problema: Alta Latencia

**Síntomas:**
- p95 latency > 1s
- Timeouts en requests

**Diagnóstico:**
```bash
# Verificar recursos
kubectl top pods -n ml-production

# Verificar logs
kubectl logs deployment/churn-predictor -n ml-production | grep "slow"

# Profiling
python -m cProfile -o profile.stats src/api/main.py
```

**Soluciones:**
- Escalar horizontalmente: `kubectl scale deployment churn-predictor --replicas=10`
- Optimizar modelo: Reducir features, usar modelo más ligero
- Agregar caché: Redis para predicciones frecuentes

### Problema: Errores 500

**Diagnóstico:**
```bash
# Ver logs de errores
kubectl logs deployment/churn-predictor -n ml-production --tail=100 | grep ERROR

# Verificar health check
curl https://api.empresa.com/health
```

**Soluciones:**
- Verificar variables de entorno
- Verificar conexión a base de datos
- Verificar que el modelo existe en el path correcto

### Problema: Data Drift Detectado

**Síntomas:**
- Alertas de drift en Slack
- Degradación de métricas

**Acciones:**
1. Revisar dashboard de data quality
2. Comparar distribuciones: actual vs. training
3. Evaluar necesidad de reentrenamiento
4. Documentar en `experimentation_log.md`

### Problema: OOM (Out of Memory)

**Diagnóstico:**
```bash
kubectl describe pod <pod-name> -n ml-production
```

**Soluciones:**
- Aumentar límites de memoria en deployment
- Reducir batch size
- Optimizar uso de memoria en código

---

## Contactos y Soporte

- **ML Team Lead**: ml-lead@empresa.com
- **DevOps Team**: devops@empresa.com
- **On-call**: PagerDuty rotation
- **Slack**: #ml-support

## Referencias

- [Configuración de Deployment](config/deployment_config.yaml)
- [Configuración de Monitoring](config/monitoring_config.yaml)
- [Model Card](model_card.md)
- [Runbook de Incidentes](runbook.md)
