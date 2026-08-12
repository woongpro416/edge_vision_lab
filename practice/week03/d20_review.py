# Day 20 복습: 기존 helper를 재사용한 탐지 결과 흐름 확인

from week03.d19 import build_detection_response


def main():
    
    raw_results = [
        {
            "bbox": [120, 80, 300, 220],
            "class_id": 0,
            "className": "vehicle",
            "confidence": 0.87,
        },
        {
            "bbox": [400, 100, 480, 280],
            "class_id": 1,
            "className": "person",
            "confidence": 0.76,
        },
        {
            "bbox": [400, 100, 480, 280],
            "class_id": 2,
            "className": "baggage",
            "confidence": 0.62,
        },
    ]
    threshold = 0.8
    
    response_model = build_detection_response(raw_results, threshold)

    print(response_model.detectionCount)
    print(response_model.results[0].className)

    return response_model

if __name__ == "__main__":
    main()
