"""
Pipeline completo de procesamiento de datos.

Este módulo orquesta el flujo completo desde carga de datos crudos
hasta features listas para modelado.
"""
from typing import Optional, Dict, Any
from pathlib import Path

import pandas as pd

from src.data.preprocessing import (
    clean_missing_values,
    remove_duplicates,
    convert_dates,
    normalize_text
)
from src.data.quality_checks import run_quality_pipeline
from src.features.engineering import (
    create_date_features,
    encode_categorical,
    scale_features
)


class DataPipeline:
    """
    Pipeline completo de procesamiento de datos.

    Este pipeline ejecuta todos los pasos necesarios para transformar
    datos crudos en features listas para modelado.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el pipeline.

        Args:
            config: Configuración del pipeline (rutas, parámetros, etc.)
        """
        self.config = config or {}
        self.data = None
        self.quality_report = None

    def load_data(self, source: str, **kwargs) -> pd.DataFrame:
        """
        Carga datos desde la fuente especificada.

        Args:
            source: Ruta al archivo de datos
            **kwargs: Argumentos adicionales para carga

        Returns:
            DataFrame con datos cargados
        """
        file_ext = Path(source).suffix.lower()

        if file_ext == '.csv':
            self.data = pd.read_csv(source, **kwargs)
        elif file_ext in ['.xlsx', '.xls']:
            self.data = pd.read_excel(source, **kwargs)
        elif file_ext == '.parquet':
            self.data = pd.read_parquet(source, **kwargs)
        else:
            raise ValueError(f"Formato no soportado: {file_ext}")

        return self.data

    def validate_quality(self, reference_df: Optional[pd.DataFrame] = None) -> bool:
        """
        Valida calidad de los datos.

        Args:
            reference_df: DataFrame de referencia para comparación

        Returns:
            True si pasa validaciones, False en caso contrario
        """
        self.quality_report = run_quality_pipeline(self.data, reference_df)
        return self.quality_report.get('passed', False)

    def clean_data(self) -> pd.DataFrame:
        """
        Limpia los datos (missing values, duplicados, etc.).

        Returns:
            DataFrame limpio
        """
        self.data = remove_duplicates(self.data)
        self.data = clean_missing_values(self.data, strategy='median')
        return self.data

    def transform_data(self) -> pd.DataFrame:
        """
        Aplica transformaciones a los datos.

        Returns:
            DataFrame transformado
        """
        date_columns = self.config.get('date_columns', [])
        if date_columns:
            self.data = convert_dates(self.data, date_columns)

        text_columns = self.config.get('text_columns', [])
        if text_columns:
            self.data = normalize_text(self.data, text_columns)

        return self.data

    def engineer_features(self) -> pd.DataFrame:
        """
        Crea features derivadas.

        Returns:
            DataFrame con features adicionales
        """
        date_columns = self.config.get('date_columns', [])
        for col in date_columns:
            self.data = create_date_features(self.data, col)

        categorical_columns = self.config.get('categorical_columns', [])
        if categorical_columns:
            self.data = encode_categorical(self.data, categorical_columns)

        numerical_columns = self.config.get('numerical_columns', [])
        if numerical_columns:
            self.data = scale_features(self.data, numerical_columns)

        return self.data

    def save_processed_data(self, output_path: str) -> None:
        """
        Guarda datos procesados.

        Args:
            output_path: Ruta donde guardar los datos
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        file_ext = Path(output_path).suffix.lower()

        if file_ext == '.csv':
            self.data.to_csv(output_path, index=False)
        elif file_ext == '.parquet':
            self.data.to_parquet(output_path, index=False)
        else:
            raise ValueError(f"Formato no soportado para guardar: {file_ext}")

    def run(
        self,
        source: str,
        output_path: str,
        validate: bool = True,
        reference_df: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """
        Ejecuta el pipeline completo.

        Args:
            source: Ruta a datos crudos
            output_path: Ruta para guardar datos procesados
            validate: Si True, valida calidad de datos
            reference_df: DataFrame de referencia para validación

        Returns:
            DataFrame procesado
        """
        self.load_data(source)

        if validate:
            if not self.validate_quality(reference_df):
                raise ValueError("Validación de calidad falló. Ver quality_report.")

        self.clean_data()
        self.transform_data()
        self.engineer_features()
        self.save_processed_data(output_path)

        return self.data
