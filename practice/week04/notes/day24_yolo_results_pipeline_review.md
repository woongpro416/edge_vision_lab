# Day 24 — YOLO Results Pipeline 이해도 강화

## 오늘 목표

Day 23에서 실제 YOLO를 연결하며 확인한 `Results → Boxes → Tensor → Adapter → raw_results → Filtering → DetectionResult` 흐름을 다시 구현하고, 각 단계의 책임을 구분한다.

## Day 23에서 어려웠던 부분

`Results`, `Boxes`, Tensor, `.tolist()`, `.item()`, `zip()`처럼 YOLO와 PyTorch가 제공하는 객체와 메서드가 한꺼번에 나타났다. 특히 모델 데이터와 서비스 데이터의 경계, 그리고 `zip()`이 같은 detection의 값을 묶는 이유를 복습했다.

## 전체 Data Flow

```text
Image
→ YOLO model
→ Results
→ Boxes (xyxy / cls / conf Tensor)
→ Python Data (list / int / float / str)
→ YOLO Adapter
→ raw_results
→ convert_detections() filtering
→ DetectionResult
```

## Results / Boxes / Tensor 정리

- `Results`: 이미지 한 장에 대해 YOLO가 반환한 전체 결과 객체다.
- `Boxes`: 탐지된 여러 객체의 위치, class id, confidence가 들어 있는 객체다.
- `xyxy`: bounding box의 좌상단과 우하단 좌표 `[x1, y1, x2, y2]`다.
- `cls`: 모델이 부여한 객체 종류 번호다. `result.names[class_id]`로 이름을 찾는다.
- `conf`: 탐지 한 건에 대한 모델 confidence다. 모델 전체 정확도 지표와는 다르다.
- Tensor: 모델 라이브러리가 반환하는 값 형식이다. 서비스 dict에 바로 의존하지 않도록 Adapter에서 Python 기본 자료형으로 변환한다.

## `.tolist()` / `.item()` 이해

```text
xyxy Tensor 여러 값 → .tolist() → Python list
cls / conf Tensor 한 값 → .item() → Python scalar
```

실제 Adapter에서는 bbox 좌표를 `.tolist()`으로 꺼낸 뒤 `int()`로 pixel 좌표 `list[int]`로 통일했다. class id는 `int`, confidence는 `float`, class name은 `str`로 만들었다.

## `zip()`의 역할

`zip(boxes.xyxy, boxes.cls, boxes.conf)`는 같은 index의 위치, class id, confidence를 한 detection으로 묶어 순회한다. 자료형 변환이나 key 이름 변경은 `zip()`의 역할이 아니다.

## 코드 분석과 직접 재구현

`d24.py`에서 가짜 모델 값으로 다음 흐름을 직접 구현했다.

```text
tuple 좌표 / float class id / float confidence / names dict
→ list / int / float / str
→ model_detection
→ build_raw_detection()
→ raw_detection
```

`d24_review.py`에서는 `build_raw_detections_from_yolo_result(result)`를 다시 구현했다. 함수는 `result.boxes`를 읽고, 세 Tensor field를 `zip()`으로 순회하며, `build_raw_detection()`을 재사용해 `raw_results`를 반환한다.

## Adapter와 Filtering 책임 분리

```text
build_raw_detections_from_yolo_result()
→ YOLO Result에서 값 추출, Python 자료형 변환, raw_results 연결

build_raw_detection()
→ model_detection의 xyxy / class_name 등을 서비스 raw_detection key로 통일

convert_detections()
→ confidence threshold filtering 후 DetectionResult 생성
```

역할을 분리하면 YOLO 모델 또는 라이브러리가 바뀌었을 때 Adapter 경계를 우선 수정할 수 있다. 서비스 filtering 정책과 DTO는 모델 세부 구조에 덜 영향을 받는다.

## 한 Detection의 Data Flow

실제 이미지에서 첫 번째 detection을 따라갔다.

