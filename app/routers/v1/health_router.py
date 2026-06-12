"""
Health check y documentacion.
"""
from fastapi import APIRouter, status

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "message": "ErgoDocente API is running",
    }


@router.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {
        "nombre": "ErgoDocente API",
        "version": "1.0.0",
        "descripcion": "Backend para app de ergonomia y bienestar para docentes",
        "endpoints_disponibles": {
            "v1": "/api/v1",
            "docs": "/docs",
            "redoc": "/redoc",
        },
    }