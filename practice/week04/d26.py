
# Day 26 구현: Detection confidence filtering service
def filtering_detection_results(detections: list[dict], threshold: float):
    results = []
    for detection in detections:
        if detection['confidence'] >= threshold:
            results.append(detection)
    return results
