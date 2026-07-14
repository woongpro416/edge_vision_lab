# Day 06 - OpenCV 이미지 처리 함수화와 중앙 Crop

## 오늘 목표

Day 05에서 작성한 OpenCV 코드를 작은 함수로 분리하고, 중앙 crop과 실패 케이스를 추가했다.

```text
Path -> read_image_safe() -> image array
image array -> get_image_info() -> metadata dict
image array -> resize_for_model() / crop_center() -> processed image array
processed image array -> save_image() -> output file
```

## 작성한 함수

- `read_image_safe(image_path: Path)`: `cv2.imread(str(image_path))`로 이미지를 읽고, 실패 시 `FileNotFoundError`를 발생시킨다.
- `get_image_info(image)`: `height`, `width`, `channels`, `dtype`을 dict로 반환한다.
- `resize_for_model(image, width, height)`: 0 이하 크기를 거부하고, 모델 입력 크기로 resize한다.
- `crop_center(image, crop_width, crop_height)`: 이미지 중앙을 기준으로 지정한 크기만큼 crop한다.
- `save_image(image, output_path: Path)`: 부모 폴더를 생성하고 이미지를 저장한 뒤, 저장 실패를 확인한다.

## 핵심 규칙

```text
image.shape = (height, width, channels)
cv2.resize(image, (width, height))
crop = image[y1:y2, x1:x2]
```

- NumPy 이미지 배열의 첫 번째 축은 세로 행(row)이므로 `y`가 먼저 온다.
- 두 번째 축은 가로 열(column)이므로 `x`가 나중에 온다.
- `cv2.imread()`는 읽기에 실패하면 `None`을 반환한다.
- `cv2.imwrite()`는 저장 성공 여부를 `True` 또는 `False`로 반환한다.

## 중앙 Crop 좌표

원본이 `width=640`, `height=480`이고 crop 크기가 `320x240`이면 다음과 같이 계산한다.

```python
x1 = (width - crop_width) // 2   # 160
y1 = (height - crop_height) // 2 # 120
x2 = x1 + crop_width             # 480
y2 = y1 + crop_height            # 360
```

```python
cropped = image[y1:y2, x1:x2]
```

슬라이싱 끝점은 포함하지 않지만, 결과 길이는 `x2 - x1`, `y2 - y1`이므로 요청한 crop 크기와 같다.

## 입력 검증과 실패 케이스

- 없는 이미지 경로: `FileNotFoundError`
- resize width 또는 height가 0 이하: `ValueError`
- crop width 또는 height가 0 이하: `ValueError`
- crop 크기가 원본보다 큼: `ValueError`
- 이미지 저장 실패: `ValueError`

`0`이나 음수 crop 크기를 먼저 검증하지 않으면, 빈 배열 또는 의도하지 않은 NumPy slicing 결과가 다음 단계로 넘어갈 수 있다.

## 실습 결과물

- `d6.py`: Day 06 구현
- `d6_review.py`: 함수 전체를 다시 작성한 복습 구현
- `outputs/resized_for_model.jpg`: 640x480 resize 결과
- `outputs/cropped_sample.jpg`: 320x240 중앙 crop 결과
- `outputs/d6_review_resized.jpg`: 복습 resize 결과
- `outputs/d6_review_cropped.jpg`: 복습 중앙 crop 결과

## 테스트

`np.zeros((480, 640, 3), dtype=np.uint8)`로 파일에 의존하지 않는 검은색 테스트 이미지를 만들었다.

```text
python -m pytest tests/test_d6.py -q
8 passed

python -m pytest tests/test_d6_review.py -q
8 passed
```

검증한 내용:

- 존재하지 않는 경로에서 `FileNotFoundError` 발생
- image info dict의 shape/dtype 값
- resize 결과 shape
- crop 결과 shape
- 원본 초과, 0, 음수 crop에서 `ValueError` 발생
- 저장 후 output 파일 존재 여부

주의: crop 결과 shape 테스트만으로는 crop 위치가 중앙인지 증명할 수 없다. shape는 같지만 좌상단 영역을 crop하는 구현도 통과할 수 있으므로, 필요하면 위치 정보를 가진 테스트 이미지로 좌표 자체를 검증해야 한다.

## AI Vision / 공항 도메인 연결

공항 CCTV, 차량 카메라, 수하물 X-ray 이미지가 AI inference에 들어가기 전에도 같은 전처리 흐름이 필요하다.

```text
입력 경로 검증 -> 이미지 읽기 -> shape/dtype 확인 -> resize 또는 crop -> 저장/다음 단계 전달
```

중앙 crop은 관심 영역이 항상 중앙이라는 근거가 있을 때만 사용한다. CCTV의 차량이나 활주로 객체, X-ray의 수하물은 화면 가장자리에 있을 수 있으므로 근거 없이 중앙 crop을 적용하면 중요한 정보를 잃을 수 있다.

현재 구현은 일반적인 3채널 BGR 이미지 입력을 전제로 한다. 실제 모델이 RGB를 요구할 때만 BGR/RGB 변환을 전처리 계약에 추가한다.

## 오늘 복습에서 확인한 점

- `Path`는 이미지 자체가 아니라 파일 위치를 나타낸다.
- `image`는 OpenCV가 읽은 NumPy array다.
- `save_image()`는 저장 작업을 수행하고 `None`을 반환한다. 저장 검증은 함수 내부의 `imwrite()` 반환값과 외부의 `Path.exists()`로 한다.
- 학습 코드의 `assert`는 결과 확인에 적절하다. 서비스에서는 명시적 예외 처리와 로그로 대체한다.

## 추천 커밋 메시지

```text
feat: add Day 06 OpenCV preprocessing utilities and crop tests
```

커밋 본문을 쓴다면:

```text
- Add safe image loading, metadata extraction, resize, center crop, and save utilities
- Validate missing image paths and invalid resize/crop dimensions
- Add Day 06 review implementation and pytest coverage for success and failure cases
- Document image preprocessing flow for AI vision inference inputs
```

## 복습 질문

```text
1. cv2.imread()와 cv2.imwrite()는 실패를 각각 어떤 값으로 알리는가?
2. image.shape와 cv2.resize()의 width/height 순서는 어떻게 다른가?
3. 중앙 crop에서 x1, y1, x2, y2는 어떤 순서로 계산하는가?
4. crop slicing에서 y가 x보다 먼저 오는 이유는 무엇인가?
5. 0 또는 음수 crop 크기를 검증해야 하는 이유는 무엇인가?
6. crop 결과 shape 테스트만으로 중앙 crop을 완전히 증명할 수 없는 이유는 무엇인가?
7. 공항 CCTV에 중앙 crop을 적용하기 전에 어떤 도메인 가정을 확인해야 하는가?
```
