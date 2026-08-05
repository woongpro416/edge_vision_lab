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
    # TODO: VALID_RESPONSE_DATA로 model을 생성한다.
    model = InferenceResponse(**VALID_RESPONSE_DATA)
    # TODO: rawDetectionCount, detectionCount, confidenceThreshold,
    #       classCounts, results 길이를 assert한다.
    assert model.rawDetectionCount == 2
    assert model.detectionCount == 1
    assert model.confidenceThreshold == 0.8
    assert model.classCounts == {"vehicle": 1}
    assert len(model.results) == 1


def test_invalid_threshold():
    # TODO: VALID_RESPONSE_DATA 복사본의 confidenceThreshold를 1.1로 바꾼다.
    invalid = VALID_RESPONSE_DATA.copy()
    invalid["confidenceThreshold"] = 1.1
    # TODO: pytest.raises(ValidationError) 안에서 DTO 생성을 시도한다.
    with pytest.raises(ValidationError):
        InferenceResponse(**invalid)

def test_invalid_detection_count():
    # TODO: VALID_RESPONSE_DATA 복사본의 detectionCount를 -1로 바꾼다.
    invalid = VALID_RESPONSE_DATA.copy()
    invalid["detectionCount"] = -1
    # TODO: pytest.raises(ValidationError) 안에서 DTO 생성을 시도한다.
    with pytest.raises(ValidationError):
        InferenceResponse(**invalid)