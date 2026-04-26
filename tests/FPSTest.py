import cv2
import time

import cv2
print(cv2.getBuildInformation())

def test_config(camera_index, width, height, fps, exposure):
    cap = cv2.VideoCapture(camera_index, cv2.CAP_MSMF)
    if not cap.isOpened():
        print(f"  Failed to open camera")
        return

    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, fps)

    cap.grab()


    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
    cap.set(cv2.CAP_PROP_EXPOSURE, -10)

    actual_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    actual_exp = cap.get(cv2.CAP_PROP_EXPOSURE)

    # Warm up — first few frames are often slow
    for _ in range(10):
        cap.read()

    # Measure real throughput
    count = 0
    start = time.time()
    while count < 100:
        ret, _ = cap.read()
        if not ret:
            break
        count += 1
    elapsed = time.time() - start
    real_fps = count / elapsed if elapsed > 0 else 0

    print(f"  Requested:  {width}x{height} @ {fps}fps  exposure={exposure}")
    print(f"  Got:        {actual_w:.0f}x{actual_h:.0f}  exposure={actual_exp:.4f}  real fps={real_fps:.1f}")
    print()

    cap.release()


def run_tests(camera_index):
    print(f"=== Camera {camera_index} config sweep ===\n")

    configs = [
        # (width, height, fps, exposure)
        # Baseline
        (1280, 800,  100, None),

        # Lower resolution — does fps improve?
        (800,  600,  100, None),
        (640,  480,  100, None),
        (320,  240,  100, None),

        # Push fps harder at low res
        (640,  480,  200, None),
        (320,  240,  200, None),
        (320,  240,  300, None),

        # Short exposures at full res (values are log2 seconds on most drivers,
        # so -7 = 1/128s, -10 = 1/1024s, -13 = 1/8192s)
        (1280, 800,  100, -7),
        (1280, 800,  100, -10),
        (1280, 800,  100, -13),

        # Short exposure + low res
        (640,  480,  100, -10),
        (640,  480,  100, -13),
    ]

    for width, height, fps, exposure in configs:
        label = f"{width}x{height} @ {fps}fps exp={exposure}"
        print(f"--- {label} ---")
        test_config(camera_index, width, height, fps, exposure)


if __name__ == "__main__":
    run_tests(camera_index=0)