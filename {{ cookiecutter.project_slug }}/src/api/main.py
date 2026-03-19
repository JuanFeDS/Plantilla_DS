"""
API FastAPI para servir predicciones del modelo.

Este módulo proporciona endpoints REST para realizar predicciones
con el modelo de machine learning.

Referencia: docs/ops/deployment.md
"""
from typing import Dict, Any, List

from fastapi import FastAPI, HTTPException

from src.api.models import (
    PredictionResponse,
    BatchPredictionRequest,
    ModelInfo
)
from src.logger import get_logger

logger = get_logger(__name__)


app = FastAPI(
    title="ML Model API",
    description="API para servir predicciones del modelo de ML",
    version="1.0.0"
)


@app.get("/health")
def health_check() -> Dict[str, Any]:
    """
    Endpoint de health check.

    Returns:
        Estado del servicio y versión del modelo
    """
    return {
        "status": "healthy",
        "model_version": "1.0.0",
        "uptime_seconds": 3600
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict():
    """
    Realiza predicción individual.

    Returns:
        Predicción con probabilidad y metadata

    Raises:
        HTTPException: Si hay error en la predicción

    Ejemplo:
        POST /predict
        {
            "edad": 35,
            "ingreso_mensual": 50000,
            "score_crediticio": 720,
            "num_productos": 2,
            "antiguedad_meses": 24
        }
    """
    logger.info("Predicción individual solicitada")
    raise NotImplementedError(
        "Implementa la lógica de predicción cargando el modelo y usando request.edad, "
        "request.ingreso_mensual, request.antiguedad_meses"
    )


@app.post("/predict/batch")
def predict_batch(request: BatchPredictionRequest) -> List[PredictionResponse]:
    """
    Realiza predicciones por lotes.

    Args:
        request: Lista de instancias para predicción

    Returns:
        Lista de predicciones
    """
    if len(request.instances) > 100:
        raise HTTPException(
            status_code=400,
            detail="Máximo 100 instancias por request"
        )

    raise NotImplementedError(
        "Implementa predicción por lotes. "
        "Considera usar vectorización para mejor performance."
    )


@app.get("/model/info", response_model=ModelInfo)
async def model_info():
    """
    Endpoint para obtener información del modelo.

    Retorna metadata del modelo en producción.
    """
    logger.info("Información del modelo solicitada")
    raise NotImplementedError(
        "Implementa la lógica para retornar información del modelo cargando metadata JSON"
    )


@app.get("/metrics")
async def metrics():
    """
    Endpoint para métricas de Prometheus.

    Expone métricas en formato Prometheus para monitoreo.
    """
    logger.info("Métricas solicitadas")
    raise NotImplementedError(
        "Implementa la exposición de métricas usando prometheus_client"
    )
