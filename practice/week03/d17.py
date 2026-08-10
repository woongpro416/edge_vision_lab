# Day 17 학습: AI inference latency의 개수·평균·최대값 요약

def summarize_latencies(latencies: list[float]) -> dict:
    # TODO 1: latencies가 비어 있으면 ValueError 발생
    if len(latencies) == 0:
        raise ValueError("지연시간 값이 존재하지 않습니다.")

    sample_count = len(latencies)

    avg_latency = sum(latencies) / len(latencies)

    max_latency = max(latencies)

    latency_dict = {
        "sampleCount": sample_count,
        "avgLatencyMs": avg_latency,
        "maxLatencyMs": max_latency
    }

    return latency_dict


def main() -> None:
    latencies = [42.0, 55.0, 48.0, 70.0, 45.0]

    summary = summarize_latencies(latencies)

    print(summary)

if __name__ == "__main__":
    main()
