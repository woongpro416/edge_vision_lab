# Day 26 재구현: Detection filtering 함수
def filtered_detection(detections: list[dict], threshold: float):
    results = []

    for detection in detections:
        if detection["confidence"] >= threshold:
            results.append(detection)

    return results


def mock_filtered_detection():
    detections = [
        {
            "bbox": [100, 300, 200, 400],
            "class_id": 0,
            "className": 'person',
            "confidence": 0.87,
        },
        {
            "bbox": [200, 400, 300, 500],
            "class_id": 1,
            "className": 'car',
            "confidence": 0.72,
        },
        {
            "bbox": [30, 50, 80, 120],
            "class_id": 2,
            "className": 'airplane',
            "confidence": 0.62,
        },
    ]

    threshold = 0.8

    mock_detection = filtered_detection(detections, threshold)
    print(mock_detection)
    return mock_detection

mock_filtered_detection()

