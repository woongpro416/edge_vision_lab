
# Day 17 복습: latency summary와 빈 리스트 검증을 다시 구현

def summarize_latencies(latencies: list[float]) -> dict:

    if len(latencies) == 0:
        raise ValueError("지연값이 존재하지 않습니다.")

    sample_count = len(latencies)

    avg_latency = sum(latencies) / sample_count

    max_latency = max(latencies)

    latency_dict = {
        "sampleCount": sample_count,
        "avgLatencyMs": avg_latency,
        "maxLatencyMs": max_latency,
    }

    return latency_dict


def main() -> None:

    latencies = [42.0, 55.0, 48.0, 70.0, 45.0]

    summary = summarize_latencies(latencies)


    print(summary)

if __name__ == "__main__":
    main()
