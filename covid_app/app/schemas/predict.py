from typing import Any, List, Optional

from pydantic import BaseModel

# 🔹 Schema for prediction results
class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: Optional[Any]   # can be list, dict, or string depending on your model

    class Config:
        schema_extra = {
            "example": {
                "errors": None,
                "version": "1.0.0",
                "predictions": {"label": "cat", "confidence": 0.97}
            }
        }
