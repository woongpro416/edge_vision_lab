# Day 26 pytest: confidence filtering Happy/Empty 계약 검증
from week04.d26 import filtering_detection_results

def test_happy_path_results():
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
    mock_results = filtering_detection_results(detections, threshold)

    assert len(mock_results) == 1
    assert mock_results[0]["confidence"] == 0.87

def test_empty_case_result():
    detections = []

    threshold = 0.8
    empty_results = filtering_detection_results(detections, threshold)

    assert empty_results == []
