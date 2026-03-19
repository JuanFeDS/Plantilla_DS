# 🏗️ Estructura del Proyecto

Documentación de la organización de carpetas y módulos del proyecto.

## 📁 Estructura General

```
{{ cookiecutter.project_slug }}/
│
├── data/                          # Datos (no versionados en git)
│   ├── raw/                       # Datos crudos sin procesar
│   ├── processed/                 # Datos procesados listos para modelado
│   ├── final/                     # Datos finales
│   └── reference/                 # Datos de referencia para validación
│
├── models/                        # Modelos entrenados (versionados)
│   ├── experiments/               # Modelos de experimentación
│   └── production/                # Modelos en producción
│
├── notebooks/                     # Jupyter notebooks
│   ├── exploratory/               # Análisis exploratorios (EDA)
│   ├── experiments/               # Notebooks de experimentación
│   └── reports/                   # Notebooks para reportes
│
├── src/                          # Código fuente del proyecto
│   ├── api/                      # API para servir el modelo
│   │   ├── __init__.py
│   │   └── main.py               # FastAPI application
│   │
│   ├── bd/                       # Conectores de base de datos
│   │   ├── __init__.py
│   │   ├── base.py               # Clase abstracta DatabaseConnector
│   │   └── oracle_connector.py   # Implementación para Oracle
│   │
│   ├── config/                   # Configuración del proyecto
│   │   ├── __init__.py
│   │   └── settings.py           # Variables de entorno y configuración
│   │
│   ├── data/                     # Módulos de manejo de datos
│   │   ├── __init__.py
│   │   ├── eda.py                # Utilidades para análisis exploratorio
│   │   ├── preprocessing.py      # Limpieza y transformación de datos
│   │   └── quality_checks.py     # Validaciones de calidad de datos
│   │
│   ├── features/                 # Ingeniería de features
│   │   ├── __init__.py
│   │   └── engineering.py        # Creación y transformación de features
│   │
│   ├── models/                   # Modelos de ML
│   │   ├── __init__.py
│   │   └── dummie_model.py       # Modelo de ejemplo
│   │
│   ├── pipelines/                # Pipelines de procesamiento
│   │   ├── __init__.py
│   │   └── data_pipeline.py      # Pipeline completo de datos
│   │
│   ├── logger/                   # Sistema de logging
│   │   ├── __init__.py
│   │   └── logger.py             # Configuración de logging
│   │
│   ├── notifications/            # Sistema de notificaciones
│   │   ├── __init__.py
│   │   └── slack.py              # Notificaciones a Slack
│   │
│   └── visualization/            # Visualizaciones
│       └── __init__.py
│
├── scripts/                      # Scripts ejecutables
│   ├── data_processing.py        # Procesamiento de datos
│   ├── download_model.py         # Descarga de modelos
│   ├── model_evaluation.py       # Evaluación de modelos
│   └── model_training.py         # Entrenamiento de modelos
│
├── tests/                        # Tests unitarios
│   ├── __init__.py
│   └── test_bd/
│       └── test_database.py
│
├── docs/                         # Documentación
│   ├── README.md                 # Índice de documentación
│   ├── STRUCTURE.md              # Este archivo
│   │
│   ├── model/                    # Documentación del modelo
│   │   ├── model_card.md
│   │   └── experimentation_log.md
│   │
│   ├── data/                     # Documentación de datos
│   │   ├── data_dictionary.md
│   │   ├── data_sources.md
│   │   └── data_quality.md
│   │
│   ├── ops/                      # Documentación operativa
│   │   ├── deployment.md
│   │   └── monitoring.md
│   │
│   ├── config/                   # Configuraciones YAML
│   │   ├── model_metadata.yaml
│   │   ├── data_schema.yaml
│   │   ├── deployment_config.yaml
│   │   └── monitoring_config.yaml
│   │
│   └── templates/                # Plantillas reutilizables
│       ├── eda_template.md
│       └── rfc_template.md
│
├── logs/                         # Logs de aplicación
├── .env.example                  # Ejemplo de variables de entorno
├── .gitignore                    # Archivos ignorados por git
├── pyproject.toml                # Configuración del proyecto y herramientas
├── README.md                     # README principal del proyecto
├── requirements.txt              # Dependencias de Python
└── run.py                        # Punto de entrada principal
```

