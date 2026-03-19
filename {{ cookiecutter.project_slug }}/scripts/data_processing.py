"""
Funciones para procesamiento de datos.

Este módulo proporciona funciones para ejecutar el pipeline de procesamiento
de datos. Importa y usa estas funciones en tus notebooks o scripts.
"""
from typing import Optional, Dict, Any

import pandas as pd

from src.pipelines.data_pipeline import DataPipeline
from src.logger import get_logger

logger = get_logger(__name__)


def process_data(
    input_path: str,
    output_path: str,
    config: Optional[Dict[str, Any]] = None,
    validate: bool = True,
    reference_df: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Procesa datos usando el pipeline completo.

    Args:
        input_path: Ruta a datos crudos (CSV, Excel, Parquet)
        output_path: Ruta para guardar datos procesados
        config: Configuración del pipeline (columnas, estrategias, etc.)
        validate: Si True, ejecuta validaciones de calidad
        reference_df: DataFrame de referencia para validación (opcional)
    Returns:
        DataFrame con datos procesados
    """
    logger.info("Iniciando procesamiento de datos: %s", input_path)

    pipeline = DataPipeline(config or {})

    try:
        df = pipeline.run(
            source=input_path,
            output_path=output_path,
            validate=validate,
            reference_df=reference_df
        )

        logger.info("Procesamiento completado exitosamente")
        logger.info("Filas procesadas: %d", len(df))
        logger.info("Columnas generadas: %d", len(df.columns))
        logger.info("Datos guardados en: %s", output_path)

        return df

    except Exception as e:
        logger.error("Error en procesamiento: %s", str(e))
        raise
