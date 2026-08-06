from pydantic import BaseModel, Field, ValidationError

from pathlib import Path

from week01.d6 import read_image_safe
from week02.d8 import prepare_model_input_simple
from week02.d9 import run_mock_inference
from week02.d10 import filter_detections_by_confidence
from week02.d11 import build_filtered_inference_response

class InferenceResponse(BaseModel):
    status: str
    rawDetectionCount: int = Field(ge=0)
    detectionCount: int = Field(ge=0)
    confidenceThreshold: float = Field(ge=0.0, le=1.0)
    classCounts: dict[str, int]
    results: list[dict]


def main():
    image_path = Path("week01/inputs/sample.jpg")
    bgr_image = read_image_safe(image_path)
    model_input = prepare_model_input_simple(bgr_image, 640, 480)
    raw_results = run_mock_inference(model_input)
    threshold = 0.8
    filtered_results = filter_detections_by_confidence(raw_results, threshold)
    response_data = build_filtered_inference_response(raw_results, filtered_results, threshold)

    response_model = InferenceResponse(**response_data)

    print(type(response_model))
    print(response_model.rawDetectionCount)
    print(response_model.detectionCount)
    print(type(response_model.results))

    serialized_response = response_model.model_dump()
    assert isinstance(response_model, InferenceResponse)
    assert isinstance(serialized_response, dict)

    assert response_model.rawDetectionCount == 2
    assert response_model.detectionCount == 1
    assert response_model.confidenceThreshold == 0.8
    assert serialized_response["status"] == "OK"
    assert serialized_response["results"] == response_data["results"]

    invalid_response_data = response_data.copy()
    invalid_response_data["confidenceThreshold"] = 1.1

    try:
        InferenceResponse(**invalid_response_data)
    except ValidationError:
        print("confidenceThreshold validation failed")

    return serialized_response


if __name__ == "__main__":
    main()
