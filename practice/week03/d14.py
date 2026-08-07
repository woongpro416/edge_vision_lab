# ?? ??: Day 14 ? FastAPI POST request body? Pydantic Request DTO? ?????.

from fastapi import FastAPI
from pydantic import BaseModel, Field

from week02.d10 import filter_detections_by_confidence
from week02.d11 import build_filtered_inference_response
from week03.d12 import InferenceResponse


app = FastAPI()


class PredictMockRequest(BaseModel):
    confidenceThreshold: float = Field(ge=0.0, le=1.0)


def build_mock_prediction(threshold: float) -> InferenceResponse:

    raw_results = [
        {"className": "vehicle", "confidence": 0.87},
        {"className": "person", "confidence": 0.76},
    ]

    filtered_results = filter_detections_by_confidence(raw_results, threshold)

    response_data = build_filtered_inference_response(raw_results, filtered_results, threshold)

    response_model = InferenceResponse(**response_data)

    return response_model


@app.post(
    "/api/predict/mock",
    response_model=InferenceResponse,
)
def predict_mock(request: PredictMockRequest) -> InferenceResponse:

    threshold = request.confidenceThreshold

    response_model = build_mock_prediction(threshold)

    return response_model
