# Day 25 학습: Model Threshold와 Service Threshold 비교 실험

from pathlib import Path

from ultralytics import YOLO

from week04.d24_review import build_raw_detections_from_yolo_result
from week03.d16 import convert_detections

model_path = Path("yolo11n.pt")
model = YOLO(model_path)

image_path = Path("week01/inputs/sample.jpg")

model_threshold_A = 0.25
model_threshold_B = 0.70
service_threshold = 0.60


def run_case(
    model: YOLO,
    image_path: Path,
    model_threshold: float,
    service_threshold: float,
) -> dict:
    results = model.predict(source=image_path, conf=model_threshold)

    result = results[0]

    model_detections = len(result.boxes)

    raw_results = build_raw_detections_from_yolo_result(result)

    detections = convert_detections(raw_results, service_threshold)

    return {
        "model_threshold": model_threshold,
        "model_detections": model_detections,
        "raw_results": len(raw_results),
        "service_detections": len(detections),
    }


def main():
    case_a_result = run_case(
        model=model,
        image_path=image_path,
        model_threshold=model_threshold_A,
        service_threshold=service_threshold
    )

    case_b_result = run_case(
        model=model,
        image_path=image_path,
        model_threshold=model_threshold_B,
        service_threshold=service_threshold
    )

    records = [case_a_result, case_b_result]

    print("model threshold | model detections | raw_results | service detections")

    for record in records:
        print(
            f"{record['model_threshold']:.2f} | "
            f"{record['model_detections']} | "
            f"{record['raw_results']} | "
            f"{record['service_detections']}"
        )


if __name__ == "__main__":
    main()
