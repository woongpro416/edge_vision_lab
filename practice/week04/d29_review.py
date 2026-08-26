# Day 29 Review — Request Validation → Detection Pipeline 독립 재구현
from fastapi import FastAPI
from pydantic import BaseModel, Field

from week03.d16 import DetectionResult
from week04.d28 import build_dto_detections


app = FastAPI()


class PredictMockRequest(BaseModel):
    confidenceThreshold: float = Field(ge=0.0, le=1.0)


@app.post("/api/predict/mock", response_model=list[DetectionResult])
def predict_mock(request: PredictMockRequest) -> list[DetectionResult]:
    threshold = request.confidenceThreshold

    model_results = [
        {
            "xyxy": [120, 80, 360, 420],
            "class_id": 0,
            "class_name": "person",
            "confidence": 0.91,
        },
        {
            "xyxy": [400, 150, 620, 510],
            "class_id": 1,
            "class_name": "vehicle",
            "confidence": 0.76,
        },
        {
            "xyxy": [700, 210, 810, 390],
            "class_id": 2,
            "class_name": "baggage",
            "confidence": 0.58,
        },
    ]

    return build_dto_detections(model_results, threshold)
