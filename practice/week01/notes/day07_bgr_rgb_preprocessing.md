# Day 07 - BGR/RGB 변환과 모델 입력 전처리 계약

## 문제

OpenCV reads most color images as BGR arrays, while matplotlib and many AI models expect RGB arrays. Shape and dtype can remain identical even when the color-channel meaning is wrong.

## 구현 내용

- Added BGR to RGB and RGB to BGR conversion functions with None and 3-channel validation.
- Saved an RGB preview with matplotlib and saved a restored BGR image with OpenCV.
- Built prepare_model_input(image, width, height) to resize a BGR image and return an RGB image array.
- Built prepare_model_input_with_info() to return the processed image and metadata for original size, target size, color space, and dtype.
- Rebuilt the Day 07 functions in d7_review.py.
- Added seven pytest tests for pixel conversion, shape/dtype, round-trip restoration, failure cases, model input shape, and metadata.

## 데이터 흐름

    Path
    -> read_image_safe()
    -> BGR image array
    -> resize_for_model()
    -> RGB conversion
    -> model input image array and metadata

For display, the RGB image is passed to matplotlib. For OpenCV saving, the RGB image is converted back to BGR first.

## 핵심 규칙

    cv2.resize(image, (width, height))
    image.shape == (height, width, channels)
    BGR [10, 20, 30] -> RGB [30, 20, 10]

prepare_model_input(image, 640, 480) returns an RGB array with shape (480, 640, 3) when the input is a 3-channel uint8 BGR image.

## 테스트

    python -m pytest tests/test_d7_review.py -q
    7 passed

The tests cover a known BGR pixel, shape and dtype preservation, BGR to RGB to BGR round-trip restoration, None, grayscale input, requested model-input shape, and metadata values.

## 나의 역할과 AI 학습 보조

I wrote the Day 07 implementation, review implementation, and pytest assertions through small exercises. AI assistance was used for concept explanations, TODO structure, error analysis, and code review. I should be able to explain the input, return value, and validation rule of each function without reading the code.

## 한계

- This practice only handles 3-channel BGR input and returns RGB uint8 arrays.
- It does not include normalization, tensor conversion, batch dimensions, real model inference, ONNX, or GPU processing.
- The metadata records the BGR input contract; shape alone cannot prove that an arbitrary array is actually BGR.

## 다음 복습 질문

1. Why does cv2.resize(image, (640, 480)) produce shape (480, 640, 3)?
2. Why should an RGB image be converted back to BGR before cv2.imwrite()?
3. Why does save_image() not provide an image array to compare?
4. What is the difference between a Path, an image array, a metadata dict, and None?
5. Why does prepare_model_input_with_info() return two values?
