# 학습 요약: Day 05 — 이미지 크기 확인과 resize helper 함수를 연습한다.

from pathlib import Path

import cv2


def read_image_safe(image_path: Path):
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError("파일이 없습니다")

    return image


def get_image_info(image):
    height, width, channels = image.shape
    dtype = str(image.dtype)

    info = {
        "height": height,
        "width": width,
        "channels": channels,
        "dtype": dtype,
    }

    return info


def resize_image(image, width: int, height: int):
    if width is None:
        raise ValueError("width is required")

    if width <= 0:
        raise ValueError("width는 0 이하일 수 없습니다.")

    if height is None:
        raise ValueError("height is required")

    if height <= 0:
        raise ValueError("height는 0 이하일 수 없습니다.")

    resized = cv2.resize(image, (width, height))

    return resized


def main():
    image_path = Path("inputs/sample.jpg")

    image = read_image_safe(image_path)
    info = get_image_info(image)

    print(info)

    resized = resize_image(image, 480, 240)
    resized_info = get_image_info(resized)

    print("original", info)
    print("resized", resized_info)


if __name__ == "__main__":
    main()
