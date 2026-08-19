# Day 25 — Detection Postprocessing과 Threshold 책임 이해

## 오늘 목표

YOLO가 반환하는 `Results` 이후의 postprocessing 흐름을 이해하고, Model threshold와 Service threshold의 책임을 구분한다. 또한 bbox 자료형 정책, IoU, NMS가 어느 단계에 속하는지 개념 수준에서 정리한다.

## Day 24 복습

Day 24의 핵심 흐름은 다음과 같다.

```text
Image
→ YOLO
→ Results / Boxes
→ Tensor를 Python 기본 자료형으로 변환
→ Adapter
→ raw_results
→ Service Filtering
→ DetectionResult
```

`Results`는 이미지 한 장에 대한 YOLO의 전체 결과이고, `Boxes`에는 detection별 `xyxy`, `cls`, `conf`가 담긴다. Adapter는 Tensor와 YOLO 객체 구조를 서비스가 다루기 쉬운 Python 자료형과 raw detection 계약으로 변환한다.

## 오늘의 핵심 질문

YOLO가 각 detection에 confidence를 이미 포함하는데도 Service에서 별도의 threshold를 두는 이유는, 두 threshold가 결정하는 책임과 시점이 다르기 때문이다.

## 전체 Data Flow

```text
Image
→ YOLO inference
→ Model confidence threshold와 NMS를 포함한 Model postprocessing
→ Results / Boxes
→ Adapter
→ raw_results
→ Service confidence filtering
→ DetectionResult
```

현재 사용한 Ultralytics YOLO에서 `Results`는 Model postprocessing 뒤에 만들어진다. Service Adapter는 NMS를 직접 수행하지 않는다.

## Model Threshold와 Service Threshold

| 구분 | 책임 |
| --- | --- |
| Model threshold | 낮은 confidence detection이 Model Result에 들어오는 것을 제한한다. |
| Adapter | Model Result를 서비스 raw_results 계약으로 변환한다. |
| Service threshold | 반환된 raw_results 중 서비스가 사용할 detection을 선택한다. |

Model 단계에서 제거된 detection은 `Results`와 `raw_results`에 존재하지 않는다. 따라서 Service threshold를 낮춰도 복구할 수 없다.

## Threshold 비교 실험

동일한 `sample.jpg`를 `yolo11n.pt`로 추론하고, Service threshold는 `0.60`으로 고정했다.

| Model threshold | Model detections | raw_results | Service detections |
| ---: | ---: | ---: | ---: |
| 0.25 | 8 | 8 | 4 |
| 0.70 | 2 | 2 | 2 |

Model threshold를 `0.25`에서 `0.70`으로 높이자 `Boxes` 수가 8건에서 2건으로 줄었다. 두 Case 모두 Adapter 전후 개수는 같았다. Case A에서는 Service filtering이 4건을 제거했지만, Case B는 Model 단계에서 이미 2건만 전달했으므로 Service threshold가 더 낮아도 결과를 늘릴 수 없었다.

## bbox 좌표 정책

YOLO bbox는 float 좌표로 반환될 수 있다. 현재 Adapter와 `DetectionResult` 계약은 `list[int]`를 사용하므로 `int()`로 변환한다.

```text
[10.8, 20.2, 100.9, 200.7]
→ [10, 20, 100, 200]
```

정수 pixel 좌표는 화면에 box를 그리기 편하지만 소수점 위치 정보는 사라진다. 화면 표시만 필요한지, crop·tracking·정밀 geometry 계산에도 재사용할지에 따라 API 계약을 결정해야 한다.

## IoU와 NMS

IoU는 두 bbox가 얼마나 겹치는지 나타내는 값이다. 0에 가까우면 거의 겹치지 않고, 1에 가까우면 거의 같은 위치를 가리킨다.

NMS는 겹침이 큰 중복 bbox 중 confidence가 높은 box를 우선 남겨 같은 객체가 여러 번 집계되는 문제를 줄이는 postprocessing 개념이다. NMS는 중복 bbox를 다루고, Service confidence filtering은 각 detection을 서비스 정책의 confidence 기준으로 선택하므로 서로 다른 기능이다.

## 구현한 코드

- `d25.py`: 동일 이미지에 두 Model threshold를 적용하고, Model Result·Adapter·Service filtering 단계별 detection 수를 출력한다.
- `d25_review.py`: Model postprocessing을 이미 통과한 학습용 후보 3건을 Adapter와 Service filtering으로 다시 추적한다. 실행 결과는 `3 | 3 | 2`다.

## 테스트 결과

`test_d25.py`는 confidence `0.91`, `0.72`, `0.55`의 가짜 raw_results에 Service threshold `0.7`을 적용한다. `0.91`과 `0.72`만 남고 `0.55`가 제외되는지 검증했다.

```text
Week 04 tests: 9 passed
```

## 공항·관제 도메인 연결

학습용 공항 제한구역 CCTV 흐름에서는 `Camera → Vision Model → Adapter → Service Filtering → Dashboard / Alarm` 구조를 생각할 수 있다. Model threshold를 과도하게 높이면 낮은 confidence 객체는 Service까지 도달하지 못한다. 중복 bbox가 남으면 detectionCount, Alarm, Tracking, 통계가 한 객체를 여러 개로 취급할 수 있으므로 NMS 개념이 중요하다. 이는 실제 공항 운영 threshold를 의미하지 않는 학습용 예시다.

## 오늘 이해가 높아진 부분

- Model threshold와 Service threshold의 적용 시점과 책임 차이
- Adapter가 결과 개수를 임의로 줄이지 않는다는 점
- Model에서 제거된 detection은 Service에서 복구할 수 없다는 Data Flow 관점
- IoU, NMS, Service filtering의 역할 차이
- bbox 자료형이 Service Data Contract와 연결된다는 점

## 현재 구현의 한계

- 실험은 이미지 한 장과 두 Model threshold만 비교했다.
- 현재 bbox 계약은 int 좌표만 허용하므로 float 정밀도를 보존하지 않는다.
- Model threshold와 Service threshold 값은 학습용 비교 값이며 실제 운영 정책이 아니다.

## 다음 학습 포인트

Day 26은 새로운 주제를 자동으로 추가하지 않는다. Model threshold, Service threshold, Adapter, bbox 정책, IoU, NMS를 코드 없이 설명할 수 있는지 먼저 확인한 뒤 다음 범위를 결정한다.

## 면접용 설명

YOLO inference 결과는 Model confidence threshold와 NMS를 거친 뒤 `Results`로 반환된다. Adapter는 YOLO의 Tensor와 객체 구조를 서비스 raw detection 계약으로 변환하고, Service는 별도의 confidence threshold로 Dashboard나 Alarm에 사용할 detection을 선택한다. Model 단계에서 제외된 결과는 뒤 단계에서 복구할 수 없으며, NMS는 중복 bbox를 정리하는 기능이라 Service confidence filtering과 목적이 다르다.
