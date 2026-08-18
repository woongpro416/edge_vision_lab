# Day 24 실습: 모델 값 → Python 기본 자료형 → 서비스 raw_detection

from week04.d21 import build_raw_detection


def main() -> dict:
    model_xyxy = (10.5, 20.3, 100.8, 200.1)
    model_class_id = 2.0
    model_confidence = 0.87
    names = {0: "person", 2: "car"}

    bbox = list(model_xyxy)
    class_id_int = int(model_class_id)
    confidence_float = float(model_confidence)
    class_name = names[class_id_int]

    model_detection = {
        "xyxy": bbox,
        "class_id": class_id_int,
        "class_name": class_name,
        "confidence": confidence_float,
    }

    raw_detection = build_raw_detection(model_detection)

    print(raw_detection)
    print(type(bbox))
    print(type(class_id_int))
    print(type(class_name))
    print(type(confidence_float))

    return raw_detection


if __name__ == "__main__":
    main()
