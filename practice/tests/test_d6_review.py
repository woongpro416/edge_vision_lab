from pathlib import Path

import numpy as np
import pytest

from d6_review import (
    crop_center,
    get_image_info,
    read_image_safe,
    resize_for_model,
    save_image,
)


def make_test_image():
    # TODO: np.zeros()로 (480, 640, 3), uint8 이미지 생성
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    return image


def test_read_image_safe_raises_for_missing_path():
    missing_path = Path("inputs/does_not_exist.jpg")

    # TODO: pytest.raises(FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        read_image_safe(missing_path)
    # TODO: read_image_safe(missing_path) 호출


def test_get_image_info_returns_expected_dict():
    image = make_test_image()

    # TODO: get_image_info(image) 호출
    image_info = get_image_info(image)
    # TODO: 기대 dict 작성
    expected_dict = {
        "height": 480,
        "width": 640,
        "channels": 3,
        "dtype": "uint8",
    }
    # TODO: 두 dict가 같은지 assert
    assert image_info == expected_dict


def test_resize_for_model_returns_requested_shape():
    image = make_test_image()

    # TODO: resize_for_model(image, 320, 240) 호출
    resized = resize_for_model(image, 320, 240)
    # TODO: shape가 (240, 320, 3)인지 assert
    assert resized.shape == (240, 320, 3)


def test_crop_center_returns_requested_shape():
    image = make_test_image()

    # TODO: crop_center(image, 320, 240) 호출
    cropped = crop_center(image, 320, 240)
    # TODO: shape가 (240, 320, 3)인지 assert
    assert cropped.shape == (240, 320, 3)


def test_crop_center_raises_for_oversized_crop():
    image = make_test_image()

    # TODO: pytest.raises(ValueError)
    with pytest.raises(ValueError):
        crop_center(image, 641, 240)
    # TODO: crop_center(image, 641, 240) 호출


def test_crop_center_raises_for_zero_crop_width():
    image = make_test_image()

    # TODO: pytest.raises(ValueError)
    with pytest.raises(ValueError):
        crop_center(image, 0, 240)
    # TODO: crop_center(image, 0, 240) 호출


def test_crop_center_raises_for_negative_crop_height():
    image = make_test_image()

    # TODO: pytest.raises(ValueError)
    with pytest.raises(ValueError):
        crop_center(image, 320, -1)
    # TODO: crop_center(image, 320, -1) 호출


def test_save_image_creates_file():
    image = make_test_image()
    output_path = Path("outputs/test_d6_review_saved.jpg")

    # TODO: save_image(image, output_path) 호출
    save_image(image, output_path)
    # TODO: output_path.exists() assert
    assert output_path.exists()