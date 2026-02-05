import os
from pathlib import Path
import cv2
import requests
from ultralytics import YOLO


def download_test_image():
    test_image_url = "https://ultralytics.com/images/bus.jpg"
    test_image_path = "test_image.jpg"

    if os.path.exists(test_image_path):
        print(f"Test image found at {test_image_path}")
        return test_image_path

    try:
        print(f"Downloading test image...")
        response = requests.get(test_image_url)
        response.raise_for_status()

        with open(test_image_path, "wb") as f:
            f.write(response.content)

        print(f"Test image downloaded and saved to {test_image_path}")
        return test_image_path

    except Exception as e:
        print(f"Error downloading test image: {e}")
        return None

def test_yolo_import():
    try:
        from ultralytics import __version__
        print(__version__)
        return True
    except Exception as e:
        print(f"Error importing ultralytics: {e}")
        return False

def test_yolo_model_loading():
    try:
        print("Loading model YOLOv8n...")
        model = YOLO('yolov8n.pt')
        print("Model loaded")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def test_detection_on_image(model, image_path):
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return False

    try:
        print(f"Detecting on image {image_path}")

        image = cv2.imread(image_path)
        if image is None:
            print(f"Image not found: {image_path}")
            return False

        print(f"Image shape: {image.shape[1]}x{image.shape[0]}")

        results = model(image_path)

        detections = results[0].boxes
        if detections is not None:
            print(f"Found {len(detections)} detections")

            for i, box in enumerate(detections):
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = results[0].names[class_id]

                print(f"Detection {class_name}: {confidence:.2%}")
        else:
            print(f"No detection found")

        annotated_image = results[0].plot()
        output_path = "detection_result.png"
        cv2.imwrite(output_path, annotated_image)
        print(f"Detection saved to {output_path}")

        print("\n👀 Print result")
        cv2.imshow('Oculus - Test YOLO Detection', annotated_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return True

    except Exception as e:
        print(f"Error printing result: {e}")
        return False

def main():
    print("Oculus - Test YOLO Detection")
    print("=" * 40)

    if not test_yolo_import():
        return False

    model = test_yolo_model_loading()
    if model is None:
        return False

    test_image = download_test_image()
    if test_image is None:
        image_file = list(Path('.').glob('*.jpg')) + list(Path('.').glob('*.png'))
        if image_file:
            test_image = str(image_file[0])
            print(f"Test image: {test_image}")
        else:
            print(f"Test image not found")
            return False

    if not test_detection_on_image(model, test_image):
        return False

    print("\n SUCCESS YOLO Detection is available")
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("SUCCESS")
    else:
        print("FAIL")

