# Day 21 복습: model output → adapter → 기존 detection pipeline 연결

from week03.d16 import convert_detections


def build_raw_detection(model_detection: dict) -> dict:
    xyxy = model_detection["xyxy"]
    class_id = model_detection["class_id"]
    class_name = model_detection["class_name"]
    confidence = model_detection["confidence"]

    return {
        "bbox": xyxy,
        "class_id": class_id,
        "className": class_name,
        "confidence": confidence
    }


def main():
    model_detections = [
        {
            "xyxy": [120, 80, 300, 220],
            "class_id": 0,
            "class_name": "vehicle",
            "confidence": 0.87,
        },
        {
            "xyxy": [400, 100, 480, 280],
            "class_id": 1,
            "class_name": "person",
            "confidence": 0.76,
        },
    ]

    raw_results = [
        build_raw_detection(model_detection)
        for model_detection in model_detections
    ]

    threshold = 0.8

    model_response = convert_detections(raw_results, threshold)

    print(len(model_response))
    print(model_response[0].className)

if __name__ == "__main__":
    main()
