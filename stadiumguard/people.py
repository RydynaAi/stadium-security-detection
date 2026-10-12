from ultralytics import YOLO


class PersonDetector:
    def __init__(self, model_path, confidence):
        self.model = YOLO(model_path)
        self.confidence = confidence

    def detect(self, image):
        result = self.model(image, classes=[0], conf=self.confidence, verbose=False)[0]
        return [tuple(int(value) for value in box) for box in result.boxes.xyxy.tolist()]
    