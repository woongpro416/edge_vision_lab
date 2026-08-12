# Day 20 테스트: threshold별 탐지 응답 계약과 요청 검증

from fastapi.testclient import TestClient
from week03.d20 import app


def test_threshold_0_8():

    client = TestClient(app)

    response = client.post(
        "/api/predict/mock",
        json={"confidenceThreshold": 0.8},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["detectionCount"] == 1
    assert len(body["results"]) == 1
    assert body["results"][0]["className"] == "vehicle"


def test_threshold_0_5():

    client = TestClient(app)

    response = client.post(
        "/api/predict/mock",
        json={"confidenceThreshold": 0.5},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["detectionCount"] == 3
    assert len(body["results"]) == 3
    assert body["results"][2]["className"] == "baggage"


def test_threshold_1_1():

    client = TestClient(app)

    response = client.post(
        "/api/predict/mock",
        json={"confidenceThreshold": 1.1},
    )


    assert response.status_code == 422
