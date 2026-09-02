# Day 32 — Week 7 Final Review & Project Closing

## 오늘 목표

새 기능을 구현하지 않고, Day 26~31에서 다룬 작은 Mock Detection API를 요구사항, Data Contract, Responsibility, Data Flow, Test Contract 관점에서 정리한다.

오늘은 `vision_practice` 학습 프로젝트의 마지막 날이다. Week 8의 새 구현으로 바로 확장하지 않고, 지금까지 직접 이해하고 설명할 수 있게 된 범위를 정직하게 마무리한다.

## 오늘의 요구사항 해부

```text
대시보드 팀이 confidence 기준으로 CCTV 탐지 결과를 조회할 수 있어야 한다.
Mock Vision Model 결과를 사용해 Detection API를 구현한다.
```

- Actor: 대시보드 팀
- 원하는 행동: confidence 기준으로 CCTV 탐지 결과를 조회한다.
- Input 후보: `confidenceThreshold`
- Output 후보: threshold를 통과한 Detection 목록
- Data Source: Mock Vision Model이 반환한 여러 Detection 결과

## Requirement Fact와 설계 결정

### Requirement Fact

- 대시보드 팀이 탐지 결과를 조회한다.
- confidence 기준이 필요하다.
- CCTV Detection 결과를 다룬다.
- Mock Vision Model 결과를 사용한다.
- Detection API가 필요하다.

### Design Decision

- `confidenceThreshold`라는 요청 field 이름
- threshold를 `float`, `0.0 <= value <= 1.0`으로 검증
- `DetectionResult` DTO를 외부 Response Contract로 사용
- 탐지 결과가 없으면 `200 + []`를 반환
- Adapter와 Filtering Service를 분리
- HTTP Method와 threshold 전달 위치를 결정

### 아직 확인할 수 있는 항목

- threshold가 누락됐을 때 기본값이 필요한지
- Response에 Detection count가 필요한지
- bbox의 세부 형식
- 실제 API Client가 Dashboard Frontend인지 Backend인지

### 범위 밖

- 실제 YOLO 또는 ONNX inference
- CCTV RTSP 연결과 이미지 업로드
- DB, GPU, Docker, 인증
- NMS, IoU, 성능 최적화, Dashboard UI

## Data Contract 정리

```text
Model Detection 한 건: dict
Model Detection 여러 건: list[dict]
API Response Detection 한 건: DetectionResult
API Response 여러 건: list[DetectionResult]
```

Detection 한 건은 `bbox`, `class_id`, `className`, `confidence`처럼 이름과 의미가 다른 field를 묶어야 한다. 현재 학습 Contract에서는 field 이름으로 읽을 수 있는 `dict`가 이해하기 쉬운 선택이다.

여러 Detection은 항상 같은 목록 Contract를 유지한다.

```text
0건: []
1건: [detection]
여러 건: [detection1, detection2]
```

`[]`는 유효한 요청에서 탐지 결과가 없다는 정상 상태다. `None`은 값 자체가 없거나 계산되지 않았다는 다른 의미이므로 정상 Empty Response에는 사용하지 않는다.

`DetectionResult`는 내부 Service의 raw dict와 외부 Client에 약속한 Response Contract를 분리한다.

## 전체 Data Flow

```text
Client Request
→ Pydantic DetectionRequest Validation
→ FastAPI Endpoint
→ Mock Model Output: list[dict]
→ Adapter: list[dict]
→ Filtering: list[dict] + threshold
→ DTO Conversion: list[DetectionResult]
→ FastAPI JSON Response
```

## Responsibility Boundary

- Pydantic Request DTO: 요청값의 type과 허용 범위를 검증한다.
- Endpoint: 검증된 threshold를 꺼내 Pipeline에 전달하고 결과를 반환한다.
- Adapter: `xyxy → bbox`, `class_name → className`처럼 Model Contract를 Service Contract로 변환한다.
- Filtering Service: `confidence >= threshold` 정책으로 결과를 남긴다.
- DTO Conversion: 내부 `dict` 결과를 외부 `DetectionResult` DTO로 변환한다.
- FastAPI: DTO를 JSON HTTP Response로 직렬화하고 validation 실패를 `422`로 처리한다.
- TestClient: HTTP Request부터 HTTP Response까지의 API Contract를 검증한다.

