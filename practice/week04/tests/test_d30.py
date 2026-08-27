# Day 30 테스트 — Valid, Empty, Invalid HTTP Contract를 검증한다.
from fastapi.testclient import TestClient
from week04.d30 import app


def test_happy_case():

    client = TestClient(app)

    response = client.post(
        "/detections",
        json={"confidenceThreshold": 0.7},
    )

    body = response.json()

    assert response.status_code == 200
    assert len(body) == 2


def test_threshold_1_0():

    client = TestClient(app)

    response = client.post(
        "/detections",
        json={"confidenceThreshold": 1.0},
    )

    body = response.json()

    assert response.status_code == 200
    assert body == []


def test_threshold_1_1():

    client = TestClient(app)

    response = client.post(
        "/detections",
        json = {"confidenceThreshold": 1.1},
    )

    assert response.status_code == 422
