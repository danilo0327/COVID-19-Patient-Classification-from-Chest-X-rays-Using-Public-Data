import json
from typing import Any
import tempfile
import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, File
from loguru import logger
from covid_app.app.model import __version__ as model_version
from covid_app.app.model.predict import make_prediction
from covid_app.app import __version__, schemas
from covid_app.app.config import settings

api_router = APIRouter()

# Ruta para verificar que la API se esté ejecutando correctamente
@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    """
    Root Get
    """
    health = schemas.Health(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
    )

    return health.dict()

# Ruta para realizar las predicciones
@api_router.post("/predict", status_code=200)
async def predict(file: UploadFile = File(...)) -> Any:
    """
    Predicción usando el modelo con una imagen de entrada
    """

    # Leer bytes de la imagen
    contents = await file.read()

    logger.info(f"Making prediction on uploaded file: {file.filename}")

    try:
        # 🔹 Aquí asumo que tu make_prediction ya puede manejar imágenes
        #     Si no, tendrás que modificar make_prediction para aceptar `bytes`

        # Guardar la imagen como archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        # Pasar la ruta del archivo a tu función
        results = make_prediction(tmp_path)
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Error while making prediction")

    if isinstance(results, dict) and results.get("errors") is not None:
        logger.warning(f"Prediction validation error: {results.get('errors')}")
        raise HTTPException(status_code=400, detail=json.loads(results["errors"]))

    logger.info(f"Prediction results: {results}")

    return results
