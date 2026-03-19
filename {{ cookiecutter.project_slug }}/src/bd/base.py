"""Módulo base para conectores de bases de datos"""
from abc import ABC, abstractmethod
from typing import Dict, Optional
from contextlib import contextmanager
import logging

import pandas as pd

class DatabaseError(Exception):
    """Excepción base para errores de base de datos"""


class QueryError(DatabaseError):
    """Error en la ejecución de consultas"""


class InsertError(DatabaseError):
    """Error durante la inserción de datos"""


class DatabaseConnector(ABC):
    """Clase base abstracta para conectores de bases de datos"""

    def __init__(self, **kwargs):
        self._connection = None
        self._config = kwargs
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def connect(self) -> None:
        """Establece la conexión a la base de datos"""

    @abstractmethod
    def disconnect(self) -> None:
        """Cierra la conexión a la base de datos"""

    @property
    def is_connected(self) -> bool:
        """Verifica si hay una conexión activa"""
        return self._connection is not None

    @contextmanager
    def connection(self):
        """Context manager para manejo seguro de conexiones"""
        try:
            if not self.is_connected:
                self.connect()
            yield self._connection
        except Exception as e:
            self.logger.error("Error de conexión: %s", str(e))
            raise ConnectionError(f"Error de conexión: {str(e)}") from e

    def execute_get_query(self, query: str, params: Optional[Dict] = None) -> pd.DataFrame:
        """
        Ejecuta una consulta y devuelve un DataFrame

        Args:
            query: Consulta SQL a ejecutar (usar placeholders para parámetros)
            params: Parámetros para la consulta

        Returns:
            DataFrame con los resultados
        """
        with self.connection() as conn:
            try:
                result = pd.read_sql(query, conn, params=params)
                return result
            except Exception as e:
                self.logger.error("Error en la consulta: %s", str(e))
                raise QueryError(f"Error en la consulta: {str(e)}") from e

    @abstractmethod
    def execute_insert_df(
        self,
        df: pd.DataFrame,
        table_name: str,
        if_exists: str = "append",
        index: bool = False,
        chunksize: int = 5000,
        **kwargs,
    ) -> int:
        """
        Inserta los datos de un DataFrame en una tabla de la base de datos.

        Args:
            df: DataFrame con los datos a insertar.
            table_name: Nombre de la tabla de destino.
            if_exists: Comportamiento si la tabla existe:
                      - 'fail': Lanza un error si la tabla existe.
                      - 'replace': Elimina la tabla antes de insertar.
                      - 'append': Inserta los datos en la tabla existente.
            index: Si es True, incluye el índice del DataFrame como columna.
            chunksize: Número de filas a insertar por lote.
            **kwargs: Argumentos adicionales para pandas.DataFrame.to_sql().

        Returns:
            Número total de filas insertadas.

        Raises:
            ValueError: Si el parámetro if_exists no es válido.
            InsertError: Si ocurre un error durante la inserción.
        """
        valid_if_exists = ["fail", "replace", "append"]
        if if_exists not in valid_if_exists:
            raise ValueError(f"if_exists debe ser uno de: {', '.join(valid_if_exists)}")

        if df.empty:
            self.logger.warning("El DataFrame está vacío, no hay datos para insertar.")
            raise ValueError("El DataFrame está vacío, no hay datos para insertar.")

        with self.connection() as conn:
            try:
                # Obtener el número de filas antes de la inserción
                count_query = f"SELECT COUNT(*) FROM {table_name}"
                rows_before = pd.read_sql(count_query, conn).iloc[0, 0]

                # Realizar la inserción
                df.to_sql(
                    name=table_name,
                    con=conn,
                    if_exists=if_exists,
                    index=index,
                    chunksize=chunksize,
                    method="multi" if chunksize > 1 else None,
                    **kwargs,
                )
                conn.commit()

                # Calcular y devolver el número de filas insertadas
                rows_after = pd.read_sql(count_query, conn).iloc[0, 0]
                rows_inserted = rows_after - rows_before

                self.logger.info(
                    "Insertadas %d filas en la tabla %s", rows_inserted, table_name
                )
                return rows_inserted

            except Exception as e:
                conn.rollback()
                error_msg = f"Error al insertar en {table_name}: {str(e)}"
                self.logger.error(error_msg)
                raise InsertError(error_msg) from e
