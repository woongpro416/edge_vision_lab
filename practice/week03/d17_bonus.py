# Day 17 보너스: perf_counter로 mock detection 변환 시간 한 번 측정

from time import perf_counter
from week03.d16 import convert_detections


def measure_convert_detections_once(
    raw_results: list[dict],
    threshold: float,
) -> float:
    start = perf_counter()

    convert_detections(raw_results, threshold)

    end = perf_counter()

    elapsed_ms = (end - start) * 1000

    return elapsed_ms


def main() -> None:
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

    elapsed_ms = measure_convert_detections_once(raw_results, threshold)

    print(f"convert_detections latency: {elapsed_ms:.3f}ms")

if __name__ == "__main__":
    main()