---

## 🎯 Capas de la Arquitectura

### 1. **Capa de Datos (`src/data/`)**

Responsable de la limpieza y validación de datos.

**Módulos**:
- `preprocessing.py`: Limpieza de missing values, duplicados, normalización
- `quality_checks.py`: Validaciones de calidad (schema, completitud, rangos)
- `eda.py`: Utilidades para análisis exploratorio

**Flujo típico**:
```python
import pandas as pd
from src.data.preprocessing import clean_missing_values, remove_duplicates
from src.data.quality_checks import run_quality_pipeline

# Cargar (usa pandas directamente)
df = pd.read_csv('data/raw/clientes.csv')

# Validar
quality_report = run_quality_pipeline(df)

# Limpiar
df = remove_duplicates(df)
df = clean_missing_values(df, strategy='median')
```

---

### 2. **Capa de Features (`src/features/`)**

Responsable de la ingeniería de features.

**Módulos**:
- `engineering.py`: Creación de features derivadas, encoding, scaling

**Flujo típico**:
```python
from src.features.engineering import (
    create_date_features,
    encode_categorical,
    scale_features
)

# Features temporales
df = create_date_features(df, 'fecha_registro', ['year', 'month'])

# Encoding
df = encode_categorical(df, ['genero', 'ciudad'], method='onehot')

# Scaling
df = scale_features(df, ['edad', 'ingreso'], method='standard')
```

---

### 3. **Capa de Pipelines (`src/pipelines/`)**

Orquesta el flujo completo de procesamiento.

**Módulos**:
- `data_pipeline.py`: Pipeline completo desde datos crudos hasta features

**Flujo típico**:
```python
from src.pipelines.data_pipeline import DataPipeline

config = {
    'date_columns': ['fecha_registro'],
    'categorical_columns': ['genero', 'ciudad'],
    'numerical_columns': ['edad', 'ingreso']
}

pipeline = DataPipeline(config)
df = pipeline.run(
    source='data/raw/clientes.csv',
    output_path='data/processed/features.parquet'
)
```

---

### 4. **Capa de Modelos (`src/models/`)**

Contiene la lógica de los modelos de ML.

**Módulos**:
- `dummie_model.py`: Modelo de ejemplo (reemplazar con tu modelo)

**Flujo típico**:
```python
# Entrenar
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
model.fit(X_train, y_train)

# Guardar
import joblib
joblib.dump(model, 'models/production/model_v1.0.0.pkl')
```

---

### 5. **Capa de API (`src/api/`)**

Expone el modelo como servicio REST.

**Módulos**:
- `main.py`: Aplicación FastAPI con endpoints

**Flujo típico**:
```bash
# Iniciar servidor
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Hacer predicción
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"edad": 35, "ingreso_mensual": 50000, ...}'
```

---

### 6. **Capa de Base de Datos (`src/bd/`)**

Conectores para diferentes bases de datos.

**Módulos**:
- `base.py`: Clase abstracta `DatabaseConnector`
- `oracle_connector.py`: Implementación para Oracle

**Flujo típico**:
```python
from src.bd.oracle_connector import OracleConnector

with OracleConnector() as db:
    df = db.execute_get_query("SELECT * FROM clientes WHERE id = :id", params={'id': 123})
```

---

### 7. **Logger y Notificaciones**

Sistemas de logging y notificaciones.

**Módulos**:
- `src.logger`: Sistema de logging centralizado
- `src.notifications`: Notificaciones a Slack

**Flujo típico**:
```python
from src.logger import get_logger
from src.notifications import send_message

logger = get_logger(__name__)
logger.info("Proceso iniciado")

send_message(webhook_url, "Modelo entrenado exitosamente")
```

