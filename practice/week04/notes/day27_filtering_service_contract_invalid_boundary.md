# Day 27 — Filtering Service Contract와 Invalid Boundary

## 오늘 목표

Filtering Service의 정상 Contract를 먼저 정하고, 잘못된 입력을 모두 Service에 넣지 않고 Request Validation, Adapter, Service 중 어느 경계가 책임질지 판단한다.

## Day 26 복습

- Detection 한 건은 이름 있는 필드를 담는 `dict`다.
- 여러 Detection은 0건부터 여러 건까지 같은 방식으로 순회할 수 있는 `list[dict]`다.
- 검출 결과가 없을 때 `[]`는 정상적으로 실행된 Empty 결과이며, `None`과 구분한다.

## 요구사항과 구현 전 Contract

```text
Input:
  detections: list[dict]
  threshold: 이미 검증된 float

Output:
  filtered detections: list[dict]

Happy:
  confidence >= threshold인 Detection만 입력 순서를 유지해 반환한다.

Empty:
  [] -> []

Invalid responsibility:
  threshold가 문자열 또는 0.0~1.0 범위를 벗어남 -> Request Validation
  Detection에 confidence key가 없음 -> Adapter / 이전 Detection Contract
  detections가 [] -> Invalid가 아닌 정상 Empty
```

## Filtering Service가 책임지는 범위

Filtering Service는 validated Detection 목록과 threshold를 받아 confidence 정책으로 Detection을 선택한다. Request 값의 자료형이나 범위, Adapter가 만든 Detection dict의 필수 key를 검증하지 않는다.

```text
Client Request
-> Request Validation
-> Model / Adapter
-> Detection Data
-> Filtering Service
-> filtered detections
```

## Happy / Empty / Boundary pytest

- Happy: Detection 3건과 threshold `0.8`을 넣어 confidence `0.87`인 1건만 남는지 검증했다.
- Empty: 빈 목록을 넣었을 때 값과 자료형 계약에 맞는 `[]`가 반환되는지 검증했다.
- Boundary: `confidence == threshold == 0.8`일 때 결과가 정확히 1건 남는지 검증했다.

Boundary 결과는 `confidence >= threshold` Contract에서 등호를 포함한다는 것을 증명한다. 비교 연산자가 `>`로 바뀌어 같은 값의 Detection이 제외되는 버그를 막는다.

## 구현 중 오류와 Contract 분석

1. `pytest` 실행 시 `week04` module을 찾지 못했다. `practice` 폴더에서 `python -m pytest week04/tests/test_d27.py -q`로 실행해 현재 작업 경로를 Python module search path에 포함했다.
2. Empty test 함수의 매개변수에 `detections`를 넣어 pytest가 fixture로 해석했다. Arrange에서 직접 만드는 입력값은 test 함수 매개변수가 아니라 함수 내부에 둔다.
3. 반복문에서 전체 목록 `detections`를 결과에 추가해 `list[list[dict]]`가 되었다. 현재 반복 중인 단일 `detection` dict를 추가하도록 수정했다.

```text
detections: list[dict]
detection: dict
results: list[dict]
```

## Review 재구현

`d27_review.py`에서 기존 구현을 보지 않고 filtering 함수를 다시 작성했다. 모든 Detection을 순회하고, 조건을 통과한 단일 dict를 결과 목록에 추가한 뒤 반복문 밖에서 반환했다.

Review 파일의 Happy / Empty helper는 pytest가 아니라 Arrange와 Act를 담은 수동 실행용 예시다. 실제 pytest 검증은 `tests/test_d27.py`의 Happy, Empty, Boundary 3개 테스트가 담당한다.

## 테스트 결과

```text
python -m pytest week04/tests/test_d27.py -q
3 passed
```

## 공항·관제 도메인 연결

공항 제한구역 CCTV 학습 예시에서 Dashboard 사용자가 잘못된 threshold를 보낸다면 Request Validation에서 먼저 막는다. 반면 Model Adapter가 confidence 없는 Detection dict를 만들면 Adapter Contract 문제다. Filtering Service는 정상 Detection 목록에서 정책 기준을 통과한 결과를 Dashboard 또는 Alarm 단계에 전달하는 역할에 집중한다.

이는 실제 공항 운영 validation 정책이 아니라 책임 경계와 Data Flow를 학습하기 위한 예시다.

## 오늘 스스로 결정한 부분

- Empty `[]`를 Invalid와 구분했다.
- threshold 형식과 범위 오류를 Request Validation 책임으로 뒀다.
- confidence 누락을 Adapter / 이전 Detection Contract 문제로 분리했다.
- Service-level Invalid pytest를 억지로 추가하지 않고 Happy, Empty, Boundary Contract를 검증했다.

## 면접용 설명

"Filtering Service는 이미 검증된 `list[dict]` Detection과 threshold를 받아 `confidence >= threshold`인 Detection만 새 목록으로 반환하도록 설계했습니다. 빈 목록은 정상 Empty 결과로 `[]`를 유지했습니다. threshold의 타입과 범위는 Request Validation, confidence key 누락은 Adapter Contract 책임으로 분리했고, Happy, Empty, equality boundary를 pytest로 검증했습니다."

## 다음 학습 포인트

Day 28에서는 새 기술을 추가하지 않고 mock model output에서 raw results를 거쳐 DetectionResult Adapter를 요구사항만 보고 독립 재구현한다.
