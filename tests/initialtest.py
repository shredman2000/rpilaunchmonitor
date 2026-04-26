import cv2
import time

def test_camera(camera_index=0):
    print(f"Opening camera {camera_index}...")
    cap = cv2.VideoCapture(camera_index, cv2.CAP_MSMF)

    if not cap.isOpened():
        print(f"Failed to open camera {camera_index}")
        return

    # Request 100fps and correct resolution
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
    cap.set(cv2.CAP_PROP_FPS, 100)

    # Report what we actually got
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    actual_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Requested: 1280x800 @ 100fps")
    print(f"Got:       {actual_w:.0f}x{actual_h:.0f} @ {actual_fps:.0f}fps")

    # Measure real throughput over 200 frames
    print("\nMeasuring real frame rate over 200 frames...")
    frame_count = 0
    start = time.time()

    while frame_count < 200:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame")
            break
        frame_count += 1

    elapsed = time.time() - start
    real_fps = frame_count / elapsed
    print(f"Real throughput: {real_fps:.1f} fps")

    # Live preview
    print("\nShowing live preview — press Q to quit")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Burn fps onto the frame so you can see it live
        cv2.putText(frame, f"{real_fps:.1f} fps", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow("Camera Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    test_camera(camera_index=0)