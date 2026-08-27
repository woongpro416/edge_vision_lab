# Day 30 Review — 기존 Detection Service를 재사용해 FastAPI Boundary를 다시 구성한다.
from fastapi import FastAPI
from pydantic import BaseModel, Field

from week03.d16 import DetectionResult
from week04.d28 import build_dto_detections

from fastapi.testclient import TestClient

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


def test_happy_case():

    client = TestClient(app)

    response = client.post(
        "/detections",
        json={"confidenceThreshold": 0.7},
    )

    body = response.json()

    assert response.status_code == 200
    assert len(body) == 2


def test_empty_case():

    client = TestClient(app)

    response = client.post(
        "/detections",
        json={"confidenceThreshold": 1.0},
    )

    body = response.json()

    assert response.status_code == 200
    assert body == []


def test_invalid_case():

    client = TestClient(app)

    response = client.post(
        "/detections",
        json={"confidenceThreshold": 1.1},
    )

    assert response.status_code == 422
