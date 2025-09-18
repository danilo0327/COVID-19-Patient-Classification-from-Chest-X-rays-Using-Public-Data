import os, tempfile
from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, HTTPException, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from loguru import logger

from covid_app.app.model import __version__ as model_version
from covid_app.app.model.predict import predict_with_probs
from covid_app.app import __version__, schemas
from covid_app.app.config import settings
from covid_app.app.schemas import PredictionResults, PredictionPayload  # tipado pydantic

api_router = APIRouter()
templates = Jinja2Templates(directory="covid_app/app/templates")

@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    return schemas.Health(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
    ).dict()

# JSON (para clientes programáticos)
@api_router.post("/predict", response_model=PredictionResults, status_code=200)
async def predict_json(file: UploadFile = File(...)) -> PredictionResults:
    contents = await file.read()
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name
        pred, probs = predict_with_probs(tmp_path)
        return PredictionResults(
            errors=None,
            version=model_version,
            predictions=PredictionPayload(pred=pred, probs=probs),
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Error while making prediction")
    finally:
        try:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
        except Exception:
            pass

# HTML (renderiza el reporte en index.html)
@api_router.post("/predict_html", response_class=HTMLResponse)
async def predict_html(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    upload_dir = Path("covid_app/app/static/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = None
    try:
        # 1) Guardar imagen para previsualización
        filename = f"{uuid4().hex}_{file.filename}"
        saved_path = upload_dir / filename
        with open(saved_path, "wb") as f:
            f.write(contents)
        image_url = f"/static/uploads/{filename}"

        # 2) Predecir
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        pred, probs = predict_with_probs(tmp_path)  # probs 0-1
        probs_pct = {k: round(v * 100.0, 2) for k, v in probs.items()}

        result = {
            "pred": pred,
            "probs": probs_pct,        # porcentajes 0-100
            "image_url": image_url,    # para mostrar la RX
        }

        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": result
        })

    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Error while making prediction")
    finally:
        try:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
        except Exception:
            pass
