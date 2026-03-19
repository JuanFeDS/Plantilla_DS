"""Módulo para la conexión con bases de datos Oracle.

Este módulo proporciona una interfaz para conectarse a bases de datos Oracle utilizando
variables de entorno para la configuración sensible. Las variables deben estar definidas
en un archivo .env en el directorio raíz del proyecto.
"""
from typing import Dict, Optional
from pathlib import Path

import oracledb
import pandas as pd
from dotenv import load_dotenv

from src.bd.base import DatabaseConnector, QueryError, DatabaseError
from src.config.settings import DB_CONFIG
from src.logger import get_logger

# Cargar variables de entorno desde el archivo .env
env_path = Path(__file__).parent.parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class OracleConnector(DatabaseConnector):
    """Conector para bases de datos Oracle.

    Esta clase implementa la funcionalidad específica para conectarse a bases de datos
    Oracle y ejecutar consultas, manteniendo compatibilidad con la interfaz definida
    en DatabaseConnector.
    """

    def __init__(self):
        """Inicializa el conector Oracle."""
        self.logger = get_logger(__name__)
        self._cursor = None
        self._connection = None

        # Configuración de conexión
        self.user = DB_CONFIG["user"]
        self.password = DB_CONFIG["password"]
        self.dsn = DB_CONFIG["dsn"]
        self.lib_dir = DB_CONFIG["lib_dir"]

    def connect(self) -> None:
        """Establece la conexión a la base de datos Oracle.

        Raises:
            ConnectionError: Si no se puede establecer la conexión.
        """
        try:
            if self.lib_dir:
                oracledb.init_oracle_client(lib_dir=self.lib_dir)

            self._connection = oracledb.connect(
                user=self.user,
                password=self.password,
                dsn=self.dsn
            )
            self._cursor = self._connection.cursor()
            self.logger.info("Conexión a Oracle establecida correctamente.")
        except oracledb.Error as error:
            error_msg = f"Error al conectar a Oracle: {str(error)}"
            self.logger.error(error_msg)
            raise DatabaseError(error_msg) from error

    def disconnect(self) -> None:
        """Cierra la conexión a la base de datos."""
        if self._cursor:
            self._cursor.close()
            self._cursor = None

        if self._connection:
            self._connection.close()
            self._connection = None
            self.logger.info("Conexión a Oracle cerrada correctamente.")

    def execute_get_query(
        self, query: str, params: Optional[Dict] = None
    ) -> pd.DataFrame:
        """Ejecuta una consulta y devuelve los resultados como un DataFrame.

        Args:
            query: Consulta SQL a ejecutar.
            params: Parámetros para la consulta (opcional).

        Returns:
            DataFrame con los resultados de la consulta.
        """
        try:
            with self.connection():
                query = query.format(**params) if params else query
                df = pd.read_sql(query, con=self._connection)
                return df

        except Exception as error:
            error_msg = f"Error al ejecutar la consulta: {str(error)}"
            self.logger.error(error_msg)
            raise QueryError(error_msg) from error

    def execute_insert_df(self, df: pd.DataFrame, query: str, chunksize: int = 5000):
        """Función de conveniencia para insertar datos desde un DataFrame.

        Args:
            df: DataFrame con los datos a insertar.
            query: Consulta SQL para la inserción.
            config_path: Ruta al archivo de configuración.
            **kwargs: Parámetros adicionales para el conector.

        Returns:
            Número de filas insertadas.
        """
        # Convertir DataFrame a lista de tuplas con valores convertidos a str y truncados
        rows = [tuple(str(val)[:2000] for val in row) for row in df.values]
        total_rows = len(rows)

        # Inserción de los registros
        try:
            for i in range(0, total_rows, chunksize):
                chunk = rows[i : i + chunksize]
                self._cursor.executemany(query, chunk)
                self._connection.commit()
        except Exception as error:
            self._connection.rollback()
            error_msg = f"Error al insertar los datos: {str(error)}"
            self.logger.error(error_msg)
            raise QueryError(error_msg) from error

    def execute_procedure(self, procedure_name: str, parameters: Optional[list] = None):
        """Ejecuta un procedimiento almacenado.

        Args:
            procedure_name: Nombre del procedimiento a ejecutar.
            parameters: Lista de parámetros para el procedimiento (opcional).
        """
        try:
            with self.connection():
                if parameters:
                    self._cursor.callproc(procedure_name, parameters)
                else:
                    self._cursor.callproc(procedure_name)
                self._connection.commit()
        except Exception as error:
            self._connection.rollback()
            error_msg = (
                f"Error al ejecutar el procedimiento {procedure_name}: {str(error)}"
            )
            self.logger.error(error_msg)
            raise QueryError(error_msg) from error

    def execute_query(self, query: str) -> None:
        """Ejecuta una consulta.

        Args:
            query: Sentencia SQL a ejecutar.
        """
        try:
            with self.connection():
                self._cursor.execute(query)
                self._connection.commit()
        except Exception as error:
            error_msg = f"Error al ejecutar el query: {str(error)}"
            self.logger.error(error_msg)
            raise QueryError(error_msg) from error
