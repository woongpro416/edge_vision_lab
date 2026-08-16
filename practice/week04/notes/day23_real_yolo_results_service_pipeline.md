# Day 23 — 실제 YOLO Results와 Service Pipeline 연결

## 목표와 실제 결과

`yolo11n.pt`로 이미지 1장을 추론해 8건을 탐지하고 `raw_results`로 변환했다. `model(image)`은 `list`, 첫 결과는 `Results`, `result.boxes`는 `Boxes`였다.

## Data Flow

```text
Image → YOLO → Results → Adapter → raw_results → Filtering → DetectionResult
```

## 자료형 경계와 구현

`xyxy`·`cls`·`conf` Tensor와 `result.names`를 `list[int]`·`int`·`float`·`str`로 바꿨다. `build_raw_detection()`을 재사용했고 filtering은 `convert_detections()`가 담당한다. threshold 0.6에서 4건이 남았다.

## 테스트와 Edge Case

가짜 Results로 Adapter 계약과 pipeline 연결을 검증해 pytest 2개가 통과했다. 0건 detection은 두 결과가 모두 `[]`이며, 외부 구조 문제는 Adapter에서 확인한다.

## 공항·관제 도메인 연결

CCTV 모델 결과를 공통 Detection Data로 바꾸면 모델 변경은 Adapter와 가짜 외부 결과 테스트에 집중된다.

## 현재 한계와 다음

`int()` bbox 변환은 소수 좌표를 버리고 Adapter는 `boxes` 구조를 가정한다. Day 24는 이동 Gate 뒤 결정한다.

## 면접용 설명

YOLO Tensor를 서비스 계약으로 변환하고 기존 filtering·DTO pipeline을 재사용해 모델 교체 영향을 경계에 집중시켰다.
