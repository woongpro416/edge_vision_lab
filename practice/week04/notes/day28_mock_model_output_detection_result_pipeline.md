# Day 28 — Mock Model Output → DetectionResult 독립 재구현

## 오늘 목표

Mock Model Output 여러 건을 Service 내부 Contract로 변환하고, confidence filtering 뒤 기존 `DetectionResult` DTO 목록으로 만드는 작은 Pipeline을 구현한다.

## Day 27 복습

- Detection 한 건은 `dict`, 여러 건은 `list[dict]`로 다룬다.
- Empty `[]`는 탐지 결과가 없는 정상 상태이며 Invalid와 구분한다.
- Filtering 조건 `confidence >= threshold`는 equality boundary를 포함한다.

## 요구사항

```text
Model Detection 여러 건
→ Adapter
→ Service raw_results
→ confidence Filtering
→ DetectionResult 목록
```

실제 YOLO 실행, Input Validation, FastAPI Endpoint는 추가하지 않았다.

## 구현 전 Data Contract

```text
Model Detection 한 건:
  dict
  xyxy / class_id / class_name / confidence

Model Detection 여러 건:
  list[dict]

Adapter Input:
  model_results: list[dict]

Adapter Output:
  raw_results: list[dict]
  bbox / class_id / className / confidence

Filtering Input:
  raw_results: list[dict]
  threshold: float, 0.0 <= threshold <= 1.0

Filtering Output:
  filtered_raw_results: list[dict]

Final Output:
  list[DetectionResult]

Empty:
  [] → []
```

## Model Contract와 Service Contract 차이

| 구분 | Model Contract | Service Contract |
| --- | --- | --- |
| bbox field | `xyxy` | `bbox` |
| class name field | `class_name` | `className` |
| 유지되는 field | `class_id`, `confidence` | `class_id`, `confidence` |
| 책임 | 모델 라이브러리 결과 제공 | Service 내부 처리와 외부 DTO 생성 |

Adapter는 Model Contract를 Service Contract로 바꾸며 Detection을 제거하지 않는다. 따라서 Adapter 전후 Detection 수는 일반적으로 같다.

## 전체 Data Flow와 책임

```text
model_results: list[dict]
→ Adapter
raw_results: list[dict]
→ Filtering (confidence >= threshold)
filtered_raw_results: list[dict]
→ DetectionResult 변환
final_results: list[DetectionResult]
```

- Mock Model Output: Model 형식 제공
- Adapter: field 이름 변환과 Service raw Contract 생성
- Filtering: threshold 기준으로 Detection 선택
- DetectionResult: Pydantic DTO로 최종 결과 전달
- Pipeline: 위 세 책임을 정해진 순서로 연결

## 구현한 함수 구조

```text
adapt_model_results()
→ build_filtered_results()
→ build_final_results()
→ build_dto_detections()
```

Review 파일에서는 같은 Contract를 `build_adapt_detections()`, `build_filtered_detections()`, `build_dto_detections()`, `build_pipeline()`으로 다시 구성했다. 함수명은 달라도 Input, Output, 책임이 같으면 같은 Pipeline Contract를 만족한다.

## 구현 중 Contract 기준 오류 분석

1. 결과 list와 반복 중인 한 Detection dict를 같은 변수로 다루면 `dict`에 `append()`하거나 마지막 Detection만 남길 수 있다. 여러 결과를 담는 list와 한 건의 dict를 분리했다.
2. Filtering에서 목록 전체가 아니라 현재 반복 중인 raw detection의 `confidence`를 비교해야 한다. 목록의 첫 항목만 검사하면 모든 Detection이 같은 기준으로 통과하거나 제외된다.
3. DTO 변환에서 raw dict 전체 목록을 append하면 `list[list[dict]]`가 된다. 한 raw dict를 `DetectionResult` 한 건으로 만든 뒤 DTO 목록에 추가했다.
4. pytest test 함수에 Arrange 데이터용 파라미터를 넣으면 pytest가 fixture로 해석한다. 테스트 데이터는 함수 내부에서 만들었다.

## pytest

- Adapter Mapping: `xyxy → bbox`, `class_name → className`, Detection 수 유지 확인
- Pipeline Happy: Model Detection 3건에서 threshold `0.70` 후 `DetectionResult` 2건 확인
- Empty: `[]` 입력이 최종 `[]`으로 유지되는지 확인
- Boundary: `confidence == threshold`인 Detection이 포함되는지 확인

```text
python -m pytest week04/tests/test_d28.py
4 passed
```

## Review 재구현

다른 Mock Detection 3건과 threshold `0.70`으로 Pipeline을 다시 구성했다. Adapter 후 3건을 유지하고, `0.94`와 `0.70`은 통과하며 `0.52`는 제외되어 최종 `DetectionResult` 2건이 반환됐다.

## 공항·관제 도메인 연결

공항 제한구역 CCTV에서 Vision Model은 모델 전용 field를 반환할 수 있다. Adapter가 이를 Service raw Contract로 제한하면, 모델 field 이름이 바뀌어도 Adapter를 먼저 수정하면 된다. Filtering 정책, API DTO, Dashboard는 모델 전용 구조에 직접 의존하지 않는다.

이는 실제 공항 시스템 구현이 아니라 Adapter와 Service 책임 경계를 이해하기 위한 학습 예시다.

## Day 27보다 난이도가 높아진 부분

Day 27은 `detections → Filtering → results`를 다뤘다. Day 28은 Model Contract, Adapter Contract, Service raw Contract, DTO Contract까지 연결해야 했다. 문법보다 단계별 자료형과 함수 책임을 동시에 유지하는 점이 난이도 상승 지점이었다.

## 오늘 스스로 결정한 부분

- Adapter와 Filtering을 분리했다.
- Filtering 이후에만 `DetectionResult` DTO를 생성했다.
- Pipeline 함수를 추가해 호출자가 Adapter, Filtering, DTO 변환 순서를 직접 알 필요 없게 했다.
- Mapping, Happy, Empty, Boundary를 각각 분리된 pytest로 검증했다.

## 아직 부족한 부분

- 단수 `dict`와 복수 `list[dict]`를 변수 이름과 `append()` 위치에서 더 빠르게 구분할 필요가 있다.
- raw dict와 Pydantic DTO의 차이를 코드 작성 전에 먼저 명확히 적어야 한다.

## 다음 학습 포인트

Day 29에서는 기존 Pipeline에 Request Validation을 연결해 잘못된 threshold가 어느 경계에서 422로 처리되어야 하는지 다룬다.

## 면접용 설명

"모델 라이브러리의 Detection 형식을 API까지 직접 전달하지 않고 Adapter에서 Service raw Contract로 변환했습니다. Filtering은 `confidence >= threshold` 정책만 담당하고, Filtering 이후 기존 Pydantic `DetectionResult` DTO로 최종 응답 형식을 만들었습니다. 이 경계를 두면 모델 field 이름이 바뀌어도 Adapter 중심으로 수정 범위를 제한할 수 있습니다."
