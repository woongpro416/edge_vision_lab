# 학습 요약: Day 14 테스트 — POST threshold filtering과 request validation을 pytest로 검증한다.

from fastapi.testclient import TestClient

from week03.d14 import app


client = TestClient(app)


def test_predict_mock_threshold_0_8():
    response = client.post(
        "/api/predict/mock",
        json={"confidenceThreshold": 0.8}
    )

    body = response.json()

    assert response.status_code == 200
    assert body["rawDetectionCount"] == 2
    assert body["detectionCount"] == 1
    assert body["confidenceThreshold"] == 0.8
    assert body["classCounts"] == {"vehicle": 1}
    assert len(body["results"]) == 1


def test_predict_mock_threshold_0_7():

    response = client.post(
        "/api/predict/mock",
        json = {"confidenceThreshold": 0.7},
    )

    body = response.json()


    assert response.status_code == 200
    assert body["rawDetectionCount"] == 2
    assert body["detectionCount"] == 2
    assert body["confidenceThreshold"] == 0.7
    assert body["classCounts"] == {"vehicle": 1, "person": 1}
    assert len(body["results"]) == 2


def test_predict_mock_rejects_invalid_threshold():
    response = client.post(
        "/api/predict/mock",
        json= {"confidenceThreshold": 1.1}
    )


    assert response.status_code == 422
