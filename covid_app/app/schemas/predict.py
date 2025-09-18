from typing import Any, Dict, Optional
from pydantic import BaseModel

class PredictionPayload(BaseModel):
    pred: str
    probs: Dict[str, float]  # {clase: prob}

class PredictionResults(BaseModel):
    errors: Optional[Any] = None
    version: str
    predictions: PredictionPayload

    class Config:
        schema_extra = {
            "example": {
                "errors": None,
                "version": "1.0.0",
                "predictions": {
                    "pred": "Lung_Opacity",
                    "probs": {
                        "COVID": 0.02,
                        "Lung_Opacity": 0.91,
                        "Normal": 0.05,
                        "Viral Pneumonia": 0.02
                    }
                }
            }
        }