---

## 🔄 Flujo de Trabajo Completo

### 1. Desarrollo Local

```bash
# 1. Procesar datos
python scripts/data_processing.py \
  --input data/raw/clientes.csv \
  --output data/processed/features.parquet \
  --config config/pipeline_config.yaml

# 2. Entrenar modelo
python scripts/model_training.py

# 3. Evaluar modelo
python scripts/model_evaluation.py

# 4. Servir modelo localmente
uvicorn src.api.main:app --reload
```

### 2. Experimentación

```bash
# Usar notebooks en notebooks/experiments/
jupyter notebook notebooks/experiments/exp_001_baseline.ipynb

# Documentar en docs/model/experimentation_log.md
```

### 3. Deployment

```bash
# 1. Descargar modelo
python scripts/download_model.py --version 1.0.0

# 2. Construir imagen Docker
docker build -t ml-model:1.0.0 .

# 3. Desplegar (ver docs/ops/deployment.md)
kubectl apply -f k8s/production/
```

---

## 📦 Dependencias entre Módulos

```
scripts/
  └─> src.pipelines.data_pipeline
        └─> pandas (carga directa)
        └─> src.data.preprocessing
        └─> src.data.quality_checks
        └─> src.features.engineering

src.api.main
  └─> src.api.models (esquemas Pydantic)
  └─> src.logger

src.bd.oracle_connector
  └─> src.bd.base
  └─> src.config.settings
```

---

## 🎨 Convenciones de Código

### Nombres de Archivos
- Módulos: `snake_case.py`
- Clases: `PascalCase`
- Funciones: `snake_case()`
- Constantes: `UPPER_SNAKE_CASE`

### Estructura de Módulos
```python
"""
Docstring del módulo.

Descripción de qué hace el módulo y cuándo usarlo.
"""
from typing import Optional
import pandas as pd

# Imports de terceros

# Imports locales
from src.utils.logger.logger import get_logger

logger = get_logger(__name__)


def funcion_publica():
    """Docstring de la función."""
    pass


def _funcion_privada():
    """Funciones privadas con prefijo _."""
    pass
```

### Docstrings
```python
def funcion(arg1: str, arg2: int = 10) -> pd.DataFrame:
    """
    Descripción breve de la función.

    Args:
        arg1: Descripción del argumento 1
        arg2: Descripción del argumento 2 (opcional)

    Returns:
        Descripción del valor de retorno

    Raises:
        ValueError: Cuándo se lanza esta excepción

    Ejemplo:
        >>> df = funcion('datos.csv', arg2=20)
    """
    pass
```

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest tests/

# Con cobertura
pytest tests/ --cov=src --cov-report=html

# Test específico
pytest tests/test_bd/test_database.py
```

---

## 📊 Logging

Todos los módulos deben usar el logger centralizado con lazy formatting:

```python
from src.logger import get_logger

logger = get_logger(__name__)

# Usar lazy formatting (%) en lugar de f-strings
logger.debug("Mensaje de debug: %s", variable)
logger.info("Procesando %d registros", count)
logger.warning("Advertencia en %s", module_name)
logger.error("Error al procesar: %s", error_msg)
logger.critical("Error crítico en %s", component)
```

Logs se guardan en:
- `logs/app.log` (rotación diaria)
- Consola (nivel INFO)

---

## 🔐 Configuración

Variables de entorno en `.env`:

```bash
# Base de datos
DB_HOST=localhost
DB_PORT=1521
DB_NAME=ORCL
DB_USER=user
DB_PASSWORD=password

# API
API_KEY_SECRET=secret

# Slack
SLACK_WEBHOOK=https://hooks.slack.com/...
```

Cargar con:
```python
from src.config.settings import DB_CONFIG, SLACK_CONFIG
```

---

## 📚 Referencias

- [README Principal](../README.md)
- [Documentación Completa](docs/README.md)
- [Deployment Guide](docs/ops/deployment.md)
- [Data Quality Guide](docs/data/data_quality.md)
