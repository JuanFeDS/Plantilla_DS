"""Dummie model"""
from src.logger import get_logger
from src.config.settings import DB_CONFIG

def dummie_model():
    """Run the dummie model."""
    logger = get_logger(__name__)
    logger.info('Dummie model')

    db_host = DB_CONFIG['host']
    db_name = DB_CONFIG['name']
    db_port = DB_CONFIG['port']

    logger.info(
        'Configuración de BD cargada - Host: %s, DB: %s, Puerto: %s',
        db_host,
        db_name,
        db_port
    )
