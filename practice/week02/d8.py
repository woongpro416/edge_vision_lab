# ?? ??: Day 08 ? BGR/RGB preprocessing? ?? ?? ??? ??? ?????.

import cv2
from pathlib import Path

from week01.d6 import read_image_safe


def convert_bgr_to_rgb(image):

    if image is None:
        raise ValueError("image 가 존재하지 않습니다.")


    if image.ndim != 3 or image.shape[2] !=3:
        raise ValueError("image가 color image가 아닙니다.")


    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return rgb_image

def prepare_model_input_simple(image, width: int, height: int):

    if image is None:
        raise ValueError("image가 존재하지 않습니다.")


    if width <= 0 or height <= 0:
        raise ValueError("width 와 height는 0 이하일 수 없습니다.")


    resized = cv2.resize(image, (width, height))


    rgb_image = convert_bgr_to_rgb(resized)
    return rgb_image

def main():

    image_path = Path("week01/inputs/sample.jpg")


    bgr_image = read_image_safe(image_path)


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