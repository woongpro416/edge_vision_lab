# Day 18 Review: latency 목록을 avg, max, p95 summary로 다시 구현하기
# 원본 코드를 import하지 않고 함수 계약과 빈 입력 처리를 복습한다.

import numpy as np

def summarize_latency_metrics(latencies: list[float]) -> dict:
    if len(latencies) == 0:
        raise ValueError("측정된 지연시간이 없습니다.")

    sample_count = len(latencies)
    avg_latency = sum(latencies) / sample_count
    max_latency = max(latencies)
    p95_latency = float(np.percentile(latencies, 95))

    summary = {
        "sampleCount" : sample_count,
        "avgLatencyMs" : avg_latency,
        "maxLatencyMs" : max_latency,
        "p95LatencyMs" : p95_latency,
    }

    return summary

def main() -> None:
    latencies = [42.0, 55.0, 48.0, 70.0, 45.0]

    summary = summarize_latency_metrics(latencies)

    print(summary)

if __name__ == "__main__":
    main()
