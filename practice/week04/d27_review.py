# Day 27 학습: Filtering Service Contract와 Invalid Boundary 재구현
def build_filtered_results(
    detections: list[dict],
    threshold: float,
):

    results = []
    for detection in detections:
        if detection["confidence"] >= threshold:
            results.append(detection)

    return results


def build_happy_results():
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

    happy_results = build_filtered_results(detections, threshold)
    return happy_results


def build_empty_results():
    detections = []
    threshold = 0.8

    empty_results = build_filtered_results(detections,threshold)
    return empty_results
