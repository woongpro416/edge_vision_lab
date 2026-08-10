# Day 18 학습: Latency p95와 반복 측정으로 latency summary 만들기
# 개별 실행 시간(ms)을 수집한 뒤 avg, max, p95 metric으로 요약한다.

import numpy as np
from time import perf_counter
from week03.d16 import convert_detections


def summarize_latency_metrics(
        latencies: list[float]
) -> dict:
    if len(latencies) == 0:
        raise ValueError("지연 값이 존재하지 않습니다.")

    sample_count = len(latencies)

    avg_latency = sum(latencies) / sample_count

    max_latency = max(latencies)

    p95_latency = float(np.percentile(latencies, 95))

    summary = {
        "sampleCount": sample_count,
        "avgLatencyMs": avg_latency,
        "maxLatencyMs": max_latency,
        "p95LatencyMs": p95_latency,
    }

    return summary


def measure_convert_detections_runs(
        raw_results: list[dict],
        threshold: float,
        repeat_count: int,
) -> list[float]:
    latencies = []

    for _ in range(repeat_count):
        start = perf_counter()
        convert_detections(raw_results, threshold)
        end = perf_counter()
        elapsed_ms = (end - start) * 1000
        latencies.append(elapsed_ms)

    return latencies


def main() -> None:
    repeat_count = 20

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

    latencies = measure_convert_detections_runs(
        raw_results, threshold, repeat_count
    )

    summary = summarize_latency_metrics(latencies)

    print(summary)


if __name__ == "__main__":
    main()
