# Day 31 — Detection API 90분 Cold Rebuild

from fastapi import FastAPI
from pydantic import BaseModel, Field

from week03.d16 import DetectionResult

app = FastAPI()


class DetectionRequest(BaseModel):
    confidenceThreshold: float = Field(ge=0.0, le=1.0)


def build_adapt_detections(model_results: list[dict]) -> list[dict]:
    raw_results = []

    for detection in model_results:
        detections = {
            "bbox": detection["xyxy"],
            "class_id": detection["class_id"],
            "className": detection["class_name"],
            "confidence": detection["confidence"]
        }
        raw_results.append(detections)
    return raw_results


def filter_detections(raw_results: list[dict], threshold: float) -> list[dict]:
    filtered_results = []

    for detection in raw_results:
        if detection["confidence"] >= threshold:
            filtered_results.append(detection)

    return filtered_results


def build_detectionresults(filtered_results: list[dict]) -> list[DetectionResult]:

    detection_results = []

    for detection in filtered_results:
        detections = DetectionResult(**detection)
        detection_results.append(detections)

    return detection_results



def build_dto_detections(model_results: list[dict], threshold: float) -> list[DetectionResult]:

    adapt_results = build_adapt_detections(model_results)
    filtered_results = filter_detections(adapt_results, threshold)
    detection_results = build_detectionresults(filtered_results)
    return detection_results




@app.post("/detections", response_model=list[DetectionResult])
def object_detections(request: DetectionRequest) -> list[DetectionResult]:
    model_results = [
        {
            "xyxy": [40, 60, 280, 370],
            "class_id": 0,
            "class_name": "person",
            "confidence": 0.91,
        },
        {
            "xyxy": [310, 90, 520, 260],
            "class_id": 2,
            "class_name": "vehicle",
            "confidence": 0.74,
        },
        {
            "xyxy": [550, 120, 690, 290],
            "class_id": 1,
            "class_name": "bag",
            "confidence": 0.42,
        },
    ]

    threshold = request.confidenceThreshold

    dto_results = build_dto_detections(model_results, threshold)

    return dto_results

