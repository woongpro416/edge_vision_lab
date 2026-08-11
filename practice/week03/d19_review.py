# Day 19 복습: FastAPI 없이 raw detection 목록을 DetectionResponse로 변환한다.

from pydantic import BaseModel, Field
from week03.d16 import DetectionResult, convert_detections


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

    print(response_model)


if __name__ == "__main__":
    main()
