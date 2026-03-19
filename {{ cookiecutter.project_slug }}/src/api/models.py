"""
Modelos Pydantic para la API.

Define los esquemas de request y response para los endpoints.
"""
from typing import List, Dict
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Esquema para solicitud de predicción individual."""

    edad: int = Field(
        ...,
        ge=18,
        le=100,
        description="Edad del cliente"
    )
    ingreso_mensual: float = Field(
        ...,
        ge=0,
        description="Ingreso mensual"
    )
    antiguedad_meses: int = Field(
        ...,
        ge=0,
        description="Antigüedad en meses"
    )

    class Config:
        """Configuración del modelo Pydantic."""

        schema_extra = {
            "example": {
                "edad": 35,
                "ingreso_mensual": 50000.0,
                "antiguedad_meses": 24
            }
        }


class PredictionResponse(BaseModel):
    """Esquema para respuesta de predicción."""

    prediction: int = Field(
        ...,
        description="Clase predicha (0 o 1)"
    )
    probability: float = Field(
        ...,
        ge=0,
        le=1,
        description="Probabilidad"
    )
    model_version: str = Field(
        ...,
        description="Versión del modelo"
    )


class BatchPredictionRequest(BaseModel):
    """Esquema para solicitud de predicción por lotes."""

    instances: List[PredictionRequest] = Field(
        ...,
        description="Lista de instancias para predicción"
    )


class BatchPredictionResponse(BaseModel):
    """Esquema para respuesta de predicción por lotes."""

    predictions: List[PredictionResponse] = Field(
        ...,
        description="Lista de predicciones"
    )
    total_processed: int = Field(
        ...,
        description="Total de instancias procesadas"
    )


class ModelInfo(BaseModel):
    """Esquema para información del modelo."""

    name: str = Field(
        ...,
        description="Nombre del modelo"
    )
    version: str = Field(
        ...,
        description="Versión del modelo"
    )
    algorithm: str = Field(
        ...,
        description="Algoritmo utilizado"
    )
    metrics: Dict[str, float] = Field(
        ...,
        description="Métricas de evaluación"
    )
    features: List[str] = Field(
        ...,
        description="Features utilizadas"
    )


class HealthResponse(BaseModel):
    """Esquema para respuesta de health check."""

    status: str = Field(
        ...,
        description="Estado del servicio"
    )
    model_loaded: bool = Field(
        ...,
        description="Si el modelo está cargado"
    )
    version: str = Field(
        ...,
        description="Versión de la API"
    )
