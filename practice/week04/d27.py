# Day 27 학습: Filtering Service Contract와 Invalid Boundary
def build_filtered_results(detections: list[dict],
                     threshold: float,):

    results = []

    for detection in detections:
        if detection["confidence"] >= threshold:
            results.append(detection)

    return results
