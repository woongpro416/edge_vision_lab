# Day 20 학습: 요구사항 기반 FastAPI 탐지 결과 통합 Endpoint

from fastapi import FastAPI

from week03.d15 import PredictMockRequest
from week03.d19 import DetectionResponse, build_detection_response


app = FastAPI()


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
        {
            "bbox": [400, 100, 480, 280],
            "class_id": 2,
            "className": "baggage",
            "confidence": 0.62,
        },
    ]
    response_model = build_detection_response(raw_results, threshold)

    return response_model