## 반복 오류 복습

### list[dict]와 dict

`raw_results`는 여러 결과인 `list[dict]`다. 따라서 `raw_results["confidence"]`는 잘못된 접근이다. 반복 중인 `detection` 한 건이 `dict`이고, `detection["confidence"]`가 비교할 `float`다.

### Pipeline 자기 호출

Pipeline의 Input은 `model_results: list[dict]`, `threshold: float`다. 첫 단계는 Pipeline 자신이 아니라 Model 결과를 받을 수 있는 Adapter여야 한다.

```text
model_results
→ Adapter
→ raw_results
→ Filtering
→ filtered_results
→ DTO Conversion
→ list[DetectionResult]
```

## 200 + []와 422

- `confidenceThreshold = 1.0`이고 통과한 Detection이 없을 때: 요청은 유효하므로 `200 + []`
- `confidenceThreshold = 1.1`일 때: Request 자체가 유효하지 않으므로 Pydantic validation 단계에서 `422`

## Test Contract

### Happy Test

`confidenceThreshold = 0.70`에서 confidence가 `0.91`, `0.74`인 두 결과만 반환되는지 확인한다. 이때 HTTP status, Detection 수, Adapter field mapping, Response JSON 일부를 검증한다.

### Valid Empty Test

유효한 threshold에서 조건을 통과한 Detection이 없을 때 HTTP `200`과 `[]`를 확인한다.

### Invalid Test

범위 밖 threshold가 들어오면 HTTP `422`를 확인한다. 이는 Service Filtering이 아니라 Request Validation이 처리하는 오류다.

### Unit Test와 API Test

Adapter Unit Test는 Model dict가 Service dict로 정확히 변환되는지 확인한다. API Test는 HTTP Request가 validation, Pipeline, JSON Response까지 올바르게 이어지는지 확인한다.

## Week 7 마무리 평가

이번 주에는 완성된 코드를 읽는 것보다 요구사항을 보고 작은 Detection API의 Request, Validation, Adapter, Filtering, Response, Test Contract를 나누어 생각하는 연습을 했다.

현재는 아래 범위를 설명하고, 기존 구현을 읽으며 검증할 수 있다.

- Mock Model Output을 `list[dict]`로 받아 Adapter에서 Service Contract로 바꾸는 흐름
- confidence threshold Filtering과 정상 Empty Response의 차이
- Pydantic Validation 오류와 Filtering 결과 0건의 차이
- `list[DetectionResult]` Response Contract와 TestClient 기반 Happy, Empty, Invalid 테스트

처음 보는 요구사항에서 모든 세부 Contract를 즉시 문장으로 완성하는 일은 아직 체크리스트를 함께 사용해야 안정적이다. 이는 다음 프로젝트를 시작하기 전에 다시 확인할 보완 습관으로 남긴다.

## 프로젝트 마무리

`vision_practice`는 여기서 마무리한다. 이 프로젝트에서 실제로 만든 것은 작은 학습용 Vision API Pipeline이며, 실제 YOLO inference, 운영 CCTV 연동, DB 기반 서비스까지 구현한 것은 아니다.

대신 이미지 기본 처리부터 Mock Detection API까지 이어지는 흐름에서, 데이터가 어떤 형태로 들어오고 변환되며 검증되는지를 단계별로 추적하는 기반을 만들었다. 이후 프로젝트에서는 먼저 요구사항을 Contract와 책임으로 나눈 뒤, 작은 기능과 테스트부터 직접 구현한다.

## 공항·관제 도메인 연결

공항 제한구역 CCTV Dashboard라면 Client는 confidence threshold를 보내고, API는 Mock 또는 Model Detection 결과를 Adapter로 내부 형식에 맞춘 뒤 Filtering한다. Dashboard에는 정책을 통과한 결과만 명시적인 Response Contract로 반환한다.

이 학습 프로젝트는 실제 관제 시스템이 아니라, 그러한 서비스의 Request → Validation → Service → Response → Test 흐름을 작게 연습한 것이다.

## 오늘의 핵심 한 줄

자연어 요구사항을 바로 코드로 옮기지 않고, 먼저 Requirement Fact, Contract, Responsibility, Test Behavior로 나눈 뒤 구현한다.
