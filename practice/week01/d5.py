from pathlib import Path
import cv2

def main():
    image_path = Path("inputs/sample.jpg")
    output_dir = Path("outputs")
    output_path = output_dir / "resized_sample.jpg"

    #TODO 1: cv2.imread(str(image_path))로 이미지 읽기
    image = cv2.imread(str(image_path))

    #TODO 2: image가 None인지 확인하기
    #힌트 : 경로가 틀리면 OpenCv는 에러 대신 None을 줄 수 있음
    assert image is not None

    # TODO 3: type(image), image.shape, image.dtype 출력하기
    print(type(image))
    print(image.shape)
    print(image.dtype)

    #TODO 4: image.shape에서 height, width, channels 분리하기
    height, width, channels = image.shape

    #TODO 5: cv2.resize()로 640X480 크기로 변경하기
    # 주의 : resize 크기는 (width, height) 순서
    resized = cv2.resize(image, (640, 480))

    # TODO 6: outputs 폴더 만들기
    output_dir.mkdir(exist_ok=True)

    # TODO 7: cv2.imwrite(str(output_path), resized_image)로 저장하기
    saved = cv2.imwrite(str(output_path), resized)

    #TODO 8: output_path.exists()로 저장 여부 확인하기
    assert saved is True
    assert output_path.exists()

if __name__ == "__main__":
    main()
