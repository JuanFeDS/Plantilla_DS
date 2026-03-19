"""
Módulo para enviar mensajes a Slack mediante webhooks.
"""
import requests

from src.logger import get_logger

logger = get_logger(__name__)

def send_message(webhook_url: str, mensaje: str) -> bool:
    """
    Envía un mensaje a un canal de Slack usando un webhook.
    
    Args:
        webhook_url: URL del webhook de Slack
        mensaje: Texto del mensaje a enviar
        
    Returns:
        bool: True si el mensaje se envió correctamente, False en caso de error
    """
    try:
        payload = {'text': mensaje}

        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return True

    except Exception as error:
        logger.error("Error al enviar mensaje a Slack: %s", error)
        return False
