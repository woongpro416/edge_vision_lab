from pathlib import Path
import cv2

def main():
    image_path = Path("inputs/sample.jpg")
    output_dir = Path("outputs")
    output_path = output_dir / "center_box_sample.jpg"

    # TODO 1: image_path.resolve(), image_path.exists() 출력하기
    print(image_path.resolve())
    print(image_path.exists())

    # TODO 2: cv2.imread(str(image_path))로 이미지 읽기
    image = cv2.imread(str(image_path))

    # TODO 3: image is not None 확인하기
    assert image is not None
    # TODO 4: image.shape에서 height, width, channels 분리하기
    height, width, channels = image.shape

    # TODO 5: center_x, center_y 계산하기
    # 힌트: width // 2, height // 2
    center_x = width // 2
    center_y = height // 2

    # TODO 6: box_width = 200, box_height = 150 만들기
    box_width = 200
    box_height = 150

    # TODO 7: x1, y1, x2, y2 계산하기
    x1 = center_x - box_width // 2
    y1 = center_y - box_height // 2
    x2 = center_x + box_width // 2
    y2 = center_y + box_height // 2

    # TODO 8: cv2.rectangle()로 중앙 박스 그리기
    # 색상은 빨간색으로 해보기
    # 힌트: OpenCV BGR에서 빨강은 (0, 0, 255)
    boxed = cv2.rectangle(image, (x1, y1), (x2, y2) ,(0, 0, 255), 2)

    # TODO 9: output_dir 만들기
    output_dir.mkdir(exist_ok=True)

    # TODO 10: cv2.imwrite(str(output_path), boxed_image)로 저장하기
    saved = cv2.imwrite(str(output_path), boxed)

    # TODO 11: saved is True, output_path.exists() 확인하기
    assert saved is True
    assert output_path.exists()


if __name__ == "__main__":
    main()