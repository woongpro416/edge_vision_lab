import cv2
from pathlib import Path

from week01.d6 import read_image_safe


def convert_bgr_to_rgb(image):
    # TODO: image가 None이면 ValueError
    if image is None:
        raise ValueError("image 가 존재하지 않습니다.")

    # TODO: image가 3채널 color image가 아니면 ValueError
    if image.ndim != 3 or image.shape[2] !=3:
        raise ValueError("image가 color image가 아닙니다.")

    # TODO: cv2.cvtColor()로 BGR을 RGB로 변환해 반환
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return rgb_image

def prepare_model_input_simple(image, width: int, height: int):
    # TODO: image가 None이면 ValueError
    if image is None:
        raise ValueError("image가 존재하지 않습니다.")

    # TODO: width 또는 height가 0 이하이면 ValueError
    if width <= 0 or height <= 0:
        raise ValueError("width 와 height는 0 이하일 수 없습니다.")

    # TODO: cv2.resize()로 (width, height) 크기의 BGR 배열 생성
    resized = cv2.resize(image, (width, height))

    # TODO: 위 BGR 배열을 convert_bgr_to_rgb()에 전달하고 반환
    rgb_image = convert_bgr_to_rgb(resized)
    return rgb_image

def main():
    # TODO: Path("week01/inputs/sample.jpg") 생성
    image_path = Path("week01/inputs/sample.jpg")

    # TODO: read_image_safe()로 원본 BGR image 읽기
    bgr_image = read_image_safe(image_path)

    # TODO: prepare_model_input_simple(image, 640, 480) 실행
    model_input = prepare_model_input_simple(bgr_image, 640, 480)

    print("bgr_image type:", type(bgr_image))
    print("bgr_image shape:", bgr_image.shape)
    print("bgr_image dtpe:", bgr_image.dtype)
    print("model_input type:", type(model_input))
    print("model_input shape:", model_input.shape)
    print("model_input dtype:", model_input.dtype)

    assert model_input is not None
    assert model_input.shape == (480, 640, 3)

if __name__ == "__main__":
    main()