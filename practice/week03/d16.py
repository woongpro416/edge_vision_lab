# Day 16 학습: Mock YOLO Detection Output을 DetectionResult DTO로 변환한다.

from pydantic import BaseModel, Field
from week02.d10 import filter_detections_by_confidence


class DetectionResult(BaseModel):
    bbox: list[int]
    class_id: int = Field(ge=0)
    className: str
    confidence: float = Field(ge=0.0, le=1.0)


def main():
    raw_results = [
        {
        "bbox": [120, 80, 300, 220],
        "class_id": 0,
        "className": "vehicle",
        "confidence": 0.87,
        },
        {"bbox": [400, 100, 480, 280],
        "class_id": 1,
        "className": "person",
        "confidence": 0.76,
        }
    ]

    threshold = 0.8

    detections = convert_detections(raw_results, threshold)

    print(type(raw_results))
    print(len(detections))
    print(type(detections[0]))
    print(detections[0].className)

    return detections

def convert_detections(
    raw_results: list[dict],
    threshold: float,


) -> list[DetectionResult]:
    filtered_results = filter_detections_by_confidence(raw_results, threshold)
    results_list = []
    for raw_detection in filtered_results:
        detection = DetectionResult(**raw_detection)
        results_list.append(detection)

    return results_list



if __name__ == "__main__":
    main()
