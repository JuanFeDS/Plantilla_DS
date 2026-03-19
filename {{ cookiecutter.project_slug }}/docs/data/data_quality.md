# 🔍 Data Quality Guide

Guía de validaciones y controles de calidad de datos para el proyecto.

## 📋 Tabla de Contenidos

- [Resumen](#resumen)
- [Schema de Datos](#schema-de-datos)
- [Validaciones Automáticas](#validaciones-automáticas)
- [Pipeline de Calidad](#pipeline-de-calidad)
- [Manejo de Datos Faltantes](#manejo-de-datos-faltantes)
- [Detección de Outliers](#detección-de-outliers)
- [Monitoreo Continuo](#monitoreo-continuo)
- [Troubleshooting](#troubleshooting)

---

## Resumen

Este documento describe las validaciones de calidad de datos implementadas en el proyecto. Todas las configuraciones técnicas están en [`config/data_schema.yaml`](config/data_schema.yaml).

### Objetivos de Calidad

- **Completitud**: < 15% valores faltantes en features críticos
- **Validez**: 100% de valores dentro de rangos esperados
- **Consistencia**: 0 duplicados en IDs
- **Actualidad**: Datos no más antiguos de 7 días

---

## Schema de Datos

### Estructura Esperada

El dataset debe cumplir con el schema definido en `config/data_schema.yaml`:

| Campo              | Tipo    | Nullable | Rango/Valores            | Descripción                    |
|--------------------|---------|----------|--------------------------|--------------------------------|
| id_cliente         | int     | No       | Único                    | Identificador del cliente      |
| edad               | int     | No       | 18-99                    | Edad en años                   |
| genero             | str     | Sí       | M, F, Otro, No especif.  | Género del cliente             |
| ingreso_mensual    | float   | Sí       | 0-1,000,000              | Ingreso mensual estimado       |
| fecha_registro     | date    | No       | >= 2020-01-01            | Fecha de registro              |
| score_crediticio   | int     | Sí       | 300-850                  | Score crediticio               |
| num_productos      | int     | No       | 0-10                     | Número de productos            |
| antiguedad_meses   | int     | No       | >= 0                     | Antigüedad en meses            |
| target             | int     | No       | 0, 1                     | Variable objetivo (churn)      |

### Ejemplo de Validación Programática

```python
import pandas as pd
import yaml

# Cargar schema
with open('docs/config/data_schema.yaml', 'r') as f:
    schema = yaml.safe_load(f)

# Validar tipos de datos
def validate_schema(df, schema):
    errors = []
    
    for col_name, col_spec in schema['columns'].items():
        if col_name not in df.columns:
            errors.append(f"Columna faltante: {col_name}")
            continue
            
        # Validar tipo
        expected_type = col_spec['type']
        if expected_type == 'integer' and not pd.api.types.is_integer_dtype(df[col_name]):
            errors.append(f"{col_name}: tipo esperado integer, encontrado {df[col_name].dtype}")
        
        # Validar nulls
        if not col_spec.get('nullable', True):
            null_count = df[col_name].isnull().sum()
            if null_count > 0:
                errors.append(f"{col_name}: {null_count} valores nulos (no permitidos)")
    
    return errors
```

---

## Validaciones Automáticas

### 1. Validaciones de Completitud

**Objetivo**: Asegurar que los datos tienen suficiente información.

```python
def check_completeness(df):
    """Valida porcentaje de valores faltantes."""
    missing_thresholds = {
        'id_cliente': 0.0,
        'edad': 0.0,
        'ingreso_mensual': 15.0,
        'score_crediticio': 20.0,
        'target': 0.0
    }
    
    results = {}
    for col, threshold in missing_thresholds.items():
        missing_pct = (df[col].isnull().sum() / len(df)) * 100
        results[col] = {
            'missing_pct': missing_pct,
            'threshold': threshold,
            'passed': missing_pct <= threshold
        }
    
    return results
```

**Acción si falla:**
- Missing < 20%: Log warning, continuar
- Missing 20-50%: Alertar a equipo, evaluar imputación
- Missing > 50%: Bloquear pipeline, investigar fuente

### 2. Validaciones de Rango

**Objetivo**: Detectar valores fuera de rangos esperados.

```python
def check_ranges(df):
    """Valida que valores estén en rangos esperados."""
    range_checks = {
        'edad': (18, 99),
        'ingreso_mensual': (0, 1_000_000),
        'score_crediticio': (300, 850),
        'num_productos': (0, 10)
    }
    
    results = {}
    for col, (min_val, max_val) in range_checks.items():
        out_of_range = df[
            (df[col] < min_val) | (df[col] > max_val)
        ][col].count()
        
        results[col] = {
            'out_of_range_count': out_of_range,
            'out_of_range_pct': (out_of_range / len(df)) * 100,
            'passed': out_of_range == 0
        }
    
    return results
```

### 3. Validaciones de Unicidad

**Objetivo**: Detectar duplicados en identificadores únicos.

```python
def check_uniqueness(df):
    """Valida unicidad de IDs."""
    duplicates = df['id_cliente'].duplicated().sum()
    
    return {
        'duplicate_count': duplicates,
        'duplicate_pct': (duplicates / len(df)) * 100,
        'passed': duplicates == 0
    }
```

**Acción si falla:**
- Duplicados detectados → Bloquear pipeline
- Investigar causa raíz
- Eliminar duplicados o corregir en fuente

### 4. Validaciones de Distribución

**Objetivo**: Detectar cambios significativos en distribuciones.

```python
from scipy import stats

def check_distribution(df, reference_df):
    """Compara distribuciones con datos de referencia."""
    numerical_cols = ['edad', 'ingreso_mensual', 'score_crediticio']
    
    results = {}
    for col in numerical_cols:
        # Kolmogorov-Smirnov test
        ks_stat, p_value = stats.ks_2samp(
            df[col].dropna(),
            reference_df[col].dropna()
        )
        
        results[col] = {
            'ks_statistic': ks_stat,
            'p_value': p_value,
            'passed': p_value > 0.05  # No hay diferencia significativa
        }
    
    return results
```

### 5. Validaciones de Consistencia

**Objetivo**: Verificar relaciones lógicas entre variables.

```python
def check_consistency(df):
    """Valida consistencia lógica entre variables."""
    checks = []
    
    # Antigüedad no puede ser negativa
    checks.append({
        'rule': 'antiguedad_meses >= 0',
        'violations': (df['antiguedad_meses'] < 0).sum()
    })
    
    # Fecha de registro debe ser pasada
    checks.append({
        'rule': 'fecha_registro <= today',
        'violations': (df['fecha_registro'] > pd.Timestamp.now()).sum()
    })
    
    # Num productos debe ser >= 0
    checks.append({
        'rule': 'num_productos >= 0',
        'violations': (df['num_productos'] < 0).sum()
    })
    
    return checks
```

---

## Pipeline de Calidad

### Flujo de Validación

```
┌─────────────────┐
│  Raw Data       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Schema Check    │ ◄── Valida estructura y tipos
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Completeness    │ ◄── Verifica missing values
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Range Check     │ ◄── Valida rangos de valores
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Uniqueness      │ ◄── Detecta duplicados
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Distribution    │ ◄── Compara con baseline
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Consistency     │ ◄── Valida reglas de negocio
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Quality Report  │ ◄── Genera reporte
└────────┬────────┘
         │
         ▼
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌───────┐
│ Pass  │ │ Fail  │
└───────┘ └───┬───┘
              │
              ▼
        ┌──────────┐
        │  Alert   │
        └──────────┘
```

### Implementación

```python
from src.data.quality_checks import (
    validate_schema,
    check_completeness,
    check_ranges,
    check_uniqueness,
    check_distribution,
    check_consistency
)

def run_quality_pipeline(df, reference_df=None):
    """Ejecuta pipeline completo de validación."""
    
    report = {
        'timestamp': pd.Timestamp.now(),
        'total_rows': len(df),
        'checks': {}
    }
    
    # 1. Schema
    report['checks']['schema'] = validate_schema(df, schema)
    
    # 2. Completeness
    report['checks']['completeness'] = check_completeness(df)
    
    # 3. Ranges
    report['checks']['ranges'] = check_ranges(df)
    
    # 4. Uniqueness
    report['checks']['uniqueness'] = check_uniqueness(df)
    
    # 5. Distribution (si hay referencia)
    if reference_df is not None:
        report['checks']['distribution'] = check_distribution(df, reference_df)
    
    # 6. Consistency
    report['checks']['consistency'] = check_consistency(df)
    
    # Determinar si pasa o falla
    report['passed'] = all(
        check.get('passed', True)
        for check in report['checks'].values()
    )
    
    return report
```

### Uso en Scripts

```python
# En script de procesamiento
import pandas as pd

# Cargar datos
df = pd.read_csv('data/raw/clientes.csv')

# Cargar datos de referencia
reference_df = pd.read_parquet('data/reference/train_data.parquet')

# Ejecutar validaciones
quality_report = run_quality_pipeline(df, reference_df)

# Guardar reporte
with open('reports/quality_report.json', 'w') as f:
    json.dump(quality_report, f, indent=2, default=str)

# Decidir acción
if not quality_report['passed']:
    logger.error("Quality checks failed!")
    send_alert_to_slack(quality_report)
    raise ValueError("Data quality checks failed")
else:
    logger.info("Quality checks passed ✓")
    # Continuar con procesamiento
```

---

## Manejo de Datos Faltantes

### Estrategias por Columna

| Columna            | Estrategia                        | Justificación                           |
|--------------------|-----------------------------------|-----------------------------------------|
| edad               | No permitir nulls                 | Feature crítico, siempre disponible     |
| ingreso_mensual    | Imputar con mediana por edad_bin  | Correlación con edad                    |
| score_crediticio   | Imputar con modelo predictivo     | Puede predecirse de otras features      |
| genero             | Categoría "No especificado"       | Información sensible, puede faltar      |

### Implementación

```python
def impute_missing_values(df):
    """Imputa valores faltantes según estrategia definida."""
    
    # Ingreso mensual: mediana por grupo de edad
    df['edad_bin'] = pd.cut(df['edad'], bins=[18, 25, 35, 45, 55, 65, 100])
    df['ingreso_mensual'] = df.groupby('edad_bin')['ingreso_mensual'].transform(
        lambda x: x.fillna(x.median())
    )
    
    # Género: categoría especial
    df['genero'] = df['genero'].fillna('No especificado')
    
    # Score crediticio: modelo simple
    # (en producción, usar modelo más sofisticado)
    df['score_crediticio'] = df['score_crediticio'].fillna(
        df['score_crediticio'].median()
    )
    
    return df
```

---

## Detección de Outliers

### Métodos Implementados

#### 1. IQR (Interquartile Range)

```python
def detect_outliers_iqr(df, column, threshold=1.5):
    """Detecta outliers usando método IQR."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    
    outliers = df[
        (df[column] < lower_bound) | (df[column] > upper_bound)
    ]
    
    return outliers, lower_bound, upper_bound
```

#### 2. Z-Score

```python
def detect_outliers_zscore(df, column, threshold=3):
    """Detecta outliers usando Z-score."""
    z_scores = np.abs(stats.zscore(df[column].dropna()))
    outliers = df[z_scores > threshold]
    
    return outliers
```

### Manejo de Outliers

**Estrategia**: No eliminar automáticamente, sino:

1. **Flaggear**: Agregar columna `is_outlier_{feature}`
2. **Investigar**: Revisar si son errores o valores legítimos
3. **Decidir**: 
   - Errores → Corregir o eliminar
   - Legítimos → Mantener pero monitorear

```python
# Flaggear outliers
outliers, lower, upper = detect_outliers_iqr(df, 'ingreso_mensual')
df['is_outlier_ingreso'] = df['ingreso_mensual'].isin(outliers['ingreso_mensual'])

# Log para revisión
logger.info(f"Outliers detectados en ingreso_mensual: {len(outliers)}")
logger.info(f"Rango esperado: [{lower:.2f}, {upper:.2f}]")
```

---

## Monitoreo Continuo

### Métricas Trackeadas

Se monitorean continuamente en producción (ver `config/monitoring_config.yaml`):

- **Missing values %** por columna
- **Distribución de features** (drift detection)
- **Valores fuera de rango**
- **Duplicados detectados**

### Dashboard de Calidad

Acceder a: https://grafana.empresa.com/d/data-quality

Paneles incluidos:
- Missing values trend
- Feature distributions
- Data drift scores
- Quality check failures

### Alertas Configuradas

| Condición                        | Severidad | Acción                    |
|----------------------------------|-----------|---------------------------|
| Missing > 50%                    | Critical  | Bloquear pipeline + PagerDuty |
| Missing > 20%                    | Warning   | Slack notification        |
| Duplicados detectados            | Critical  | Bloquear pipeline         |
| Data drift KS test p < 0.05      | Warning   | Email a equipo            |
| Outliers > 10%                   | Info      | Log en dashboard          |

---

## Troubleshooting

### Problema: High Missing Values

**Síntomas:**
- Alerta de missing > 20%
- Features con muchos nulls

**Diagnóstico:**
```python
# Analizar patrón de missing
import missingno as msno

msno.matrix(df)
msno.heatmap(df)

# Verificar si es aleatorio o sistemático
missing_by_date = df.groupby('fecha_registro').apply(
    lambda x: x.isnull().sum() / len(x)
)
```

**Soluciones:**
1. Verificar fuente de datos
2. Contactar a data engineer
3. Evaluar imputación o exclusión de feature

### Problema: Data Drift Detectado

**Síntomas:**
- Alerta de KS test p < 0.05
- Distribuciones diferentes

**Diagnóstico:**
```python
# Comparar distribuciones
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Distribución actual
df['edad'].hist(ax=axes[0], bins=30, alpha=0.7, label='Actual')
reference_df['edad'].hist(ax=axes[0], bins=30, alpha=0.7, label='Reference')
axes[0].legend()

# Q-Q plot
stats.probplot(df['edad'], dist="norm", plot=axes[1])
```

**Acciones:**
1. Documentar drift en `experimentation_log.md`
2. Evaluar impacto en modelo
3. Considerar reentrenamiento

### Problema: Duplicados en IDs

**Síntomas:**
- Alerta de duplicados
- Pipeline bloqueado

**Diagnóstico:**
```python
# Identificar duplicados
duplicates = df[df.duplicated(subset=['id_cliente'], keep=False)]

# Analizar patrón
print(duplicates.sort_values('id_cliente'))
```

**Soluciones:**
1. Verificar ETL upstream
2. Eliminar duplicados (keep='first' o 'last')
3. Corregir en fuente de datos

---

## Referencias

- [Data Schema YAML](config/data_schema.yaml)
- [Monitoring Config](config/monitoring_config.yaml)
- [Great Expectations Docs](https://docs.greatexpectations.io/)
- [Data Dictionary](data_dictionary.md)

## Contacto

- **Data Engineering**: data-eng@empresa.com
- **ML Team**: ml-team@empresa.com
- **Slack**: #data-quality
