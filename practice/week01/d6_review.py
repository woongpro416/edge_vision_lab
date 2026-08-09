# 학습 요약: Day 06 복습 — 이미지 유틸리티와 crop validation을 점검한다.

from pathlib import Path

import cv2


def read_image_safe(image_path: Path):

    image = cv2.imread(str(image_path))

    if image is None:
        raise FileNotFoundError(f"이미지가 존재하지 않습니다.{image_path}")

    return image



def get_image_info(image):

    height, width, channels = image.shape

    image_dtype = str(image.dtype)

    expected_dict = {
        "height": height,
        "width": width,
        "channels": channels,
        "dtype": image_dtype,
    }
    return expected_dict

def resize_for_model(image, width: int, height: int):

    if width <= 0 or height <= 0:
        raise ValueError("width 또는 height는 0 또는 음수일 수 없습니다.")

    resized = cv2.resize(image, (width,height))

    return resized


def crop_center(image, crop_width: int, crop_height: int):

    height, width = image.shape[:2]

    if crop_width <= 0 or crop_height <= 0:
        raise ValueError("crop_width, crop_height는 0또는 음수일 수 없습니다.")

    if crop_width > width or crop_height > height:
        raise ValueError("crop 이미지는 원본보다 클 수 없습니다.")


    x1 = (width - crop_width) // 2
    y1 = (height - crop_height) // 2
    x2 = x1 + crop_width
    y2 = y1 + crop_height



    cropped = image[y1:y2, x1:x2]

    return cropped


def save_image(image, output_path: Path) -> None:

    output_path.parent.mkdir(parents=True, exist_ok=True)

    saved = cv2.imwrite(str(output_path), image)

    if not saved:
        raise ValueError("이미지가 저장되지 않았습니다.")


def main():

    image_path = Path("inputs/sample.jpg")


    resized_path = Path("outputs/d6_review_resized.jpg")
    cropped_path = Path("outputs/d6_review_cropped.jpg")


    image = read_image_safe(image_path)


    print(get_image_info(image))


    resized = resize_for_model(image, 640, 480)


    save_image(resized, resized_path)


    cropped = crop_center(image, 320, 240)


    save_image(cropped, cropped_path)


    assert resized_path.exists()
    assert cropped_path.exists()


if __name__ == "__main__":
    main()
