# ?? ??: Day 12 Review ? Pydantic response DTO? field validation? ?????.

from pydantic import BaseModel, Field


class InferenceResponse(BaseModel):
    status: str

    detectionCount: int = Field(ge=0)

    rawDetectionCount: int = Field(ge=0)

    confidenceThreshold: float = Field(ge=0.0, le=1.0)

    classCounts: dict[str, int]

    results: list[dict]


def main():

    response_data = {
    "status": "OK",
    "rawDetectionCount": 2,
    "detectionCount": 1,
    "confidenceThreshold": 0.8,
    "classCounts": {"vehicle": 1},
    "results": [{"className": "vehicle", "confidence": 0.87}],
    }


    response_model = InferenceResponse(**response_data)

    serialized_response = response_model.model_dump()

    assert isinstance(response_model, InferenceResponse)
    assert isinstance(serialized_response, dict)

    return serialized_response


if __name__ == "__main__":
    print(main())