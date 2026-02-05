import sys
import cv2


def test_opencv_import():
    try:
        print(f"OpenCv version: {cv2.__version__}")
        return True
    except Exception as e:
        print(f"OpenCv error: {e}")
        return False

def test_webcam_detection():
    print("\n Recherche webcams disponibles...")

    available_cameras = []
    for index in range(5):
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            available_cameras.append(index)
            print(f"Available cameras at index {index}: {available_cameras}")
        cap.release()

    if not available_cameras:
        print("No cameras available")
        return False, None

    return True, available_cameras[0]

def test_webcam_capture(camera_index=0):
    print(f"Testing webcam {camera_index}...")
    print("Press 'q' for quit or 's' for screenshot")

    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"Could not open webcam at index {camera_index}")
        return False

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_count = 0
    screenshot_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error while reading webcam")
            break

        frame_count += 1

        cv2.putText(frame, f"Oculus - Test OpenCV", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Frame: {frame_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "Press 'q' pour quit, 's' for screenshot", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)

        cv2.imshow("Oculus - Test Webcam", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Quit")
            break
        elif key == ord('s'):
            screenshot_count += 1
            filename = f"screenshot_{screenshot_count}.png"
            cv2.imwrite(filename, frame)
            print("Screenshot saved")

    cap.release()
    cv2.destroyAllWindows()
    return True

def main():
    print("Testing opencv import...")
    print("=" * 40)

    if not test_opencv_import():
        print("OpenCv import error")
        return False

    webcam_found, camera_index = test_webcam_detection()
    if not webcam_found:
        print("Webcam not found at index", camera_index)
        return False

    print("Launching capture...")
    input("Press Enter to continue...")

    if not test_webcam_capture(camera_index):
        print("Webcam not found at index", camera_index)
        return False

    print("OpenCV & Webcam OK")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
