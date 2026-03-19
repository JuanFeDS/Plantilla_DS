# 🧪 Experimentation Log

Registro cronológico de los experimentos realizados durante el desarrollo del modelo.

## Experimentos

| ID | Fecha | Autor | Descripción | Cambios | Métricas | Tiempo | Notebook/Commit | Estado |
|----|-------|-------|-------------|---------|----------|--------|-----------------|--------|
| EXP-001 | 2025-05-15 | @data_scientist | Baseline RandomForest | Default hyperparams, sin balanceo | Acc: 0.82, Prec: 0.84, Rec: 0.70, F1: 0.75 | 15 min | [notebook](../notebooks/exp_001_baseline.ipynb) | ✅ Completado |
| EXP-002 | 2025-05-17 | @data_scientist | Balanceo con SMOTE | SMOTE sobre clase minoritaria | Acc: 0.80, Prec: 0.78, Rec: 0.82, F1: 0.80 | 20 min | [notebook](../notebooks/exp_002_smote.ipynb) | ✅ Completado |
| EXP-003 | 2025-05-20 | @ml_engineer | LightGBM + tuning | Grid search, early stopping | Acc: 0.87, Prec: 0.85, Rec: 0.82, F1: 0.81 | 2h 30min | [commit](https://github.com/repo/commit/abc123) | ✅ Seleccionado |

## Detalles de Experimentos

### EXP-001: Baseline RandomForest

**Objetivo**: Establecer baseline para comparación

**Configuración**:
```python
RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    random_state=42
)
```

**Dataset**:
- Train: 70,000 samples
- Validation: 15,000 samples
- Test: 15,000 samples

**Resultados**:
- Accuracy: 0.82
- Precision: 0.84
- Recall: 0.70 ⚠️ (bajo)
- F1 Score: 0.75
- AUC-ROC: 0.88

**Análisis**:
- ✅ Buen punto de partida
- ⚠️ Recall bajo indica que perdemos muchos casos positivos
- 💡 Considerar balanceo de clases

**Features más importantes**:
1. score_crediticio (0.25)
2. antiguedad_meses (0.18)
3. ingreso_mensual (0.15)

**Próximos pasos**:
- Probar balanceo de clases
- Explorar otros algoritmos

---

### EXP-002: Balanceo con SMOTE

**Objetivo**: Mejorar recall mediante balanceo de clases

**Configuración**:
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    random_state=42
)
```

**Dataset**:
- Train original: 70,000 (60% clase 0, 40% clase 1)
- Train balanceado: 84,000 (50% clase 0, 50% clase 1)
- Validation: 15,000 samples
- Test: 15,000 samples

**Resultados**:
- Accuracy: 0.80 (↓ -2%)
- Precision: 0.78 (↓ -6%)
- Recall: 0.82 (↑ +12%) ✅
- F1 Score: 0.80 (↑ +5%)
- AUC-ROC: 0.89 (↑ +1%)

**Análisis**:
- ✅ Recall mejorado significativamente
- ⚠️ Ligera pérdida en precision
- ✅ F1 score mejorado (mejor balance)
- 💡 Trade-off aceptable para el caso de uso

**Comparación con baseline**:
- Menos falsos negativos (-30%)
- Más falsos positivos (+15%)
- Para churn, preferimos detectar más casos (recall)

**Próximos pasos**:
- Probar algoritmos más sofisticados (Gradient Boosting)
- Tuning de hiperparámetros

---

### EXP-003: LightGBM + Tuning

**Objetivo**: Mejorar performance con algoritmo más sofisticado

**Configuración**:
```python
from lightgbm import LGBMClassifier

# Grid search
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15],
    'learning_rate': [0.01, 0.05, 0.1],
    'num_leaves': [31, 50, 100]
}

best_params = {
    'n_estimators': 200,
    'max_depth': 10,
    'learning_rate': 0.05,
    'num_leaves': 50,
    'random_state': 42
}

