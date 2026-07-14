from pathlib import Path
import pytest
import numpy as np

from d6 import (
    crop_center,
    get_image_info,
    read_image_safe,
    resize_for_model,
    save_image,
)

def make_test_image():
    # TODO: height=480, width=640, channels=3인 uint8 이미지 만들기
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    return image

def test_read_image_safe_raises_for_missing_path():
    missing_path = Path("inputs/does_not_exist.jpg")

    # TODO: pytest.raises(FileNotFoundError) 작성
    with pytest.raises(FileNotFoundError):
        
        # TODO: 블록 안에서 read_image_safe(missing_path) 호출
        read_image_safe(missing_path)

def test_get_image_info_returns_expected_dict():
    image = make_test_image()

    # TODO1: get_image_info(image) 호출해서 info 변수에 저장
    image_info = get_image_info(image)

    # TODO2: 기대하는 dict 만들기
    # height=480, width=640, channels=3, dtype="uint8"
    expected_dict = {
        "height": 480,
        "width": 640,
        "channels": 3,
        "dtype": "uint8",
    }

    # TODO3: info와 기대 dict가 같은지 assert
    assert image_info == expected_dict

def test_resize_for_model_return_requested_shape():
    image = make_test_image()

    # TODO: resize_fir_model(image, 320, 240) 호출
    resized = resize_for_model(image, 320, 240)
    # TODO: 결과 shape가 (240, 320, 3) 인지 assert
    assert resized.shape == (240, 320, 3)

def test_crop_center_returns_requested_shape():
    image = make_test_image()

    # TODO: crop_center(image, 320, 240) 호출
    cropped = crop_center(image, 320, 240)
    # TODO: 결과 shape가 (240, 320, 3) 인지 assert
    assert cropped.shape == (240, 320, 3)

def test_crop_center_raises_for_oversized_crop():
    image = make_test_image()

    # TODO1: with pytest.raises(ValueError) 작성
    with pytest.raises(ValueError):
        crop_center(image, 641, 240)

def test_crop_center_raises_for_zero_crop_width():
    image = make_test_image()

    # TODO: with pytest.raises(ValueError) 작성
    with pytest.raises(ValueError):
        crop_center(image, 0, 240)
    # TODO: crop_center(image, 0, 240) 호출


def test_crop_center_raises_for_negative_crop_height():
    image = make_test_image()

    # TODO: with pytest.raises(ValueError) 작성
    with pytest.raises(ValueError):
        crop_center(image, 320, -1)



def test_save_image_creates_file():
    image = make_test_image()
    output_path = Path("outputs/test_saved.jpg")

    # TODO: save_image(image, output_path) 호출
    save_image(image, output_path)
    # TODO: output_path.exsits()가 True 인지 assert
    assert output_path.exists()