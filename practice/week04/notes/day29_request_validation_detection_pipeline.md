# Day 29 — Request Validation → Detection Pipeline

## 오늘 목표

기존 Day 28의 `Model → Adapter → Filtering → DetectionResult` Pipeline 앞에 FastAPI Request Validation Boundary를 연결한다.

## 요구사항

- Client는 `confidenceThreshold`를 JSON body로 보낸다.
- `confidenceThreshold`는 `float`이며 `0.0 <= value <= 1.0` 범위여야 한다.
- 범위를 벗어난 요청은 Endpoint와 Pipeline 실행 전에 `422`로 차단한다.
- 정상 요청은 기존 Day 28 Pipeline을 재사용하고 `list[DetectionResult]`를 반환한다.

## 구현 전 Request Contract

| 항목 | 결정 |
| --- | --- |
| Request field | `confidenceThreshold` |
| Python type | `float` |
| 최소값 / 최대값 | `0.0` / `1.0` |
| 정상 예시 | `{"confidenceThreshold": 0.70}` |
| Request range boundary | `0.0`, `1.0` |
| Invalid 예시 | `-0.1`, `1.1` |
| Validation 실패 | HTTP `422` |

`confidenceThreshold`는 Client가 선택한 filtering 기준값이다. 모델이 반환한 각 Detection의 `confidence`와는 다른 값이다.

## 전체 Data Flow

```text
Client JSON dict
→ Pydantic PredictMockRequest 객체
→ Endpoint가 꺼낸 float threshold
→ build_dto_detections(model_results, threshold)
→ list[DetectionResult]
→ FastAPI JSON array
→ TestClient response.json(): list[dict]
```

## 책임 분리

| 계층 | 책임 |
| --- | --- |
| Request DTO | `confidenceThreshold`의 type/range 검증 |
| Endpoint | 검증된 threshold 추출, mock model results 준비, 기존 Pipeline 호출, 결과 반환 |
| Day 28 Pipeline | Adapter → Filtering → DetectionResult 변환 |
| FastAPI | DTO 목록을 HTTP JSON 응답으로 직렬화 |

Endpoint에 Adapter mapping, `for` loop filtering, `DetectionResult` 직접 생성 로직을 다시 작성하지 않았다.

## 구현 결과

- `week04/d29.py`에 `PredictMockRequest`와 POST `/api/predict/mock` Endpoint를 구현했다.
- Endpoint는 `request.confidenceThreshold`로 검증된 `float`를 꺼내 Day 28의 `build_dto_detections()`에 전달한다.
- mock model results의 confidence는 `0.91`, `0.76`, `0.58`을 사용했다.
- `week04/d29_review.py`에서 동일 Contract를 다시 구성했다.

## 테스트

`week04/tests/test_d29.py`에서 TestClient로 4개 Contract를 확인했다.

| 요청값 | 기대 결과 | 확인 결과 |
| --- | --- | --- |
| `0.70` | `200`, Detection 2건 | 통과 |
| `0.0` | `200`, Detection 3건 | 통과 |
| `-0.1` | `422` | 통과 |
| `1.1` | `422` | 통과 |

가상환경에서 `python -m pytest week04/tests/test_d29.py` 실행 결과는 `4 passed`였다.

## 422 Response 확인

`-0.1` 요청의 response body에는 `body → confidenceThreshold` 위치와 `greater_than_equal` validation error가 포함됐다. 이는 JSON request가 Endpoint 본문에 진입하기 전에 Pydantic의 `ge=0.0` 조건에서 차단됐음을 보여 준다.

## Valid Empty와 Invalid Request 차이

- `confidenceThreshold = 1.0`은 정상 상한 Boundary다. 현재 mock Detection이 모두 1.0 미만이므로 정상 `200`과 빈 배열 `[]`가 반환된다.
- `confidenceThreshold = -0.1` 또는 `1.1`은 Request Contract 위반이므로 `422`다.

## 구현 중 확인한 점

- Request DTO는 JSON dict가 아니라 Pydantic 객체이므로 Endpoint에서는 `request.confidenceThreshold`처럼 attribute access를 사용한다.
- TestClient의 `response.json()`은 HTTP JSON을 다시 읽은 Python `list[dict]`다. 서버 내부의 `list[DetectionResult]`와 구분해야 한다.
- Day 28 Pipeline은 이미 Adapter, Filtering, DTO 변환을 담당하므로 Endpoint에서는 Pipeline을 한 번 호출하는 것으로 충분하다.

## 공항·관제 도메인 연결

Dashboard 사용자가 Detection 표시 기준값을 보낼 때, 잘못된 `confidenceThreshold = 1.5`는 Detection Service까지 전달하지 않고 API Request Boundary에서 차단한다. 반면 `1.0`은 유효한 기준값이며 Detection이 없으면 정상 빈 결과를 반환한다.

## 다음 학습 포인트

FastAPI를 새로운 복잡한 Pipeline으로 보지 않고, 기존 순수 Python 서비스 함수를 HTTP Request/Response와 연결하는 얇은 Boundary로 다시 재구성한다. 다음 학습에서는 제한된 기능 하나를 `request → service → response → test` 흐름으로 처음부터 재구현한다.

## 면접용 설명

"Client의 filtering threshold는 Pydantic Request DTO에서 먼저 범위 검증했습니다. Endpoint는 검증된 float 값을 기존 Adapter·Filtering·DetectionResult Pipeline에 전달하고, FastAPI가 최종 DTO 목록을 JSON으로 직렬화하도록 분리했습니다. TestClient로 정상 요청, 하한 Boundary, 범위 밖 요청의 422 Contract를 검증했습니다."
