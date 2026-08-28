# Day 31 — Detection API 90분 Cold Rebuild

## 오늘 목표

기존 학습 내용을 보지 않고 작은 Detection API의 `request → validation → endpoint → adapter → filtering → DTO → response → test` 흐름을 다시 구성한다.

## Cold Rebuild 규칙

- 실제 YOLO, 이미지 업로드, DB 등은 추가하지 않는다.
- Mock Detection 3건과 confidence threshold만 사용한다.
- `DetectionResult` DTO는 기존 Contract를 사용하고, Adapter·Filtering·DTO 변환 Pipeline은 Day 31 안에서 다시 작성한다.

## 구현 전 요구사항

- `POST /detections`는 JSON body의 `confidenceThreshold`를 받는다.
- threshold는 `0.0` 이상 `1.0` 이하여야 한다.
- Mock Model 결과는 `xyxy`, `class_id`, `class_name`, `confidence`를 가진 여러 Detection이다.
- Adapter는 서비스용 `bbox`, `class_id`, `className`, `confidence` 형식으로만 변환한다.
- Filtering은 `confidence >= threshold`만 남긴다.
- 유효하지만 결과가 없으면 `200 + []`, 범위 밖 요청은 `422`다.

## 구현 전 Contract

```text
Request: {"confidenceThreshold": 0.70}
Response: list[DetectionResult] → HTTP JSON list[dict]
Empty: HTTP 200, []
Invalid: HTTP 422, Endpoint와 Service 실행 전 validation 실패
```

## 구현 전 Architecture

```text
Client JSON
→ Pydantic DetectionRequest validation
→ FastAPI Endpoint
→ Mock Model Output: list[dict]
→ Adapter: list[dict]
→ Filtering: list[dict] + threshold
→ DetectionResult 변환: list[DetectionResult]
→ HTTP JSON Response
```

## Request DTO 책임

`DetectionRequest`는 `confidenceThreshold: float`의 타입과 `0.0 <= value <= 1.0` 범위를 검증한다. 잘못된 값은 Endpoint 본문 전에 FastAPI의 `422` 응답으로 차단된다.

## Endpoint 책임

Endpoint는 검증된 Request에서 threshold를 꺼내고, Mock Model 결과와 함께 Pipeline을 호출한 뒤 `list[DetectionResult]`를 반환한다.

## Adapter 책임

Adapter는 Model Contract의 `xyxy`, `class_name`을 Service Contract의 `bbox`, `className`으로 매핑한다. Detection을 제거하지 않으므로 3건 입력은 3건 출력이다.

## Filtering Service 책임

Filtering은 변환된 Detection 한 건의 `confidence`와 threshold를 비교한다. `confidence >= threshold`인 Detection만 새 목록에 담는다.

## DetectionResult 책임

Filtering 후 남은 Service Contract dict 한 건을 `DetectionResult` DTO 한 건으로 만든다. 최종 Python 반환값은 `list[DetectionResult]`이고 FastAPI가 HTTP JSON으로 직렬화한다.

## 첫 구현과 Contract 기준 오류 분석

처음에는 Day 28의 전체 Pipeline을 import해 Endpoint에 연결했다. API 기능 테스트는 통과했지만, Adapter·Filtering·DTO 변환을 독립적으로 재구성하는 Day 31 목표를 충족하지 못했다. 이후 Day 31 안에 세 책임과 Pipeline을 다시 작성했다.

수정 과정에서 두 오류가 발생했다.

1. Pipeline 함수 내부에서 Adapter 대신 Pipeline 자신을 호출해 `threshold` 인자가 빠진 `TypeError`가 발생했다. Pipeline의 첫 단계는 `model_results: list[dict]`를 받는 Adapter여야 한다.
2. Filtering에서 전체 목록인 `raw_results: list[dict]`를 dict처럼 `raw_results["confidence"]`로 읽으려 했다. 반복 중인 Detection 한 건은 `dict`이고, 그 dict에서 꺼낸 `detection["confidence"]`가 비교할 `float`다.

## Data Flow가 끊긴 지점

초기 구현은 Pipeline의 첫 호출이 잘못되어 Adapter Output까지 도달하지 못했다. 수정 후에는 `model_results → adapted_results → filtered_results → detection_results`가 순서대로 이어진다.

## Happy Test

`confidenceThreshold = 0.70` 요청에서 다음을 검증했다.

- HTTP status `200`
- Detection 수 `2`
- 첫 결과의 `className == "person"`
- 첫 결과의 `confidence == 0.91`

이 테스트는 filtering 수뿐 아니라 Adapter field mapping과 JSON 응답 일부도 함께 확인한다.

## Valid Empty Test

`confidenceThreshold = 1.0` 요청에서 HTTP `200`과 `[]`를 검증했다. 유효한 요청이지만 통과한 Detection이 없는 정상 상태를 증명한다.

## Invalid Request Test

`confidenceThreshold = 1.1` 요청에서 HTTP `422`를 검증했다. Pydantic validation boundary가 범위 밖 값을 차단한다.

## 최종 테스트 결과

```text
.venv\\Scripts\\python.exe -m pytest week04/tests/test_d31.py -q
3 passed
```

## 현재 독립 구현 가능한 범위

- Pydantic Request DTO로 float 범위 검증
- FastAPI Endpoint에서 Request 값을 Service Pipeline으로 전달
- Model Contract → Service Contract Adapter
- confidence filtering
- `list[DetectionResult]` 응답과 TestClient의 JSON 검증

## 아직 외부 참고가 필요한 부분

- 함수 이름을 작성하기 전에 Input/Output 자료형을 더 빠르게 확정하는 연습
- `list[dict]` 전체와 반복 중인 `dict` 한 건을 변수 이름으로 명확히 구분하는 연습
- Pipeline Architecture를 코드 없이 짧게 설명하는 연습

## Week 7 Gate 평가

| Gate | 상태 | 근거 |
| --- | --- | --- |
| A. dict, list[dict], DTO 선택 설명 | 보완 필요 | 각 자료형 흐름은 구현했지만 선택 이유를 말로 더 연습해야 한다. |
| B. Service Input / Output 결정 | 보통 | 구현과 수정 후에는 명확했지만 초기에 Pipeline 호출 경계를 혼동했다. |
| C. pytest Arrange / Act / Assert | 보통 | Happy, Empty, Invalid HTTP 테스트를 직접 실행했고 Happy assertion을 보강했다. |

## 공항·관제 도메인 연결

공항 제한구역 CCTV Dashboard는 confidence 기준만 API에 보낸다. Model의 원본 field는 Adapter가 내부 Service Contract로 제한하고, Filtering은 표시 정책만 담당한다. 이는 실제 공항 시스템이나 실제 YOLO inference가 아닌 학습용 Mock API다.

## 다음 학습 포인트

Day 32에서는 새 기능을 추가하지 않고 Data Contract, Responsibility Boundary, FastAPI, Pydantic, pytest, Adapter, Filtering, DTO에서 반복된 오류를 코드 없이 설명하는 Review를 진행한다.

## 면접용 설명

"FastAPI Endpoint에는 HTTP Request/Response 역할만 두고, Mock Model 결과는 Adapter에서 서비스용 필드로 변환했습니다. Filtering은 `confidence >= threshold` 정책만 담당하며, 통과한 결과를 Pydantic `DetectionResult` 목록으로 반환했습니다. TestClient로 정상 결과, 정상 빈 결과, validation 422를 확인했습니다."
