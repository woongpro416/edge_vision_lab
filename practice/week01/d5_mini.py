from pathlib import Path

import cv2


def main():

    image_path = Path("inputs/sample.jpg")
    output_dir = Path("outputs")
    output_path = output_dir / "boxed_sample.jpg"
    # TODO 1: image를 읽는다
    print(image_path.resolve())
    print(image_path.exists())
    image = cv2.imread(str(image_path))

    #TODO 2: image가 None이 아닌지 확인한다
    assert image is not None

    #TODO 3: image.shape 에서 height, width, channels를 확인한다
    print(image.shape)
    height, width, channels = image.shape

    #TODO 4: cv2.rectangle()로 고정 좌표 사각형 하나를 그린다.
    #예: (50, 50) 부터 (200, 200) 까지
    boxed_image = cv2.rectangle(image, (50, 50), (200, 200), (0,255, 0), 2)

    #TODO 5: outputs/boxed_sample.jpg로 저장한다
    output_dir.mkdir(exist_ok=True)
    saved =cv2.imwrite(str(output_path), boxed_image)

    #TODO 6: 저장 성공 여부와 파일 존재 여부를 assert로 확인한다.
    assert saved is True
    assert output_path.exists()

if __name__ == "__main__":
    main()