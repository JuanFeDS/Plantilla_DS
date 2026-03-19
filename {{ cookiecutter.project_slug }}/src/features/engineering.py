"""
Módulo para ingeniería de features.

Funciones para crear, transformar y seleccionar features para modelado.
"""
from typing import List, Optional

import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder

def create_date_features(
    df: pd.DataFrame,
    date_column: str,
    features: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Crea features derivadas de una columna de fecha.

    Args:
        df: DataFrame a procesar
        date_column: Columna de fecha
        features: Features a crear ('year', 'month', 'day', 'dayofweek', 'quarter')
                 Si None, crea todas

    Returns:
        DataFrame con nuevas columnas de features temporales
    """
    df_copy = df.copy()
    date_col = pd.to_datetime(df_copy[date_column])

    all_features = ['year', 'month', 'day', 'dayofweek', 'quarter', 'dayofyear']
    features_to_create = features if features else all_features

    for feature in features_to_create:
        if feature == 'year':
            df_copy[f'{date_column}_year'] = date_col.dt.year
        elif feature == 'month':
            df_copy[f'{date_column}_month'] = date_col.dt.month
        elif feature == 'day':
            df_copy[f'{date_column}_day'] = date_col.dt.day
        elif feature == 'dayofweek':
            df_copy[f'{date_column}_dayofweek'] = date_col.dt.dayofweek
        elif feature == 'quarter':
            df_copy[f'{date_column}_quarter'] = date_col.dt.quarter
        elif feature == 'dayofyear':
            df_copy[f'{date_column}_dayofyear'] = date_col.dt.dayofyear

    return df_copy


def create_binned_features(
    df: pd.DataFrame,
    column: str,
    bins: List[float],
    labels: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Crea feature categórica binneando una variable numérica.

    Args:
        df: DataFrame a procesar
        column: Columna a binnear
        bins: Límites de los bins
        labels: Etiquetas para cada bin (opcional)

    Returns:
        DataFrame con nueva columna binneada
    """
    df_copy = df.copy()
    df_copy[f'{column}_bin'] = pd.cut(df_copy[column], bins=bins, labels=labels)
    return df_copy


def create_interaction_features(
    df: pd.DataFrame,
    columns: List[str],
    operation: str = 'multiply'
) -> pd.DataFrame:
    """
    Crea features de interacción entre columnas.

    Args:
        df: DataFrame a procesar
        columns: Lista de columnas para interacción
        operation: Operación ('multiply', 'add', 'divide', 'subtract')

    Returns:
        DataFrame con nueva columna de interacción
    """
    df_copy = df.copy()

    if len(columns) != 2:
        raise ValueError("Se requieren exactamente 2 columnas para interacción")

    col1, col2 = columns
    feature_name = f'{col1}_x_{col2}'

    if operation == 'multiply':
        df_copy[feature_name] = df_copy[col1] * df_copy[col2]
    elif operation == 'add':
        df_copy[feature_name] = df_copy[col1] + df_copy[col2]
    elif operation == 'divide':
        df_copy[feature_name] = df_copy[col1] / df_copy[col2].replace(0, np.nan)
    elif operation == 'subtract':
        df_copy[feature_name] = df_copy[col1] - df_copy[col2]

    return df_copy


def encode_categorical(
    df: pd.DataFrame,
    columns: List[str],
    method: str = 'onehot',
    drop_first: bool = False
) -> pd.DataFrame:
    """
    Codifica variables categóricas.

    Args:
        df: DataFrame a procesar
        columns: Columnas categóricas a codificar
        method: Método de encoding ('onehot', 'label', 'ordinal')
        drop_first: Si True, elimina primera categoría (evita multicolinealidad)

    Returns:
        DataFrame con columnas codificadas
    """
    df_copy = df.copy()

    if method == 'onehot':
        df_copy = pd.get_dummies(
            df_copy,
            columns=columns,
            drop_first=drop_first,
            prefix=columns
        )
    elif method == 'label':
        for col in columns:
            label_encoder = LabelEncoder()
            df_copy[col] = label_encoder.fit_transform(df_copy[col].astype(str))

    return df_copy


def scale_features(
    df: pd.DataFrame,
    columns: List[str],
    method: str = 'standard'
) -> pd.DataFrame:
    """
    Escala features numéricas.

    Args:
        df: DataFrame a procesar
        columns: Columnas a escalar
        method: Método de escalado ('standard', 'minmax', 'robust')

    Returns:
        DataFrame con columnas escaladas
    """
    df_copy = df.copy()

    if method == 'standard':
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
    elif method == 'minmax':
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
    elif method == 'robust':
        from sklearn.preprocessing import RobustScaler
        scaler = RobustScaler()

    df_copy[columns] = scaler.fit_transform(df_copy[columns])
    return df_copy