```text
xyxy Tensor: [0.30322, 87.957, 142.90, 480.0]
→ bbox: [0, 87, 142, 480]

cls Tensor: 0.0
→ class_id: 0
→ class_name: "person"

conf Tensor: 약 0.7127
→ threshold 0.6 통과
→ DetectionResult 포함
```

## 테스트 결과

`test_d24.py`에 가짜 YOLO Result를 사용한 테스트 두 개를 작성했다.

```text
1. detection 2건이 예상한 raw_results 2건으로 변환되는지 확인
2. detection 0건이 빈 list []로 반환되는지 확인
```

```text
2 passed
```

## Edge Case

YOLO가 객체를 0개 찾는 것은 정상 결과다. 이 경우 `for` loop는 0회 실행되고 `raw_results`는 `[]`로 반환된다. 파일을 읽지 못하거나 모델 호출 자체가 실패한 경우와 구분해야 한다.

## 실제 YOLO 결과 확인

동일한 모델과 이미지를 다시 실행했다.

```text
results: list, 길이 1
result: Results
result.boxes: Boxes, 길이 8
boxes.xyxy: torch.Tensor
raw_results: 8건
threshold 0.6 뒤 DetectionResult: 4건
```

YOLO가 찾은 8건을 Adapter가 제거한 것이 아니라, `convert_detections()`가 confidence 기준으로 4건을 제거했다.

## 공항·관제 도메인 연결

공항 제한구역 CCTV에서는 `Camera Image → Vision Model → Results → Adapter → Detection Data → Filtering → API/Dashboard` 흐름으로 연결될 수 있다. Dashboard가 특정 YOLO 객체를 직접 사용하지 않고 `bbox`, `class_id`, `className`, `confidence` 같은 공통 서비스 데이터만 사용하도록 경계를 둔다.

## 오늘 이해가 높아진 부분

- `Results`와 `Boxes`의 포함 관계
- 모델 Tensor를 Python 기본 자료형으로 꺼내는 이유
- `model_detection`과 서비스 `raw_detection`의 key 계약 차이
- Adapter는 형식 변환, Filtering은 서비스 정책이라는 책임 분리
- detection 0건이 정상 응답일 수 있다는 점

## 아직 헷갈리는 부분

- `.tolist()`은 여러 Tensor 값을 list로 꺼내는 기능이고, `.item()`은 한 scalar를 꺼내는 기능이라는 차이를 더 짧게 설명하는 연습이 필요하다.
- `zip()`은 변환이나 mapping이 아니라 같은 detection의 여러 field를 묶는 기능이라는 점을 작은 list 예제로 한 번 더 복습할 필요가 있다.

## 현재 한계

- bbox 좌표를 `int()`로 바꾸면 소수점이 버려진다. 좌표 반올림 정책은 서비스 요구사항에 따라 별도 결정해야 한다.
- 현재 Adapter는 Ultralytics YOLO의 `result.boxes.xyxy`, `cls`, `conf`, `names` 구조를 가정한다.

## 다음 학습 포인트

Day 25를 시작하기 전 `.tolist()` / `.item()`과 `zip()`을 5분 동안 작은 예제로 복습한다. 이후 주제는 Day 24 Gate 결과를 기준으로 결정하며, NMS·IoU·FastAPI 등 새 개념으로 자동 확장하지 않는다.

## 면접용 설명

YOLO는 이미지에서 찾은 객체를 `Results`와 `Boxes`에 Tensor 형태로 반환한다. Adapter는 위치, class id, confidence를 Python 기본 자료형과 서비스 raw detection 형식으로 변환한다. 이후 `convert_detections()`가 서비스 confidence threshold를 적용해 최종 `DetectionResult`를 만든다. 모델 라이브러리가 바뀌면 우선 Adapter 경계를 수정해 서비스 DTO와 filtering 정책의 변경 범위를 줄일 수 있다.
