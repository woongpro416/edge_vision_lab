# Day 05 - OpenCV 이미지 읽기와 image shape 기초

## 배운 내용

- `cv2.imread(str(image_path))`는 이미지 파일을 읽어서 NumPy array로 만든다.
- 이미지 경로가 틀리거나 파일을 읽을 수 없으면 `cv2.imread()`는 `None`을 반환한다.
- 컬러 이미지의 `image.shape`는 보통 `(height, width, channels)` 구조다.
- `image.dtype`은 픽셀 값의 데이터 타입을 보여준다. 오늘 샘플 이미지는 `uint8`이었다.
- `cv2.resize(image, (width, height))`는 이미지 크기를 변경한다.
- `cv2.imwrite(str(output_path), image)`는 이미지 array를 파일로 저장하고 `True` 또는 `False`를 반환한다.
- `Path.exists()`와 `Path.resolve()`는 OpenCV에 넘기기 전 파일 경로를 디버깅할 때 유용하다.

## Day 04 NumPy와 연결

Day 04에서는 NumPy array의 `shape`를 배웠다.

Day 05에서는 OpenCV로 읽은 이미지도 NumPy array라는 것을 확인했다.

```text
<class 'numpy.ndarray'>
(480, 640, 3)
uint8
```

해석:

```text
height = 480
width = 640
channels = 3
dtype = uint8
```

즉, 이미지 파일은 OpenCV로 읽으면 숫자로 이루어진 NumPy array가 된다.

## 실습 파일

- `d5.py`: 이미지를 읽고 `type`, `shape`, `dtype`을 출력한 뒤 640x480으로 resize해서 저장했다.
- `d5_mini.py`: 고정 좌표 `(50, 50)`부터 `(200, 200)`까지 초록색 사각형을 그리고 저장했다.
- `d5_center_box.py`: `image.shape`에서 이미지 중심 좌표를 계산하고, 중앙에 빨간색 사각형을 그려 저장했다.
- `d5_image_utils.py`: 이미지 읽기, 정보 추출, resize를 재사용 가능한 함수로 분리했다.

## 핵심 구분

```text
image.shape
= (height, width, channels)

cv2.resize(image, (640, 480))
= (width, height)

cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
= 좌표는 (x, y)
```

- `height`는 세로 방향 크기다.
- `width`는 가로 방향 크기다.
- `x`는 왼쪽에서 오른쪽으로 움직이는 가로 좌표다.
- `y`는 위에서 아래로 움직이는 세로 좌표다.
- OpenCV 색상 순서는 RGB가 아니라 BGR이다.
- 초록색은 `(0, 255, 0)`이다.
- 빨간색은 `(0, 0, 255)`이다.

## 경로 디버깅

`cv2.imread()`가 `None`을 반환했을 때 원인은 코드 로직이 아니라 이미지 경로였다.

확인에 사용한 코드:

```python
print(image_path.resolve())
print(image_path.exists())
```

`smaple.jpg`와 `sample.jpg` 파일명 차이 때문에 경로 확인이 실패했다. 파일명을 `sample.jpg`로 맞추고 `Path("inputs/sample.jpg")`를 사용하니 이미지가 정상적으로 읽혔다.

## 오늘 실수에서 배운 점

- `image_path`는 경로 객체이고, `image`는 OpenCV가 읽은 NumPy array다.
- `shape`, `dtype`, `resize`, `rectangle`은 경로가 아니라 이미지 array에 적용해야 한다.
- `cv2.imwrite()`는 저장 경로를 첫 번째 인자로, 저장할 이미지 array를 두 번째 인자로 받는다.
- `outputs` 폴더는 저장하기 전에 먼저 만들어야 한다.
- 상대 경로는 현재 터미널 실행 위치를 기준으로 해석된다.

## 실무형 고도화

기본 실습에서 끝내지 않고 이미지 처리 흐름을 함수로 분리했다.

```text
Path -> read_image_safe() -> image array
image array -> get_image_info() -> metadata dict
image array -> resize_image() -> resized image array
```

작성한 함수:

- `read_image_safe(image_path)`: 파일 존재 여부를 확인하고, `cv2.imread()` 실패 시 명확한 예외를 발생시킨다.
- `get_image_info(image)`: `height`, `width`, `channels`, `dtype`을 dict 형태로 정리한다.
- `resize_image(image, width, height)`: `width`, `height`를 검증한 뒤 `cv2.resize()`를 호출한다.

확인한 출력:

```text
original {'height': 480, 'width': 640, 'channels': 3, 'dtype': 'uint8'}
resized {'height': 240, 'width': 480, 'channels': 3, 'dtype': 'uint8'}
```

중요한 입력 검증:

```text
None = 값이 아예 없음
0 = 값은 있지만 이미지 크기로 부적절함
음수 = 값은 있지만 이미지 크기로 부적절함
```

따라서 `width <= 0 or None`처럼 한 줄로 처리하지 않고, 아래 순서로 나눠서 검증한다.

```text
1. width is None 또는 height is None 확인
2. width <= 0 또는 height <= 0 확인
3. cv2.resize() 실행
```

`None <= 0`은 비교할 수 없기 때문에 `TypeError`가 난다. 그래서 missing value 검사는 숫자 비교보다 먼저 해야 한다.

## AI Vision 연결

공항 CCTV, 차량 카메라, X-ray 입력 이미지 전처리도 기본 흐름은 같다.

```text
이미지 읽기 -> shape/dtype 확인 -> 크기 변경 또는 표시용 가공 -> 저장 또는 다음 단계 전달
```

오늘은 YOLO, bbox 후처리, FastAPI 업로드, 실시간 카메라, 고급 필터로 넘어가지 않았다.

## 추천 커밋 메시지

```text
feat: add Day 05 OpenCV image utility practice
```

커밋 본문을 쓴다면:

```text
- Document cv2.imread, image.shape, image.dtype, resize, and imwrite basics
- Connect OpenCV image arrays to Day 04 NumPy shape practice
- Summarize pathlib path debugging and str(path) usage with OpenCV
- Add notes for fixed and center rectangle drawing practice
- Add reusable image read, info, and resize utility practice
- Document width/height validation and None vs invalid value handling
```

## 복습 질문

```text
1. cv2.imread()는 경로가 틀리면 무엇을 반환하는가?
2. 컬러 이미지에서 image.shape = (480, 640, 3)은 각각 무엇을 뜻하는가?
3. image.shape와 cv2.resize()의 width/height 순서는 어떻게 다른가?
4. OpenCV 함수에 Path를 넘길 때 왜 str(path)를 사용하는가?
5. 이미지 좌표에서 (x, y)는 각각 어느 방향을 뜻하는가?
6. `None`, `0`, 음수는 resize 입력 검증에서 어떻게 다르게 처리해야 하는가?
7. 왜 `width <= 0 or None`은 `width is None` 검사가 아닌가?
```
