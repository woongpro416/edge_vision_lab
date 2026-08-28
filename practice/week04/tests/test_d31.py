# Day 31 — Detection API 90분 Cold Rebuild Tests

from fastapi.testclient import TestClient
from week04.d31 import app


def test_0_7():

    client = TestClient(app)

    response = client.post(
        "/detections",
        json={"confidenceThreshold": 0.7},
    )

    body = response.json()

    assert len(body) == 2
    assert response.status_code == 200
    assert body[0]["className"] == "person"
    assert body[0]["confidence"] == 0.91


def test_1_0():

    client = TestClient(app)

    response = client.post(
        "/detections",
        json={"confidenceThreshold": 1.0},
    )

    body = response.json()

    assert response.status_code == 200
    assert body == []


def test_1_1():

    client = TestClient(app)

    response = client.post(
        "/detections",
        json={"confidenceThreshold": 1.1},
    )

    assert response.status_code == 422
