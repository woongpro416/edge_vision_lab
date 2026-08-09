# 학습 요약: Day 05 — OpenCV 이미지 읽기, shape 확인, resize를 연습한다.

from pathlib import Path
import cv2

def main():
    image_path = Path("inputs/sample.jpg")
    output_dir = Path("outputs")
    output_path = output_dir / "resized_sample.jpg"


    image = cv2.imread(str(image_path))



    assert image is not None


    print(type(image))
    print(image.shape)
    print(image.dtype)


    height, width, channels = image.shape



    resized = cv2.resize(image, (640, 480))


    output_dir.mkdir(exist_ok=True)


    saved = cv2.imwrite(str(output_path), resized)


    assert saved is True
    assert output_path.exists()

if __name__ == "__main__":
    main()
