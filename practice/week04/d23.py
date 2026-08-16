# Day 23 학습: 실제 YOLO Results를 관찰하고 기존 Detection pipeline에 연결한다.
from pathlib import Path

from ultralytics import YOLO

from week03.d16 import convert_detections
from week04.d23_real_yolo_adapter import build_raw_detections_from_yolo_result


model = YOLO("yolo11n.pt")

image_path = Path("week01/inputs/sample.jpg")
results = model(image_path)

result = results[0]

print(type(results))
print(len(results))
print(type(result))
print(type(result.boxes))
print(len(result.boxes))
print(type(result.boxes.xyxy))
print(result.boxes.xyxy)
print(result.boxes.cls)
print(result.boxes.conf)
print(result.names)


raw_results = build_raw_detections_from_yolo_result(result)
print(len(raw_results))
print(raw_results[0])

detections = convert_detections(raw_results, threshold=0.6)
print(detections)
