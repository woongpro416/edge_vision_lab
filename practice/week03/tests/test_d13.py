# 학습 요약: Day 13 테스트 — FastAPI GET mock response와 404 동작을 pytest로 검증한다.

from fastapi.testclient import TestClient

from week03.d13 import app


client = TestClient(app)


def test_predict_mock_returns_expected_response():
    response = client.get("/api/predict/mock")
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "OK"
    assert body["rawDetectionCount"] == 2
    assert body["detectionCount"] == 1
    assert body["confidenceThreshold"] == 0.8
    assert body["classCounts"] == {"vehicle": 1}
    assert len(body["results"]) == 1


def test_unknown_predict_path_returns_404():
    response = client.get("/api/predict/unknown")

    assert response.status_code == 404
