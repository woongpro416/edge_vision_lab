# Day 17 테스트: latency summary의 normal, single, empty 입력 검증

from week03.d17 import summarize_latencies
import pytest


def test_summarize_latencies_normal():
    latencies = [42.0, 55.0, 48.0, 70.0, 45.0]

    summary = summarize_latencies(latencies)

    assert summary["sampleCount"] == 5

    assert summary["avgLatencyMs"] == 52.0

    assert summary["maxLatencyMs"] == 70.0


def test_summarize_latencies_single_value():
    latencies = [50.0]

    summary = summarize_latencies(latencies)

    assert summary["sampleCount"] == 1

    assert summary["avgLatencyMs"] == 50.0

    assert summary["maxLatencyMs"] == 50.0


def test_summarize_latencies_rejects_empty_list():
    latencies = []

    with pytest.raises(ValueError):
        summarize_latencies(latencies)
