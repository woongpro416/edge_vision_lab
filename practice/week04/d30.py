# Day 30 — Existing Detection Service에 FastAPI Boundary를 연결한다.
from fastapi import FastAPI
from pydantic import BaseModel, Field

from week03.d16 import DetectionResult
from week04.d28 import build_dto_detections

app = FastAPI()


class DetectionRequest(BaseModel):
    confidenceThreshold: float = Field(ge=0.0, le=1.0)


@app.post("/detections", response_model=list[DetectionResult])
def detection(request: DetectionRequest) -> list[DetectionResult]:
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
    threshold = request.confidenceThreshold

    dto_results = build_dto_detections(model_results, threshold)

    return dto_results
