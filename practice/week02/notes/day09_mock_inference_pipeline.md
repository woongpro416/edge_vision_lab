# Day 09 — Mock inference, postprocessing, and response

## Goal

Day 08에서 만든 RGB `model_input` 뒤에 mock inference와 postprocessing을 연결했다. 실제 YOLO 모델, FastAPI, Pydantic은 사용하지 않고 함수의 입력·반환 계약을 먼저 확인했다.

## Data flow

```text
Path("week01/inputs/sample.jpg")
  → read_image_safe()
  → bgr_image: numpy.ndarray (BGR)
  → prepare_model_input_simple()
  → model_input: numpy.ndarray (RGB, shape=(480, 640, 3))
  → run_mock_inference()
  → raw_results: list[dict]
  → count_detections_by_class()
  → class_counts: dict[str, int]
  → build_inference_response()
  → response: dict
```

## Implemented

- `run_mock_inference(model_input)`
  - `None`, 3차원이 아닌 배열, 3채널이 아닌 배열을 `ValueError`로 검증한다.
  - 실제 이미지 분석이나 AI 모델 호출 없이 고정된 `list[dict]`를 반환한다.
- `count_detections_by_class(raw_results)`
  - `className`을 key, 감지 개수를 value로 사용하는 `class_counts` dict를 만든다.
  - 예: `{"vehicle": 2, "person": 1}`
- `build_inference_response(raw_results)`
  - raw 결과를 검증하고 status, 전체 감지 수, class별 감지 수, 원본 결과를 포함한 response를 만든다.

```python
{
    "status": "OK",
    "detectionCount": 2,
    "classCounts": {"vehicle": 1, "person": 1},
    "results": raw_results,
}
```

## Key concepts

- `raw_results`는 모델이 반환한 가공 전 감지 결과인 `list[dict]`다.
- `detectionCount`는 전체 detection 수를 나타내는 `int`다.
- `classCounts`는 className별 detection 수를 나타내는 `dict[str, int]`다.
- `None`은 유효한 입력이 없는 오류 상태이고, `[]`는 감지가 0개인 정상 결과다.
- `model_input.ndim`은 배열의 차원 수이고, `model_input.shape[2]`는 3차원 이미지의 channel 수다.
- 실제 모델을 연결할 때는 `run_mock_inference()`를 교체하되, 입력 `numpy.ndarray`와 반환 `list[dict]` 계약을 유지한다.

## Testing

`week02/tests/test_d9.py`에서 다음 4개를 확인했다.

1. 빈 `raw_results`는 `detectionCount=0`, `classCounts={}`인 정상 response를 만든다.
2. `build_inference_response(None)`은 `ValueError`를 발생시킨다.
3. 반복된 className은 class별 count에 누적된다.
4. 빈 detection list를 집계하면 빈 dict를 반환한다.

```powershell
cd practice
python -m week02.d9
python -m pytest week02/tests/test_d9.py -q
```

## Import lesson

실제 코드인 `d9.py`가 test 파일을 import하면 circular import가 발생한다. 의존 방향은 항상 아래처럼 유지한다.

```text
test_d9.py → d9.py
```

## Scope kept for later

- 실제 YOLO/ONNX 모델 호출
- bbox, class_id, confidence threshold
- detection 내부 필드의 상세 validation
- Pydantic response DTO와 FastAPI endpoint

## Ownership note

- 직접 구현: mock inference 검증과 반환 구조, class별 집계, response 확장, `main()` 연결, assert, pytest 4개, review 파일 재구현.
- 학습 보조: 데이터 계약 설명, TODO 설계, 오류 원인 설명, 코드 리뷰.

## One-sentence interview explanation

전처리된 RGB 이미지 배열을 mock inference에 전달하고, 감지 결과를 class별로 집계한 뒤 안정적인 response 구조로 변환했으며, 빈 결과와 잘못된 입력을 pytest로 검증했습니다.
