# Day 19 테스트: DetectionResponse helper와 FastAPI 응답 계약을 검증한다.

from week03.d19 import build_detection_response, DetectionResponse, app
from fastapi.testclient import TestClient

def test_build_detection_response_threshold_0_8():
    raw_results = [
        {
            "bbox": [120, 80, 300, 220],
            "class_id": 0,
            "className": "vehicle",
            "confidence": 0.87,
        },
        {
            "bbox": [400, 100, 480, 280],
            "class_id": 1,
            "className": "person",
            "confidence": 0.76,
        },
    ]
    threshold = 0.8

    response_model = build_detection_response(raw_results, threshold)

    assert isinstance(response_model, DetectionResponse)
    assert response_model.detectionCount == 1
    assert response_model.confidenceThreshold == 0.8
    assert len(response_model.results) == 1
    assert response_model.results[0].className == "vehicle"
    assert response_model.results[0].confidence == 0.87


def test_build_detection_response_threshold_0_7():
    raw_results = [
        {
            "bbox": [120, 80, 300, 220],
            "class_id": 0,
            "className": "vehicle",
            "confidence": 0.87,
        },
        {
            "bbox": [400, 100, 480, 280],
            "class_id": 1,
            "className": "person",
            "confidence": 0.76,
        },
    ]
    threshold = 0.7

    response_model = build_detection_response(raw_results, threshold)

    assert isinstance(response_model, DetectionResponse)
    assert response_model.detectionCount == 2
    assert response_model.confidenceThreshold == 0.7
    assert len(response_model.results) == 2
    assert response_model.results[0].className == "vehicle"
    assert response_model.results[1].className == "person"
    assert response_model.results[1].confidence == 0.76

def test_predict_mock_threshold_0_8():

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

def test_predict_mock_threshold_0_7():

    client = TestClient(app)

    response = client.post(
        "/api/predict/mock",
        json={"confidenceThreshold": 0.7},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["detectionCount"] == 2
    assert body["confidenceThreshold"] == 0.7
    assert len(body["results"]) == 2
    assert body["results"][0]["className"] == "vehicle"
    assert body["results"][1]["className"] == "person"

def test_predict_mock_rejects_invalid_threshold():

    client = TestClient(app)

    response = client.post(
        "/api/predict/mock",
        json={"confidenceThreshold": 1.1},
    )

    assert response.status_code == 422
