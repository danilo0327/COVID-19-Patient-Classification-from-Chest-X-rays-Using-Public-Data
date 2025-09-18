from typing import Any
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

from covid_app.app.api import api_router
from covid_app.app.config import settings, setup_app_logging

# setup logging as early as possible
setup_app_logging(config=settings)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

root_router = APIRouter()

# Montar /static (para servir imágenes subidas)
app.mount("/static", StaticFiles(directory="covid_app/app/static"), name="static")

templates = Jinja2Templates(directory="covid_app/app/templates")

# Home
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Routers
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

# CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == "__main__":
    logger.warning("Running in development mode. Do not run like this in production.")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
