# Day 29 테스트 — Request Validation → Detection Pipeline
from fastapi.testclient import TestClient
from week04.d29 import app


def test_threshold_0_7():

    client = TestClient(app)

    response = client.post(
        "/api/predict/mock",
        json={"confidenceThreshold": 0.7},
    )

    body = response.json()

    assert response.status_code == 200
    assert len(body) == 2
    assert body[0]["className"] == "person"
    assert body[1]["className"] == "vehicle"


def test_threshold_0_0():

    client = TestClient(app)

    response = client.post(
        "/api/predict/mock",
        json={"confidenceThreshold": 0.0},
    )

    body = response.json()

    assert response.status_code == 200
    assert len(body) == 3


def test_threshold_under():

    client = TestClient(app)

    response = client.post(
        "/api/predict/mock",
        json={"confidenceThreshold": -0.1},
    )

    assert response.status_code == 422


def test_threshold_high():

    client = TestClient(app)

    response = client.post(
        "/api/predict/mock",
        json={"confidenceThreshold": 1.1},
    )

    assert response.status_code == 422
