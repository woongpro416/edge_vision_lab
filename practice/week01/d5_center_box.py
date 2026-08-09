# 학습 요약: Day 05 — 이미지 중심 좌표를 기준으로 bounding box를 계산한다.

from pathlib import Path
import cv2

def main():
    image_path = Path("inputs/sample.jpg")
    output_dir = Path("outputs")
    output_path = output_dir / "center_box_sample.jpg"


    print(image_path.resolve())
    print(image_path.exists())


    image = cv2.imread(str(image_path))


    assert image is not None

    height, width, channels = image.shape



    center_x = width // 2
    center_y = height // 2


    box_width = 200
    box_height = 150


    x1 = center_x - box_width // 2
    y1 = center_y - box_height // 2
    x2 = center_x + box_width // 2
    y2 = center_y + box_height // 2




    boxed = cv2.rectangle(image, (x1, y1), (x2, y2) ,(0, 0, 255), 2)


    output_dir.mkdir(exist_ok=True)


    saved = cv2.imwrite(str(output_path), boxed)


    assert saved is True
    assert output_path.exists()


if __name__ == "__main__":
    main()
