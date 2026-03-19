"""
Funciones para evaluación de modelos.

Este módulo proporciona funciones para evaluar modelos y calcular métricas.
Importa y usa estas funciones en tus notebooks o scripts.
"""
from typing import Dict, Any, Optional

import pandas as pd
import numpy as np

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    mean_squared_error, mean_absolute_error, r2_score
)

from src.logger import get_logger
from src.notifications import send_message
from src.config.settings import SLACK_CONFIG

logger = get_logger(__name__)


def evaluate_classification_model(
    y_true: pd.Series,
    y_pred: pd.Series,
    y_pred_proba: Optional[np.ndarray] = None,
    average: str = 'binary'
) -> Dict[str, Any]:
    """
    Evalúa un modelo de clasificación y retorna métricas.

    Args:
        y_true: Valores reales del target
        y_pred: Predicciones del modelo
        y_pred_proba: Probabilidades predichas (opcional, para ROC-AUC)
        average: Tipo de promedio para métricas ('binary', 'macro', 'weighted')

    Returns:
        Diccionario con métricas de evaluación
    """
    logger.info("Calculando métricas de evaluación")

    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)

    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average=average, zero_division=0),
        'recall': recall_score(y_true, y_pred, average=average, zero_division=0),
        'f1': f1_score(y_true, y_pred, average=average, zero_division=0)
    }

    if y_pred_proba is not None:
        try:
            metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba)
        except ValueError as e:
            logger.warning(f"No se pudo calcular ROC-AUC: {e}")

    conf_matrix = confusion_matrix(y_true, y_pred)
    metrics['confusion_matrix'] = conf_matrix.tolist()
    metrics['classification_report'] = report

    logger.info(
        "Métricas calculadas: Accuracy=%.3f, F1=%.3f",
        metrics['accuracy'],
        metrics['f1']
    )

    return metrics


def evaluate_regression_model(
    y_true: pd.Series,
    y_pred: pd.Series
) -> Dict[str, float]:
    """
    Evalúa un modelo de regresión y retorna métricas.

    Args:
        y_true: Valores reales del target
        y_pred: Predicciones del modelo

    Returns:
        Diccionario con métricas de evaluación
    """

    logger.info("Calculando métricas de regresión")

    metrics = {
        'mse': mean_squared_error(y_true, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
        'mae': mean_absolute_error(y_true, y_pred),
        'r2': r2_score(y_true, y_pred)
    }

    logger.info(
        "Métricas calculadas: RMSE=%.3f, R2=%.3f",
        metrics['rmse'],
        metrics['r2']
    )

    return metrics


def notify_evaluation_results(
    metrics: Dict[str, Any],
    model_name: str = "Modelo",
    webhook_url: Optional[str] = None
) -> bool:
    """
    Envía notificación con resultados de evaluación a Slack.

    Args:
        metrics: Diccionario con métricas de evaluación
        model_name: Nombre del modelo evaluado
        webhook_url: URL del webhook de Slack (si None, usa SLACK_CONFIG)

    Returns:
        True si la notificación fue exitosa, False en caso contrario
    """
    if webhook_url is None:
        webhook_url = SLACK_CONFIG.get('webhook')

    if not webhook_url:
        logger.warning('SLACK_WEBHOOK no configurado, omitiendo notificación')
        return False

    mensaje = f"✅ {model_name} evaluado\n"
    for metric, value in metrics.items():
        if metric != 'confusion_matrix':
            if isinstance(value, float):
                mensaje += f"• {metric}: {value:.3f}\n"
            else:
                mensaje += f"• {metric}: {value}\n"

    success = send_message(webhook_url=webhook_url, mensaje=mensaje)

    if success:
        logger.info("Notificación enviada exitosamente")
    else:
        logger.warning("No se pudo enviar notificación a Slack")

    return success
