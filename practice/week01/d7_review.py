# ?? ??: Day 07 Review ? BGR/RGB ??? preprocessing metadata? ?????.

from pathlib import Path

import cv2
import matplotlib.pyplot as plt

from d6 import read_image_safe, resize_for_model, save_image


def convert_bgr_to_rgb(image):
    if image is None:
        raise ValueError("이미지가 존재하지 않습니다.")
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("image가 3채널 컬러 이미지가 아닙니다.")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def convert_rgb_to_bgr(image):
    if image is None:
        raise ValueError("이미지가 존재하지 않습니다.")
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("image가 3채널 컬러 이미지가 아닙니다.")
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


def save_rgb_preview(rgb_image, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, axis = plt.subplots()
    axis.imshow(rgb_image)
    axis.axis("off")
    fig.savefig(output_path)
    plt.close(fig)


def prepare_model_input(image, width: int, height: int):
    if width <= 0 or height <= 0:
        raise ValueError("width, height는 0 이하일 수 없습니다.")
    resized = resize_for_model(image, width, height)
    return convert_bgr_to_rgb(resized)


def prepare_model_input_with_info(image, width: int, height: int):
    original_height, original_width = image.shape[:2]
    processed_image = prepare_model_input(image, width, height)
    metadata = {
        "originalHeight": original_height,
        "originalWidth": original_width,
        "targetHeight": height,
        "targetWidth": width,
        "inputColorSpace": "BGR",
        "outputColorSpace": "RGB",
        "dtype": str(processed_image.dtype),
    }
    return processed_image, metadata


def main():
    image_path = Path("inputs/sample.jpg")
    rgb_output_path = Path("outputs/d7_review_rgb_preview.png")
    bgr_output_path = Path("outputs/d7_review_bgr_restored.jpg")

    image = read_image_safe(image_path)
    rgb_image = convert_bgr_to_rgb(image)
    restored_bgr = convert_rgb_to_bgr(rgb_image)

    print(image.shape)
    print(image.dtype)
    print(rgb_image.shape)
    print(rgb_image.dtype)

    assert (restored_bgr == image).all()

    save_rgb_preview(rgb_image, rgb_output_path)
    assert rgb_output_path.exists()

    save_image(restored_bgr, bgr_output_path)
    assert bgr_output_path.exists()

    model_input, model_input_info = prepare_model_input_with_info(image, 640, 480)
    assert model_input.shape == (480, 640, 3)
    assert model_input_info["inputColorSpace"] == "BGR"
    assert model_input_info["outputColorSpace"] == "RGB"
    assert model_input_info["targetWidth"] == 640
    assert model_input_info["targetHeight"] == 480
    print(model_input_info)


if __name__ == "__main__":
    main()
