# ?? ??: Day 05 ? OpenCV? ?? ?? bounding box? ??? ?????.

from pathlib import Path

import cv2


def main():

    image_path = Path("inputs/sample.jpg")
    output_dir = Path("outputs")
    output_path = output_dir / "boxed_sample.jpg"

    print(image_path.resolve())
    print(image_path.exists())
    image = cv2.imread(str(image_path))


    assert image is not None


    print(image.shape)
    height, width, channels = image.shape



    boxed_image = cv2.rectangle(image, (50, 50), (200, 200), (0,255, 0), 2)


    output_dir.mkdir(exist_ok=True)
    saved =cv2.imwrite(str(output_path), boxed_image)


    assert saved is True
    assert output_path.exists()

if __name__ == "__main__":
    main()