# Edge Vision Lab

Python 기반 AI Vision 결과가 API 응답으로 변환되는 과정을 직접 이해하고 재구성한 학습 repository입니다.
Model Output을 서비스 계약으로 바꾸는 Adapter, confidence Filtering, Pydantic DTO, FastAPI HTTP boundary를 분리했습니다.
최종 범위는 고정된 Mock Model Result를 사용하는 Detection API이며, `POST /detections`가 검증된 threshold에 따라 `list[DetectionResult]`를 반환합니다.
별도로 pretrained `yolo11n.pt` inference와 `Results`/`Boxes`/Tensor 기반 Adapter, threshold 비교 실험을 수행했습니다.
실제 YOLO inference와 FastAPI API는 연결하지 않았습니다.
주요 도구는 Python, FastAPI, Pydantic, pytest, OpenCV, Ultralytics YOLO입니다.

## Architecture

```text
Client
  → Pydantic Validation
  → FastAPI Endpoint
  → Mock Model Output
  → Adapter
  → Filtering
  → DetectionResult
  → HTTP JSON Response
```

- **Pydantic Validation**: `confidenceThreshold`를 `float`, `0.0~1.0` 범위로 검증합니다.
- **Endpoint**: 검증된 threshold와 Mock Model Result를 Detection pipeline에 연결합니다.
- **Adapter**: Model Contract의 `xyxy`, `class_name`을 Service Contract의 `bbox`, `className`으로 변환합니다.
- **Filtering**: `confidence >= threshold` 정책으로 서비스에 반환할 결과를 선택합니다.
- **DetectionResult / FastAPI**: 내부 `dict`를 검증된 DTO와 HTTP JSON response로 변환합니다.

## Core Implementation

- Model Contract의 `xyxy`, `class_name`을 Service Contract의 `bbox`, `className`으로 변환합니다.
- Adapter는 field/type conversion만 담당하고, confidence filtering과 분리했습니다.
- `confidence >= threshold` 조건으로 순서를 유지한 결과 목록을 반환합니다.
- `DetectionRequest`에서 `confidenceThreshold`의 범위를 검증하고, 범위 밖 요청은 `422`로 차단합니다.
- Endpoint는 filtering loop와 DTO 생성 로직을 중복하지 않고 pipeline을 호출합니다.
- `DetectionResult`의 `bbox`, `class_id`, `className`, `confidence`를 response contract로 사용합니다.

## Actual YOLO vs Mock API

| Scope | Actual YOLO experiment | Mock FastAPI API |
| --- | --- | --- |
| Input | pretrained `yolo11n.pt`와 이미지 1장 | 고정된 Mock Model Result 3건 |
| Implemented | `Results`/`Boxes`/Tensor 확인, YOLO Result Adapter, model/service threshold 비교 | Pydantic validation, Adapter, Filtering, `DetectionResult`, Endpoint |
| Verification | Fake YOLO `Results`로 Adapter 및 Empty 결과 contract 테스트 | TestClient로 HTTP Happy / Empty / Invalid contract 테스트 |
| Integration | FastAPI와 연결하지 않음 | 실제 YOLO를 호출하지 않음 |

## Testing

`pytest`와 FastAPI `TestClient`로 service 및 HTTP contract를 검증합니다. 현재 repository의 테스트 스위트는 모두 통과했습니다.

| Case | Request | Expected |
| --- | --- | --- |
| Happy | `confidenceThreshold: 0.7` | `200` + detections 2건 |
| Empty | `confidenceThreshold: 1.0` | `200` + `[]` |
| Invalid | `confidenceThreshold: 1.1` | `422` |

## Engineering Decisions

- Detection 한 건은 이름 있는 field를 표현하는 `dict`, 여러 건은 항상 순회 가능한 `list[dict]`로 다룹니다.
- Empty Detection은 오류나 미생성을 뜻하는 `None`이 아니라 정상 결과인 `[]`로 표현합니다.
- Adapter는 모델 형식 변환만 담당하며 detection을 제거하지 않습니다.
- Filtering은 서비스 정책인 `confidence >= threshold`만 담당합니다.
- Endpoint는 HTTP boundary로 유지하고 Detection Logic은 pipeline에 둡니다.

후반부에는 기존 답안을 보지 않고 요구사항에서 Input/Output Contract와 책임 경계를 먼저 정의한 뒤, 작은 Mock Detection API를 다시 구성했습니다. 이 과정에서 Happy, Empty, Invalid를 서로 다른 contract로 검증했습니다.

## Limitations

- FastAPI API는 고정된 Mock Model Result 기반입니다.
- Actual YOLO inference와 FastAPI는 연결하지 않았습니다.
- image upload 및 API 내부 OpenCV preprocessing은 구현하지 않았습니다.
- YOLO training/fine-tuning, DB, 인증, deployment는 범위 밖입니다.
- bbox는 현재 `list[int]` 계약이므로 YOLO의 float 좌표 정밀도를 보존하지 않습니다.
- 공항·관제는 실제 시스템이 아닌 학습용 domain scenario입니다.

## How to Run

현재 repository의 `practice/.venv` 환경 기준 PowerShell 명령입니다.

```powershell
# repository root에서 실행: Week 1 tests
cd practice\week01
& ..\.venv\Scripts\python.exe -m pytest tests -q

# practice directory에서 실행: Week 2~4 tests and Mock API
cd ..
& .\.venv\Scripts\python.exe -m pytest week02\tests week03\tests week04\tests -q
& .\.venv\Scripts\python.exe -m uvicorn week04.d31:app --reload
```
