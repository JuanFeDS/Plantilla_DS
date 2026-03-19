# 📊 Model Monitoring Guide

Guía completa de monitoreo y observabilidad del modelo en producción.

## 📋 Tabla de Contenidos

- [Resumen](#resumen)
- [Métricas Monitoreadas](#métricas-monitoreadas)
- [Dashboards](#dashboards)
- [Alertas](#alertas)
- [Data Drift Detection](#data-drift-detection)
- [Concept Drift Detection](#concept-drift-detection)
- [Feedback Loop](#feedback-loop)
- [Reportes Automáticos](#reportes-automáticos)
- [Runbook de Incidentes](#runbook-de-incidentes)

---

## Resumen

Este documento describe el sistema de monitoreo del modelo en producción. Toda la configuración técnica está en [`config/monitoring_config.yaml`](config/monitoring_config.yaml).

### Objetivos del Monitoreo

- **Detectar degradación** de rendimiento del modelo
- **Identificar drift** en datos o conceptos
- **Garantizar SLAs** de latencia y disponibilidad
- **Facilitar debugging** y troubleshooting
- **Automatizar alertas** a equipos relevantes

---

## Métricas Monitoreadas

### 1. Métricas de Rendimiento del Modelo

Evaluadas cada hora sobre ventana de 24h:

| Métrica    | Threshold Min | Threshold Max | Acción si Breach     |
|------------|---------------|---------------|----------------------|
| Accuracy   | 0.85          | 1.0           | Alert + Investigation|
| Precision  | 0.80          | 1.0           | Alert                |
| Recall     | 0.78          | 1.0           | Alert                |
| F1 Score   | 0.80          | 1.0           | Alert                |
| AUC-ROC    | 0.88          | 1.0           | Alert + Investigation|

**Dashboard**: https://grafana.empresa.com/d/model-performance

### 2. Métricas de Sistema

Evaluadas en tiempo real:

| Métrica              | P50    | P95    | P99    | Acción si Breach |
|----------------------|--------|--------|--------|------------------|
| Latencia (ms)        | < 10   | < 25   | < 50   | Scale up         |
| Throughput (req/s)   | > 10   | -      | -      | Alert            |
| Error Rate (%)       | -      | < 1    | < 5    | Critical alert   |
| CPU Usage (%)        | -      | < 80   | < 90   | Scale up         |
| Memory Usage (%)     | -      | < 85   | < 95   | Scale up         |

**Dashboard**: https://grafana.empresa.com/d/system-health

### 3. Métricas de Predicciones

| Métrica                        | Threshold              | Acción              |
|--------------------------------|------------------------|---------------------|
| Avg Confidence                 | > 0.70                 | Alert si < 0.70     |
| Low Confidence Predictions (%) | < 20%                  | Alert si > 20%      |
| Class 0 Distribution (%)       | 60-80%                 | Alert si fuera      |
| Class 1 Distribution (%)       | 20-40%                 | Alert si fuera      |

**Dashboard**: https://grafana.empresa.com/d/predictions

---

## Dashboards

### Dashboard 1: Model Performance

**URL**: https://grafana.empresa.com/d/model-performance

**Paneles**:
- Accuracy over time (24h, 7d, 30d)
- Precision/Recall curves
- Confusion matrix (actualizado cada hora)
- ROC curve
- Feature importance drift

**Refresh**: 5 minutos

### Dashboard 2: System Health

**URL**: https://grafana.empresa.com/d/system-health

**Paneles**:
- Request rate (req/s)
- Latency percentiles (p50, p95, p99)
- Error rate (%)
- HTTP status codes distribution
- CPU/Memory usage
- Pod status

**Refresh**: 30 segundos

### Dashboard 3: Data Quality

**URL**: https://grafana.empresa.com/d/data-quality

**Paneles**:
- Missing values % por feature
- Feature distributions
- Data drift scores (KS test)
- Outlier detection
- Schema violations

**Refresh**: 1 hora

### Dashboard 4: Business Metrics

**URL**: https://grafana.empresa.com/d/business-metrics

**Paneles**:
- Predicciones por día
- Tasa de churn predicha
- Impacto estimado ($)
- Campañas activadas
- ROI del modelo

**Refresh**: 1 día

---

## Alertas

### Configuración de Canales

**Critical** → PagerDuty + Slack (#ml-critical-alerts)
**Warning** → Slack (#ml-alerts) + Email
**Info** → Slack (#ml-monitoring)

### Reglas de Alertas

#### 1. Performance Degradation (Critical)

```yaml
- name: model_accuracy_drop
  condition: accuracy < 0.85 OR accuracy_drop > 5%
  severity: critical
  window: 1h
  channels: [pagerduty, slack_critical]
  runbook: docs/runbooks/performance_degradation.md
```

**Acción**: 
1. Revisar dashboard de performance
2. Comparar con baseline
3. Verificar data drift
4. Evaluar rollback si degradación > 10%

#### 2. High Latency (Warning)

```yaml
- name: high_latency_p95
  condition: latency_p95 > 1000ms
  severity: warning
  window: 10m
  channels: [slack]
```

**Acción**:
1. Verificar carga del sistema
2. Revisar logs de errores
3. Considerar escalado horizontal

#### 3. Data Drift Detected (Warning)

```yaml
- name: data_drift_ks_test
  condition: ks_test_p_value < 0.05
  severity: warning
  window: 24h
  channels: [slack, email]
```

**Acción**:
1. Revisar distribuciones en dashboard
2. Documentar en experimentation_log.md
3. Evaluar reentrenamiento

#### 4. High Error Rate (Critical)

```yaml
- name: high_error_rate
  condition: error_rate > 5%
  severity: critical
  window: 5m
  channels: [pagerduty, slack_critical]
```

**Acción**:
1. Revisar logs inmediatamente
2. Verificar health checks
3. Considerar rollback automático

#### 5. Low Confidence Predictions (Warning)

```yaml
- name: low_confidence_predictions
  condition: avg_confidence < 0.7 OR low_conf_pct > 20%
  severity: warning
  window: 1h
  channels: [slack]
```

**Acción**:
1. Revisar features de entrada
2. Verificar data quality
3. Analizar casos de baja confianza

---

## Data Drift Detection

### Métodos Implementados

#### 1. Kolmogorov-Smirnov Test

Para features numéricas:

```python
from scipy import stats

def detect_drift_ks(current_data, reference_data, feature):
    """Detecta drift usando KS test."""
    ks_stat, p_value = stats.ks_2samp(
        current_data[feature].dropna(),
        reference_data[feature].dropna()
    )
    
    drift_detected = p_value < 0.05
    
    return {
        'feature': feature,
        'ks_statistic': ks_stat,
        'p_value': p_value,
        'drift_detected': drift_detected
    }
```

**Threshold**: p-value < 0.05
**Features monitoreadas**: edad, ingreso_mensual, score_crediticio

#### 2. Population Stability Index (PSI)

Para features categóricas:

```python
def calculate_psi(current_data, reference_data, feature):
    """Calcula PSI para detectar drift en categóricas."""
    current_dist = current_data[feature].value_counts(normalize=True)
    reference_dist = reference_data[feature].value_counts(normalize=True)
    
    psi = 0
    for category in reference_dist.index:
        current_pct = current_dist.get(category, 0.0001)
        reference_pct = reference_dist.get(category, 0.0001)
        psi += (current_pct - reference_pct) * np.log(current_pct / reference_pct)
    
    drift_detected = psi > 0.25
    
    return {
        'feature': feature,
        'psi': psi,
        'drift_detected': drift_detected
    }
```

**Threshold**: PSI > 0.25
**Features monitoreadas**: genero, num_productos

#### 3. Jensen-Shannon Divergence

Para todas las features:

```python
from scipy.spatial.distance import jensenshannon

def calculate_js_divergence(current_data, reference_data, feature):
    """Calcula JS divergence."""
    # Crear histogramas
    current_hist, _ = np.histogram(current_data[feature].dropna(), bins=30, density=True)
    reference_hist, _ = np.histogram(reference_data[feature].dropna(), bins=30, density=True)
    
    js_div = jensenshannon(current_hist, reference_hist)
    drift_detected = js_div > 0.1
    
    return {
        'feature': feature,
        'js_divergence': js_div,
        'drift_detected': drift_detected
    }
```

**Threshold**: JS > 0.1

### Frecuencia de Checks

- **Datos en tiempo real**: Cada hora
- **Comparación con baseline**: Diario
- **Reporte completo**: Semanal

### Dashboard de Drift

**URL**: https://grafana.empresa.com/d/data-drift

Visualiza:
- Drift scores por feature
- Distribuciones: actual vs. baseline
- Timeline de drift detectado
- Features con mayor drift

---

## Concept Drift Detection

### Métodos Implementados

#### 1. ADWIN (Adaptive Windowing)

Detecta cambios en la distribución de predicciones vs. ground truth:

```python
from river import drift

detector = drift.ADWIN()

for prediction, actual in zip(predictions, actuals):
    error = int(prediction != actual)
    detector.update(error)
    
    if detector.drift_detected:
        logger.warning(f"Concept drift detected at index {i}")
        send_alert("Concept drift detected")
```

#### 2. Page-Hinkley Test

Detecta cambios en la media de errores:

```python
detector = drift.PageHinkley(threshold=50, alpha=0.9999)

for error in errors:
    detector.update(error)
    
    if detector.drift_detected:
        logger.warning("Concept drift detected (Page-Hinkley)")
```

### Acción al Detectar Concept Drift

1. **Inmediato**: Alertar a equipo ML
2. **Corto plazo** (24h): Analizar causa raíz
3. **Mediano plazo** (1 semana): Evaluar reentrenamiento
4. **Documentar**: En `experimentation_log.md`

---

## Feedback Loop

### Recolección de Ground Truth

**Fuente**: `database.feedback_table`
**Delay**: 30 días (tiempo hasta conocer resultado real)

```python
def collect_ground_truth():
    """Recolecta ground truth para predicciones pasadas."""
    query = """
    SELECT 
        p.prediction_id,
        p.customer_id,
        p.predicted_class,
        p.predicted_proba,
        p.prediction_timestamp,
        f.actual_churn,
        f.feedback_timestamp
    FROM predictions p
    JOIN feedback f ON p.customer_id = f.customer_id
    WHERE f.feedback_timestamp >= NOW() - INTERVAL '30 days'
    """
    
    return pd.read_sql(query, db_connection)
```

### Comparación Predicción vs. Realidad

Ejecutado semanalmente:

```python
def evaluate_production_performance(predictions_with_truth):
    """Evalúa rendimiento real del modelo."""
    from sklearn.metrics import accuracy_score, precision_score, recall_score
    
    metrics = {
        'accuracy': accuracy_score(
            predictions_with_truth['actual_churn'],
            predictions_with_truth['predicted_class']
        ),
        'precision': precision_score(
            predictions_with_truth['actual_churn'],
            predictions_with_truth['predicted_class']
        ),
        'recall': recall_score(
            predictions_with_truth['actual_churn'],
            predictions_with_truth['predicted_class']
        )
    }
    
    # Comparar con baseline
    baseline_metrics = load_baseline_metrics()
    
    for metric, value in metrics.items():
        degradation = (baseline_metrics[metric] - value) / baseline_metrics[metric] * 100
        
        if degradation > 5:
            logger.warning(f"{metric} degradation: {degradation:.2f}%")
            send_alert(f"Performance degradation detected: {metric}")
    
    return metrics
```

### Triggers de Reentrenamiento

Configurados en `monitoring_config.yaml`:

1. **Accuracy drop > 5%** → Notificar equipo
2. **Data drift detected** → Programar reentrenamiento
3. **Nuevos datos etiquetados > 10,000** → Evaluar reentrenamiento
4. **Concept drift detectado** → Reentrenamiento urgente

---

## Reportes Automáticos

### Reporte Diario

**Hora**: 09:00 UTC
**Destinatarios**: ml-team@empresa.com
**Contenido**:
- Volumen de predicciones
- Confianza promedio
- Error rate
- Latencia summary

### Reporte Semanal

**Día**: Lunes 09:00 UTC
**Destinatarios**: ml-team@empresa.com, stakeholders@empresa.com
**Contenido**:
- Métricas de performance
- Análisis de data drift
- Cambios en feature importance
- Métricas de negocio

### Reporte Mensual

**Día**: Primer día del mes, 09:00 UTC
**Destinatarios**: ml-team@empresa.com, management@empresa.com
**Contenido**:
- Review comprehensivo de performance
- Recomendaciones de reentrenamiento
- Análisis de costos
- ROI metrics

---

## Runbook de Incidentes

### Incidente: Model Performance Degradation

**Síntomas**:
- Accuracy < 0.85
- Alerta crítica en Slack/PagerDuty

**Diagnóstico**:
1. Revisar dashboard de performance
2. Comparar métricas con baseline
3. Verificar data drift
4. Revisar logs de errores

**Acciones**:
1. Si degradación < 5%: Monitorear de cerca
2. Si degradación 5-10%: Investigar causa, preparar reentrenamiento
3. Si degradación > 10%: Considerar rollback inmediato

**Documentación**: Crear incident report en `docs/incidents/`

### Incidente: High Latency

**Síntomas**:
- P95 latency > 1s
- Timeouts en requests

**Diagnóstico**:
```bash
# Verificar recursos
kubectl top pods -n ml-production

# Verificar logs
kubectl logs deployment/churn-predictor -n ml-production | grep "slow"
```

**Acciones**:
1. Escalar horizontalmente
2. Verificar queries a DB
3. Revisar tamaño de batch
4. Considerar caché

### Incidente: Data Drift Detected

**Síntomas**:
- KS test p-value < 0.05
- Alerta de drift en Slack

**Diagnóstico**:
1. Revisar dashboard de drift
2. Comparar distribuciones
3. Verificar fuente de datos

**Acciones**:
1. Documentar en `experimentation_log.md`
2. Evaluar impacto en modelo
3. Programar reentrenamiento si necesario
4. Notificar a data engineering si es problema de datos

---

## Referencias

- [Monitoring Config YAML](config/monitoring_config.yaml)
- [Deployment Guide](deployment.md)
- [Data Quality Guide](data_quality.md)
- [Model Card](model_card.md)

## Contacto

- **ML Team**: ml-team@empresa.com
- **On-call**: PagerDuty rotation
- **Slack**: #ml-monitoring
