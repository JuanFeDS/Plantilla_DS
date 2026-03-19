"""
Funciones para descargar modelos desde el registro de modelos.

Este módulo proporciona funciones para descargar modelos desde diferentes
registros (S3, GCS, Azure, local). Importa y usa estas funciones en tus scripts.
"""
from pathlib import Path
from typing import List

from src.logger import get_logger

logger = get_logger(__name__)


def download_model(
    version: str,
    model_name: str = "model",
    registry_type: str = "s3"
) -> Path:
    """
    Descarga un modelo específico desde el registro de modelos.

    Args:
        version: Versión del modelo a descargar (ej: '1.0.0', 'latest')
        model_name: Nombre del modelo
        registry_type: Tipo de registro ('s3', 'gcs', 'azure', 'local')

    Returns:
        Path al archivo del modelo descargado

    """
    logger.info("Descargando modelo %s v%s desde %s", model_name, version, registry_type)

    raise NotImplementedError(
        "Implementa la descarga desde el registro de modelos. "
    )


def list_available_versions(
    registry_type: str,
    model_name: str = "model"
) -> List[str]:
    """
    Lista todas las versiones disponibles de un modelo.

    Args:
        model_name: Nombre del modelo
        registry_type: Tipo de registro

    Returns:
        Lista de versiones disponibles ordenadas de más reciente a más antigua
    """
    logger.info("Listando versiones de %s en %s", model_name, registry_type)

    raise NotImplementedError(
        "Implementa el listado de versiones desde el registro de modelos."
    )
