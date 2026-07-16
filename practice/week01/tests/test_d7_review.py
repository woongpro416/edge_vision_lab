import numpy as np
import pytest

from d7_review import (
    convert_bgr_to_rgb,
    convert_rgb_to_bgr,
    prepare_model_input,
    prepare_model_input_with_info,
)


def make_test_bgr_image():
    return np.zeros((4, 6, 3), dtype=np.uint8)


def test_convert_bgr_to_rgb_swaps_known_pixel():
    bgr_image = np.array([[[10, 20, 30]]], dtype=np.uint8)
    rgb_image = convert_bgr_to_rgb(bgr_image)
    assert rgb_image[0, 0].tolist() == [30, 20, 10]


def test_convert_bgr_to_rgb_keeps_shape_and_dtype():
    image = make_test_bgr_image()
    rgb_image = convert_bgr_to_rgb(image)
    assert image.shape == rgb_image.shape
    assert image.dtype == rgb_image.dtype


def test_bgr_rgb_bgr_round_trip_restores_original_image():
    image = make_test_bgr_image()
    image[0, 0] = [10, 20, 30]
    rgb_image = convert_bgr_to_rgb(image)
    restored_image = convert_rgb_to_bgr(rgb_image)
    assert (restored_image == image).all()


def test_convert_bgr_to_rgb_raises_for_none():
    with pytest.raises(ValueError):
        convert_bgr_to_rgb(None)


def test_convert_bgr_to_rgb_raises_for_grayscale_image():
    gray_image = np.zeros((4, 6), dtype=np.uint8)
    with pytest.raises(ValueError):
        convert_bgr_to_rgb(gray_image)


def test_prepare_model_input_returns_requested_shape():
    image = make_test_bgr_image()
    model_input = prepare_model_input(image, 320, 240)
    assert model_input.shape == (240, 320, 3)


def test_prepare_model_input_with_info_returns_expected_metadata():
    image = make_test_bgr_image()
    processed_image, metadata = prepare_model_input_with_info(image, 320, 240)
    assert processed_image.shape == (240, 320, 3)
    assert metadata["originalHeight"] == 4
    assert metadata["originalWidth"] == 6
    assert metadata["targetHeight"] == 240
    assert metadata["targetWidth"] == 320
    assert metadata["inputColorSpace"] == "BGR"
    assert metadata["outputColorSpace"] == "RGB"
    assert metadata["dtype"] == "uint8"
