"""
Funciones para entrenamiento de modelos.

Este módulo proporciona funciones para entrenar y guardar modelos.
Importa y usa estas funciones en tus notebooks o scripts.
"""
from typing import Optional, Dict, Any

import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import joblib

from src.logger import get_logger

logger = get_logger(__name__)


def train_model(
    x_train: pd.DataFrame,
    y_train: pd.Series,
    model,
    model_name: str = "model",
    output_dir: str = "models/experiments",
    save: bool = True
):
    """
    Entrena un modelo y opcionalmente lo guarda.

    Args:
        x_train: Features de entrenamiento
        y_train: Target de entrenamiento
        model: Instancia del modelo (sklearn, xgboost, etc.)
        model_name: Nombre del modelo para guardar
        output_dir: Directorio donde guardar el modelo
        save: Si True, guarda el modelo entrenado

    Returns:
        Modelo entrenado
    """
    logger.info("Iniciando entrenamiento del modelo: %s", model_name)
    logger.info("Samples de entrenamiento: %d", len(x_train))
    logger.info("Features: %d", len(x_train.columns))

    try:
        model.fit(x_train, y_train)
        logger.info("Entrenamiento completado exitosamente")

        if save:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"{output_dir}/{model_name}_{timestamp}.pkl"
            joblib.dump(model, filepath)
            logger.info("Modelo guardado en: %s", filepath)

        return model

    except Exception as e:
        logger.error("Error en entrenamiento: %s", str(e))
        raise


def load_model(model_path: str):
    """
    Carga un modelo guardado.

    Args:
        model_path: Ruta al archivo del modelo

    Returns:
        Modelo cargado
    """
    logger.info("Cargando modelo desde: %s", model_path)
    model = joblib.load(model_path)
    logger.info("Modelo cargado exitosamente")
    return model


def save_model_metadata(
    model_path: str,
    metadata: Dict[str, Any],
    output_path: Optional[str] = None
) -> None:
    """
    Guarda metadata del modelo en archivo JSON.

    Args:
        model_path: Ruta al modelo
        metadata: Diccionario con metadata (métricas, hiperparámetros, etc.)
        output_path: Ruta para guardar metadata (si None, usa misma ruta que modelo)
    """

    if output_path is None:
        output_path = str(Path(model_path).with_suffix('.json'))

    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(metadata, file, indent=2, ensure_ascii=False)

    logger.info("Metadata guardada en: %s", output_path)
