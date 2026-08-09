# 학습 요약: Day 15 — TestClient로 정상 filtering과 잘못된 요청의 validation 실패를 검증한다.

from fastapi.testclient import TestClient

from week03.d15 import app

client = TestClient(app)


def test_predict_mock_threshold_0_8():
    response = client.post(
        "/api/predict/mock",
        json={"confidenceThreshold": 0.8},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["rawDetectionCount"] == 2
    assert body["detectionCount"] == 1
    assert body["classCounts"] == {"vehicle": 1}
    assert len(body["results"]) == 1


def test_predict_mock_rejects_invalid_threshold():
    response = client.post(
        "/api/predict/mock",
        json={"confidenceThreshold": 1.1},
    )

    body = response.json()

    assert response.status_code == 422
