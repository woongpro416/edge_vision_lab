# Day 25 테스트: Service Confidence Threshold Filtering 검증

from week03.d16 import convert_detections


def test_service_threshold_keeps_only_confidences_at_least_0_7():
    raw_results = [
        {
            "bbox": [10, 20, 100, 200],
            "class_id": 0,
            "className": "person",
            "confidence": 0.91,
        },
        {
            "bbox": [150, 30, 300, 220],
            "class_id": 2,
            "className": "car",
            "confidence": 0.72,
        },
        {
            "bbox": [320, 50, 400, 180],
            "class_id": 0,
            "className": "person",
            "confidence": 0.55,
        },
    ]

    detections = convert_detections(raw_results, threshold=0.7)
    confidences = [detection.confidence for detection in detections]

    assert len(detections) == 2
    assert confidences == [0.91, 0.72]
    assert 0.55 not in confidences
