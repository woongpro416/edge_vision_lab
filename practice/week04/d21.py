# Day 21 학습: Mock YOLO 모델 결과를 서비스용 raw detection으로 변환하는 adapter

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

    detections = convert_detections(raw_results, threshold)

    print(detections)
    return detections

if __name__ == "__main__":
    main()
