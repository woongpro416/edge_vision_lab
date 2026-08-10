# Day 18 Tests: p95 latency summary와 반복 측정 결과를 검증하기
# normal, single, empty, repeat count 계약을 확인한다.

import pytest
from week03.d18 import summarize_latency_metrics
from week03.d18 import measure_convert_detections_runs


def test_normal():
    latencies = [42.0, 55.0, 48.0, 70.0, 45.0]

    summary = summarize_latency_metrics(latencies)

    assert summary["sampleCount"] == 5
    assert summary["avgLatencyMs"] == 52.0
    assert summary["maxLatencyMs"] == 70.0
    assert summary["p95LatencyMs"] == pytest.approx(67.0)


def test_single():
    latencies = [42.0]

    summary = summarize_latency_metrics(latencies)

    assert summary["sampleCount"] == 1
    assert summary["avgLatencyMs"] == 42.0
    assert summary["maxLatencyMs"] == 42.0
    assert summary["p95LatencyMs"] == pytest.approx(42.0)


def test_empty():
    latencies = []

    with pytest.raises(ValueError):
        summarize_latency_metrics(latencies)


def test_repeat():
    repeat_count = 3

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

    assert len(latencies) == repeat_count
    assert all(latency >= 0 for latency in latencies)
