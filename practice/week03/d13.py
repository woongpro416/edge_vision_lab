# 학습 요약: Day 13 — FastAPI GET health·mock prediction response endpoint를 연습한다.

from fastapi import FastAPI
from week03.d12 import InferenceResponse

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "OK"}


@app.get("/api/predict/mock", response_model=InferenceResponse)
def predict_mock():
    response_data = {
        "status": "OK",
        "rawDetectionCount": 2,
        "detectionCount": 1,
        "confidenceThreshold": 0.8,
        "classCounts": {"vehicle": 1},
        "results": [{"className": "vehicle", "confidence": 0.87}],
    }

    model = InferenceResponse(**response_data)

    return model
