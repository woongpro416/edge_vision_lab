# Day 19 학습: 여러 DetectionResult를 DetectionResponse로 묶어 FastAPI JSON으로 반환한다.

from pydantic import BaseModel, Field
from fastapi import FastAPI
from week03.d16 import DetectionResult, convert_detections
from week03.d15 import PredictMockRequest


app = FastAPI()


class DetectionResponse(BaseModel):
    detectionCount: int = Field(ge=0)

    confidenceThreshold: float = Field(ge=0.0, le=1.0)

    results: list[DetectionResult]



def build_detection_response(
        raw_results: list[dict],
        threshold: float,
) -> DetectionResponse:
    detections = convert_detections(raw_results, threshold)

    detection_count = len(detections)

    response_model = DetectionResponse(
        detectionCount=detection_count,
        confidenceThreshold=threshold,
        results=detections
    )

    return response_model

@app.post("/api/predict/mock", response_model=DetectionResponse)
def predict_mock(request: PredictMockRequest) -> DetectionResponse:
    threshold = request.confidenceThreshold
    raw_results = [
        {
            "bbox": [120, 80, 300, 220],
            "class_id": 0,
            "className": "vehicle",
            "confidence": 0.87,
        },
        {
            "bbox": [400, 100, 480, 280],
            "class_id": 1,
            "className": "person",
            "confidence": 0.76,
        },
    ]

    response_model = build_detection_response(raw_results, threshold)
    return response_model


def main():
    raw_results = [
        {
            "bbox": [120, 80, 300, 220],
            "class_id": 0,
            "className": "vehicle",
            "confidence": 0.87,
        },
        {
            "bbox": [400, 100, 480, 280],
            "class_id": 1,
            "className": "person",
            "confidence": 0.76,
        },
    ]
    threshold = 0.8

    response_model = build_detection_response(raw_results, threshold)

    print(response_model.detectionCount)
    print(response_model.confidenceThreshold)
    print(type(response_model.results[0]))
    print(response_model.results[0].className)


if __name__ == "__main__":
    main()
