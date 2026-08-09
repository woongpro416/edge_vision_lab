# 학습 요약: Day 12 테스트 — Pydantic InferenceResponse validation을 pytest로 검증한다.

import pytest
from pydantic import ValidationError

from week03.d12 import InferenceResponse


VALID_RESPONSE_DATA = {
    "status": "OK",
    "rawDetectionCount": 2,
    "detectionCount": 1,
    "confidenceThreshold": 0.8,
    "classCounts": {"vehicle": 1},
    "results": [{"className": "vehicle", "confidence": 0.87}],
}


def test_valid_response():
    model = InferenceResponse(**VALID_RESPONSE_DATA)
    assert model.rawDetectionCount == 2
    assert model.detectionCount == 1
    assert model.confidenceThreshold == 0.8
    assert model.classCounts == {"vehicle": 1}
    assert len(model.results) == 1


def test_invalid_threshold():
    invalid = VALID_RESPONSE_DATA.copy()
    invalid["confidenceThreshold"] = 1.1
    with pytest.raises(ValidationError):
        InferenceResponse(**invalid)


def test_invalid_detection_count():
    invalid = VALID_RESPONSE_DATA.copy()
    invalid["detectionCount"] = -1
    with pytest.raises(ValidationError):
        InferenceResponse(**invalid)
