from pathlib import Path

import cv2


def read_image_safe(image_path: Path):
    # TODO1: cv2.imread(str(image_path))로 이미지 읽기
    image = cv2.imread(str(image_path))
    # TODO2: image가 None이면 FileNotFoundError 발생
    if image is None:
        raise FileNotFoundError(f"이미지가 존재하지 않습니다.{image_path}")
    # TODO3: image 반환
    return image
    


def get_image_info(image):
    # TODO1: image.shape에서 height, width, channels 분리
    heigth, width, channels = image.shape
    # TODO2: image.dtype을 문자열로 변환
    image_dtype = str(image.dtype)
    # TODO3: height, width, channels, dtype dict 반환
    expected_dict = {
        "height": heigth,
        "width": width,
        "channels": channels,
        "dtype": image_dtype,
    }
    return expected_dict

def resize_for_model(image, width: int, height: int):
    # TODO1: width 또는 height가 0 이하이면 ValueError 발생
    if width <= 0 or height <= 0:
        raise ValueError("width 또는 height는 0 또는 음수일 수 없습니다.")
    # TODO2: cv2.resize(image, (width, height)) 실행
    resized = cv2.resize(image, (width,height))
    # TODO3: resized image 반환
    return resized


def crop_center(image, crop_width: int, crop_height: int):
    # TODO1: image.shape[:2]에서 height, width 구하기
    height, width = image.shape[:2]
    # TODO2: crop_width 또는 crop_height가 0 이하이면 ValueError 발생
    if crop_width <= 0 or crop_height <= 0:
        raise ValueError("crop_width, crop_height는 0또는 음수일 수 없습니다.")
    # TODO3: crop 크기가 원본보다 크면 ValueError 발생
    if crop_width > width or crop_height > height:
        raise ValueError("crop 이미지는 원본보다 클 수 없습니다.")
    # TODO4: x1, y1 계산
    # 힌트: (원본 크기 - crop 크기) // 2
    x1 = (width - crop_width) // 2
    y1 = (height - crop_height) // 2
    x2 = x1 + crop_width
    y2 = y1 + crop_height
    # TODO5: x2, y2 계산
    # 힌트: 시작 좌표 + crop 크기
    # TODO6: image[y1:y2, x1:x2]로 crop
    cropped = image[y1:y2, x1:x2]
    # TODO7: cropped image 반환
    return cropped


def save_image(image, output_path: Path) -> None:
    # TODO1: output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # TODO2: cv2.imwrite(str(output_path), image) 결과를 saved 변수에 저장
    saved = cv2.imwrite(str(output_path), image)
    # TODO3: saved가 False면 ValueError 발생
    if not saved:
        raise ValueError("이미지가 저장되지 않았습니다.")


def main():
    # TODO1: inputs/sample.jpg 경로 만들기
    image_path = Path("inputs/sample.jpg")

    # TODO2: 아래 두 output 파일 경로 만들기
    resized_path = Path("outputs/d6_review_resized.jpg")
    cropped_path = Path("outputs/d6_review_cropped.jpg")

    # TODO3: read_image_safe()로 이미지 읽기
    image = read_image_safe(image_path)

    # TODO4: get_image_info() 결과 출력
    print(get_image_info(image))

    # TODO5: resize_for_model(image, 640, 480) 실행
    resized = resize_for_model(image, 640, 480)

    # TODO6: resize 결과 저장
    save_image(resized, resized_path)

    # TODO7: crop_center(image, 320, 240) 실행
    cropped = crop_center(image, 320, 240)

    # TODO8: crop 결과 저장
    save_image(cropped, cropped_path)

    # TODO9: 두 output 파일이 존재하는지 assert
    assert resized_path.exists()
    assert cropped_path.exists()


if __name__ == "__main__":
    main()