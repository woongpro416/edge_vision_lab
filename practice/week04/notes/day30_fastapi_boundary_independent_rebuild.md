# Day 30 — FastAPI Boundary 전체 재구현

## 오늘 목표

기존 Day 28 Detection Service의 Adapter, Filtering, `DetectionResult` 변환 로직은 수정하지 않고, FastAPI가 HTTP Request/Response Boundary 역할만 하도록 다시 연결했다.

## 구현 전 Architecture

```text
Client JSON
→ Pydantic DetectionRequest
→ Validation
→ FastAPI Endpoint
→ build_dto_detections(model_results, threshold)
→ list[DetectionResult]
→ HTTP JSON response
→ TestClient response.json()
```

## HTTP Contract

| 항목 | 결정 |
| --- | --- |
| Method | `POST` |
| Path | `/detections` |
| Request body | `{"confidenceThreshold": 0.70}` |
| Request DTO | `DetectionRequest` |
| Field | `confidenceThreshold: float` |
| Valid range | `0.0 <= confidenceThreshold <= 1.0` |
| Valid response | `200` + Detection 목록 |
| Empty response | `200` + `[]` |
| Invalid response | `422` |

## 책임 분리

| 계층 | 책임 |
| --- | --- |
| Pydantic Request DTO | Client JSON의 자료형과 범위를 검증하고 `DetectionRequest` 객체를 만든다. |
| Endpoint | 검증된 요청 객체에서 threshold `float`를 꺼내 기존 Service를 호출하고 결과를 반환한다. |
| Existing Detection Service | Raw model results를 Adapter → Filtering → `DetectionResult` 목록으로 변환한다. |
| FastAPI | Endpoint를 HTTP route에 연결하고 반환값을 JSON 응답으로 직렬화한다. |

Endpoint에는 filtering loop, raw-result mapping, `DetectionResult(...)` 생성 로직을 넣지 않았다. 기존 Pipeline을 한 번 호출해 Service 책임을 보호했다.

## 자료형 흐름

```text
Client Request JSON: {"confidenceThreshold": 0.70}
→ Endpoint parameter: DetectionRequest
→ Service argument: threshold float + model_results list[dict]
→ Service return: list[DetectionResult]
→ HTTP Response JSON: list[dict] 또는 []
```

`TestClient.response.json()`은 서버 내부의 `DetectionResult` 객체가 아니라, HTTP JSON을 다시 읽은 Python `list`다. 탐지가 있으면 원소는 `dict`이고, 결과가 없으면 `[]`다.

## 테스트

`week04/tests/test_d30.py`에서 TestClient로 다음 Contract를 확인했다.

| Request | 기대 결과 | 결과 |
| --- | --- | --- |
| `confidenceThreshold = 0.70` | `200`, Detection 2건 | 통과 |
| `confidenceThreshold = 1.0` | `200`, `[]` | 통과 |
| `confidenceThreshold = 1.1` | `422` | 통과 |

가상환경에서 `python -m pytest week04/tests/test_d30.py` 실행 결과는 `3 passed`였다.

## Review 독립 재구현

`d30_review.py`에서 요구사항만 보고 같은 Boundary를 다시 작성했다. 처음에는 Service에 `0.70`을 고정 전달해 Empty Contract가 깨질 수 있음을 발견했다. 이후 `request.confidenceThreshold`를 Service의 threshold argument로 연결해 Valid / Empty / Invalid 3개 테스트를 모두 통과시켰다.

Review 파일은 짧은 독립 재현 연습을 위해 API와 TestClient 테스트를 한 파일에 두었다. 일반 프로젝트에서는 API 모듈과 `test_*.py` 파일을 분리하는 편이 더 적합하다.

## 핵심 구분

- `app = FastAPI()`는 HTTP route를 등록하고 TestClient가 요청을 보낼 대상이 되는 FastAPI 애플리케이션 객체를 만든다.
- `200 + []`은 유효한 요청이 정상 처리됐지만 조건을 만족한 Detection이 0건이라는 뜻이다.
- `422`는 Pydantic validation 실패로 Endpoint와 Detection Service가 실행되기 전에 요청이 차단됐다는 뜻이다.
- FastAPI를 제거해도 순수 Python Detection Service는 남아 직접 호출하거나 단위 테스트할 수 있다.

## 공항·관제 도메인 연결

공항 CCTV Dashboard가 표시 기준값을 JSON으로 보내면 FastAPI는 그 값을 검증해 내부 Detection Service로 연결한다. Detection Logic 자체는 Service가 담당하며, FastAPI는 Dashboard와 내부 Service 사이의 HTTP Boundary다. 이는 학습용 구조이며 실제 공항 시스템을 구현했다는 의미는 아니다.

## 다음 학습 포인트

Day 31에서는 기존 해답을 열지 않고, `request → service → response → test` Contract를 먼저 정한 뒤 제한 시간 안에 작은 Detection API를 재구현한다.

## 면접용 설명

"기존 Detection Pipeline은 순수 Python Service로 유지하고, FastAPI에는 HTTP Boundary만 구현했습니다. Pydantic Request DTO로 confidence threshold의 타입과 범위를 검증한 뒤, Endpoint가 검증된 float를 기존 Pipeline에 전달했습니다. TestClient로 정상 결과, 정상 빈 결과, 검증 실패 422를 확인했습니다."
