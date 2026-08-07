# Day 14 — FastAPI POST Request Body와 Pydantic Request DTO

## 오늘 목표

고정된 GET mock response를 POST API로 확장했다. Client가 JSON request body로 confidence threshold를 보내면, 서버가 request DTO로 검증하고 mock detection filtering 결과를 `InferenceResponse`로 반환한다.

## 구현한 내용

- `PredictMockRequest`에 `confidenceThreshold: float`와 `0.0~1.0` 범위 validation을 정의했다.
- `build_mock_prediction(threshold)` helper에서 고정 mock detections를 준비하고, Day 10 filtering과 Day 11 response builder를 재사용했다.
- `POST /api/predict/mock` endpoint가 검증된 request DTO에서 threshold를 꺼내 helper에 전달하도록 구현했다.
- `InferenceResponse`를 helper의 반환 계약과 FastAPI `response_model`로 사용했다.
- TestClient로 threshold `0.8`, `0.7`, invalid `1.1` 요청을 직접 테스트했고 `3 passed`를 확인했다.

## Data Flow

```text
Client/TestClient
  → POST JSON {"confidenceThreshold": 0.8}
  → FastAPI request validation
  → request: PredictMockRequest
  → threshold: float
  → build_mock_prediction(threshold)
  → raw_results: list[dict]
  → filtered_results: list[dict]
  → response_data: dict
  → InferenceResponse
  → FastAPI JSON response
  → client response.json(): dict
```

## 정상·실패 요청

| Request | 예상 결과 |
|---|---|
| `{"confidenceThreshold": 0.8}` | 200, raw 2개, filtered 1개, vehicle만 반환 |
| `{"confidenceThreshold": 0.7}` | 200, raw 2개, filtered 2개, vehicle·person 반환 |
| `{"confidenceThreshold": 1.1}` | 422 request validation error, endpoint/helper 미실행 |
| `{}` | 422 request validation error, required field 누락 |

## 어려웠던 지점과 정리

### 1. Client와 server의 코드 경계

- 처음에는 `response.json()`을 server endpoint 안에서 쓰는 코드로 혼동했다.
- `client.post(..., json=...)`는 client/test가 request JSON을 보내는 코드다.
- `response.json()`은 server가 validation, filtering, response serialization을 마친 뒤 client/test가 response JSON을 Python dict로 읽는 코드다.

### 2. Request DTO와 function의 차이

- `PredictMockRequest`는 실행 동작이 아니라 request data의 모양과 규칙을 선언하는 class다.
- 따라서 `def`가 아니라 `class PredictMockRequest(BaseModel)`을 사용한다.
- `confidenceThreshold: float = Field(ge=0.0, le=1.0)`에서 `float`는 자료형이고 `Field`는 범위 validation 규칙이다.

### 3. Endpoint와 helper의 책임 분리

- FastAPI는 JSON을 `PredictMockRequest`로 만들고 validation한다.
- Endpoint는 검증된 `request`에서 threshold를 꺼내 helper에 전달하고 결과를 반환한다.
- Helper는 HTTP request를 받지 않고 `threshold: float`만 받아 raw results, filtering, response DTO 생성을 담당한다.
- 이 구조면 pytest나 batch job도 HTTP request 없이 helper를 재사용할 수 있다.

### 4. 자료형과 DTO 생성 시점

- `raw_results`와 `filtered_results`는 `list[dict]`다.
- `response_data`는 response field를 모두 담은 `dict`다.
- `InferenceResponse(**response_data)`는 response data dict를 검증된 response model로 바꾼다.
- raw results list를 곧바로 `InferenceResponse(**raw_results)`로 만들 수는 없다.

### 5. POST 선택 이유

POST를 선택한 이유는 client가 처리 조건을 request body로 보내고, server가 그 값으로 prediction filtering 작업을 수행하기 때문이다. 단순히 JSON을 쓴다는 이유만으로 POST를 선택하는 것은 아니다.

## 학습 방식 회고

처음에는 한 줄짜리 빈칸 TODO에 정답을 거의 드러내는 방식으로 진행되어, 요구사항에서 구조를 추론하는 연습이 부족했다. 이후에는 다음 방식으로 바꾸기로 했다.

1. 도메인 상황과 success/failure 조건을 먼저 본다.
2. request/response 방향, validation 위치, 책임 분리를 짧게 설계한다.
3. 함수·endpoint·pytest 함수처럼 의미 있는 블록을 먼저 독립 구현한다.
4. 막히면 추론 질문 → 개념 힌트 → 계약 힌트 → 정확한 코드 순으로 도움을 받는다.
5. 테스트 assertion 작성과 pytest 실행은 직접 한다.

## 공항·관제 도메인 연결

공항 CCTV나 restricted zone monitoring API에서는 client가 camera metadata와 처리 조건을 보내고, 서버가 detection filtering 결과를 dashboard·alert system·Spring backend에 전달할 수 있다. 다만 실제 운영에서는 모든 client가 threshold를 자유롭게 바꾸게 하기보다 server configuration, 관리자 정책, camera별 설정, 권한 검사를 통해 filtering policy를 관리해야 한다.

## 현재 한계와 다음 단계

- 오늘은 고정 mock detections만 사용했다.
- 실제 image upload, OpenCV preprocessing, YOLO/ONNX inference, database, authentication은 구현하지 않았다.
- 다음 단계에서는 POST request body, Request DTO, endpoint-helper boundary를 코드 없이도 먼저 설명한 뒤 작은 기능으로 구현한다.

## 면접용 설명

"FastAPI POST endpoint에서 Pydantic Request DTO로 client input을 validation하고, endpoint는 HTTP contract를 service helper에 연결했습니다. Helper는 threshold 기반 filtering과 response DTO 생성을 담당하도록 분리해 HTTP 없이도 테스트·재사용할 수 있게 했습니다."

## 추천 commit message

`feat: add FastAPI POST mock prediction request validation`

## 오늘 학습 기록 5줄

- POST request body는 client가 server에 processing condition을 전달하는 통로다.
- Request DTO는 외부 입력을 endpoint 전에 검증하는 API boundary다.
- Endpoint는 HTTP request를 helper input으로 연결하고, helper는 실제 filtering 결과를 만든다.
- `response.json()`은 server 코드가 아니라 client/test가 response body를 읽는 코드다.
- 공항 운영 환경의 threshold는 client 자유 입력보다 server policy와 권한으로 관리하는 편이 안전하다.
