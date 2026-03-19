# 🌐 Data Sources

Catálogo de fuentes de datos utilizadas en el proyecto.

## Fuentes Principales

| Fuente | Descripción | Formato | Actualización | Origen / API | URL/Path | Responsable | SLA |
|--------|-------------|---------|---------------|--------------|----------|-------------|-----|
| CRM_Clientes | Información personal y de contacto | CSV | Mensual | Base interna (BI) | `s3://data/crm/clientes/` | data-eng@empresa.com | 99.5% |
| Logs_App | Eventos de navegación y uso de app | Parquet | Diario | Google BigQuery | `project.dataset.logs_app` | analytics@empresa.com | 99.9% |
| Encuestas_NPS | Resultados de encuestas NPS | Excel | Trimestral | SharePoint externo | `https://sharepoint.com/nps/` | marketing@empresa.com | 95% |

## Detalles por Fuente

### CRM_Clientes

**Descripción completa**: Base de datos de clientes con información demográfica, contacto y productos contratados.

**Acceso**:
- Credenciales: Vault path `secret/data/crm_readonly`
- Permisos necesarios: `crm_reader` role
- Documentación: [Link interno](https://wiki.empresa.com/crm)

**Schema**:
- Ver: `docs/config/data_schema.yaml`
- Versión: 2.1
- Última modificación: 2024-01-15

**Calidad de datos**:
- Completitud: 95%
- Duplicados: < 0.1%
- Validaciones: Automáticas diarias

**Contacto**:
- Responsable técnico: data-eng@empresa.com
- Product owner: crm-team@empresa.com
- Slack: #data-crm

### Logs_App

**Descripción completa**: Eventos de interacción de usuarios con la aplicación móvil y web.

**Acceso**:
- Proyecto GCP: `empresa-analytics`
- Dataset: `app_events`
- Tabla: `logs_app`
- Query example: `SELECT * FROM \`project.dataset.logs_app\` WHERE date >= '2024-01-01'`

**Schema**:
- Campos principales: user_id, event_type, timestamp, properties (JSON)
- Particionado por: date
- Clustering por: user_id

**Procesamiento requerido**:
- ⚠️ Requiere agregación por cliente antes de usar
- Usar pipeline de datos: `src.pipelines.data_pipeline.DataPipeline`
- Tiempo de procesamiento estimado: ~30 min para 1 mes de datos

**Calidad de datos**:
- Completitud: 98%
- Latencia: < 1 hora
- Retención: 2 años

**Contacto**:
- Responsable técnico: analytics@empresa.com
- Slack: #analytics-support

### Encuestas_NPS

**Descripción completa**: Resultados de encuestas de satisfacción Net Promoter Score.

**Acceso**:
- URL: `https://sharepoint.empresa.com/sites/marketing/nps/`
- Autenticación: SSO corporativo
- Archivo más reciente: `NPS_Q{quarter}_{year}.xlsx`

**Schema**:
- Hojas: Respuestas, Metadata, Análisis
- Campos clave: cliente_id, score, fecha_respuesta, comentarios

**Procesamiento requerido**:
- ⚠️ Fechas en formato DD/MM/YY, convertir a YYYY-MM-DD
- ⚠️ Encoding: Latin-1, convertir a UTF-8
- Usar funciones de preprocesamiento: `src.data.preprocessing`

**Calidad de datos**:
- Tasa de respuesta: ~15%
- Completitud: 80% (comentarios opcionales)

**Contacto**:
- Responsable: marketing@empresa.com
- Slack: #marketing-analytics

## Fuentes Secundarias

| Fuente | Descripción | Frecuencia | Contacto |
|--------|-------------|------------|----------|
| Transacciones | Historial de compras | Tiempo real | payments@empresa.com |
| Soporte | Tickets de atención | Diario | support@empresa.com |
| Redes Sociales | Menciones y sentimiento | Semanal | social@empresa.com |

## Problemas Conocidos

### CRM_Clientes
- **Issue #123**: Duplicados ocasionales en migraciones mensuales
  - Workaround: Deduplicar por `id_cliente` + `fecha_actualizacion`
  - ETA fix: 2024-Q2

- **Issue #145**: Campo `ingreso_mensual` con ~20% missing
  - Causa: No obligatorio en formulario de registro
  - Mitigación: Imputación por segmento

### Logs_App
- **Issue #234**: Eventos perdidos durante deploy de 2024-02-15
  - Período afectado: 2024-02-15 14:00 - 16:30 UTC
  - Datos recuperables: No
  - Acción: Excluir ese período de análisis

### Encuestas_NPS
- **Issue #156**: Formato inconsistente entre Q1 y Q2 2024
  - Cambio: Nuevas columnas agregadas en Q2
  - Acción: Usar script de normalización

## Dependencias entre Fuentes

```
CRM_Clientes (id_cliente)
    ↓
Logs_App (user_id)
    ↓
Encuestas_NPS (cliente_id)
```

**Join keys**:
- CRM ↔ Logs: `id_cliente` = `user_id`
- CRM ↔ NPS: `id_cliente` = `cliente_id`

## Proceso de Actualización

### Datos de Entrenamiento
1. Extraer CRM_Clientes (último mes)
2. Agregar Logs_App (últimos 90 días)
3. Join con Encuestas_NPS (último trimestre)
4. Aplicar validaciones de calidad
5. Guardar en `data/processed/`

**Frecuencia**: Mensual
**Responsable**: ML team
**Automatización**: Airflow DAG `update_training_data`

## SLAs y Monitoreo

| Fuente | Disponibilidad | Latencia Max | Monitoreo |
|--------|----------------|--------------|-----------|
| CRM_Clientes | 99.5% | 24h | Datadog |
| Logs_App | 99.9% | 1h | GCP Monitoring |
| Encuestas_NPS | 95% | 7d | Manual |

**Alertas configuradas**:
- CRM down > 1h → Critical
- Logs latency > 3h → Warning
- NPS no actualizado en 100 días → Warning

## Auditoría y Compliance

**GDPR Compliance**:
- ✅ Datos anonimizables: Sí
- ✅ Derecho al olvido: Implementado
- ✅ Consentimiento: Verificado en CRM

**Retención de datos**:
- CRM: 7 años (regulatorio)
- Logs: 2 años (técnico)
- NPS: 5 años (negocio)

## Referencias

- [Data Dictionary](data_dictionary.md)
- [Data Quality Guide](data_quality.md)
- [Data Schema YAML](config/data_schema.yaml)

## Changelog

| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2024-03-15 | Documento inicial | @ml-team |
| 2024-03-20 | Agregado Logs_App | @analytics |
