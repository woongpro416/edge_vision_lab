# Day 08 — OpenCV preprocessing contract review

## Goal

Day 07의 BGR/RGB와 preprocessing 흐름을 복습하고, 이미지 입력 계약을 직접 구현한다.

## Implemented

- `convert_bgr_to_rgb(image)`: `None`과 3채널 color image 여부를 검증한 뒤 BGR 배열을 RGB 배열로 변환한다.
- `prepare_model_input_simple(image, width, height)`: `None`과 양수 크기를 검증하고, resize 후 BGR→RGB 변환을 수행한다.
- `main()`: Day 06의 `read_image_safe()`로 원본 BGR 이미지를 읽고, `(640, 480)` target 크기의 RGB model input을 만든다.

## Data flow

```text
Path("week01/inputs/sample.jpg")
  → read_image_safe()
  → bgr_image: BGR np.ndarray
  → prepare_model_input_simple(bgr_image, 640, 480)
  → model_input: RGB np.ndarray, shape=(480, 640, 3), dtype=uint8
```

## Key concepts

- `Path`는 파일 위치이고, image array는 실제 픽셀을 담은 `np.ndarray`이다.
- BGR과 RGB는 shape와 dtype가 같아도 채널의 의미와 순서가 다르다.
- `cv2.resize(image, (width, height))`의 인자는 `(width, height)`지만, NumPy image shape는 `(height, width, channels)`이다.
- `width`와 `height`는 `prepare_model_input_simple()`가 직접 받는 값이므로, `cv2.resize()` 호출 전에 이 함수가 검증한다.

## Verification

- 정상 BGR 입력: RGB 변환 후 shape·dtype 유지 및 `[10, 20, 30] → [30, 20, 10]` 확인.
- `None`, grayscale image, `width=0`, `height=0`: 모두 `ValueError` 확인.
- `model_input`이 `None`이 아니고 shape가 `(480, 640, 3)`인지 assert로 확인.

## Scope kept for later

- metadata dict, tuple 반환과 unpacking
- 실제 inference, model output, postprocessing

## Ownership note

- 직접 구현: 입력 검증, BGR→RGB 변환, resize→RGB 전처리, `main()` 연결과 assert.
- 학습 보조: 함수 계약 정리, 코드 리뷰, 검증 항목 안내.

## One-sentence interview explanation

이미지를 읽은 뒤 target 크기로 resize하고 BGR을 RGB로 변환해 모델 입력을 준비했으며, 잘못된 이미지와 크기는 OpenCV 호출 전에 검증했습니다.