LGBMClassifier(**best_params)
```

**Dataset**:
- Train: 70,000 (con SMOTE → 84,000)
- Validation: 15,000 samples
- Test: 15,000 samples

**Resultados**:
- Accuracy: 0.87 (↑ +7% vs baseline)
- Precision: 0.85 (↑ +1% vs baseline)
- Recall: 0.82 (↑ +12% vs baseline)
- F1 Score: 0.81 (↑ +6% vs baseline)
- AUC-ROC: 0.91 (↑ +3% vs baseline)

**Análisis**:
- ✅ Mejor modelo hasta ahora en todas las métricas
- ✅ Buen balance precision/recall
- ✅ Tiempo de entrenamiento razonable (2.5h)
- ✅ Permite interpretabilidad con SHAP

**Feature Importance (SHAP)**:
1. score_crediticio (0.28)
2. antiguedad_meses (0.22)
3. ingreso_mensual (0.18)
4. num_productos (0.12)
5. edad (0.10)

**Validación cruzada**:
- 5-fold CV mean: 0.86 (±0.02)
- Modelo estable

**Decisión**: ✅ **Seleccionado para producción**

**Próximos pasos**:
- Documentar en model_card.md
- Preparar deployment
- Configurar monitoreo

---

## Resumen de Experimentos

### Comparación de Métricas

| Experimento | Accuracy | Precision | Recall | F1 Score | AUC-ROC | Tiempo |
|-------------|----------|-----------|--------|----------|---------|--------|
| EXP-001 (Baseline) | 0.82 | 0.84 | 0.70 | 0.75 | 0.88 | 15 min |
| EXP-002 (SMOTE) | 0.80 | 0.78 | 0.82 | 0.80 | 0.89 | 20 min |
| EXP-003 (LightGBM) | **0.87** | **0.85** | **0.82** | **0.81** | **0.91** | 2h 30min |

### Lecciones Aprendidas

1. **Balanceo de clases es crucial**: SMOTE mejoró recall significativamente
2. **LightGBM > RandomForest**: Para este dataset, gradient boosting supera a RF
3. **Tuning vale la pena**: Grid search agregó +5% accuracy vs. default params
4. **Trade-offs**: Pequeña pérdida en precision es aceptable para ganar recall

### Experimentos Descartados

| ID | Fecha | Descripción | Razón de descarte |
|----|-------|-------------|-------------------|
| EXP-004 | 2025-05-22 | XGBoost | Similar a LightGBM pero más lento |
| EXP-005 | 2025-05-23 | Neural Network | Overfitting, no mejora métricas |
| EXP-006 | 2025-05-24 | Logistic Regression | Underperforming vs. baseline |

## Próximos Experimentos Planificados

- [ ] **EXP-007**: Feature engineering avanzado (interacciones, polinomiales)
- [ ] **EXP-008**: Ensemble de LightGBM + RandomForest
- [ ] **EXP-009**: Calibración de probabilidades
- [ ] **EXP-010**: Análisis de fairness por género/edad

## Configuración de Experimentos

### Ambiente
- Python: 3.11
- Librerías principales: scikit-learn 1.3.0, lightgbm 4.0.0, imbalanced-learn 0.11.0
- Hardware: 8 CPU cores, 32GB RAM
- Seed: 42 (reproducibilidad)

### Métricas de Evaluación
- **Primaria**: F1 Score (balance precision/recall)
- **Secundarias**: Accuracy, Precision, Recall, AUC-ROC
- **Negocio**: Costo de FP vs. FN

### Proceso de Validación
1. Train/Validation/Test split: 70/15/15
2. Stratified split (mantener distribución de clases)
3. 5-fold cross-validation en train set
4. Evaluación final en test set (nunca visto)

## Referencias

- Notebooks: `notebooks/experiments/`
- Modelos guardados: `models/experiments/`
- Logs de entrenamiento: `logs/experiments/`
- Configuraciones: `config/experiments/`

## Changelog

| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2025-05-15 | Experimento baseline | @data_scientist |
| 2025-05-17 | Experimento SMOTE | @data_scientist |
| 2025-05-20 | Experimento LightGBM seleccionado | @ml_engineer |
