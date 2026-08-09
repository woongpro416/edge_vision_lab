# Day 16 복습: mock raw detection을 filtering한 뒤 DetectionResult DTO로 변환한다.

from week02.d10 import filter_detections_by_confidence
from pydantic import BaseModel, Field

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

    filtered_results = filter_detections_by_confidence(raw_results, threshold)

    detections = []

    for raw_detection in filtered_results:
        detection = DetectionResult(**raw_detection)
        detections.append(detection)

    print(len(detections))
    print(detections[0].className)

    return detections

if __name__ == "__main__":
    main()
