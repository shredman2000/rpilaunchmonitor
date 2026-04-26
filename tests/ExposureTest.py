from pygrabber.dshow_graph import FilterGraph
import cv2

def set_camera_exposure(exposure_value=-10):
    graph = FilterGraph()
    
    # List available cameras
    devices = graph.get_input_devices()
    print("Available cameras:")
    for i, name in enumerate(devices):
        print(f"  {i}: {name}")
    
    # Connect to first camera
    graph.add_video_input_device(0)
    
    # Get camera controls
    camera = graph.get_IAMCameraControl()
    
    # Set exposure manually
    # CameraControl_Exposure = 4
    EXPOSURE = 4
    CameraControl_Flags_Manual = 2
    camera.Set(EXPOSURE, exposure_value, CameraControl_Flags_Manual)
    
    actual = camera.Get(EXPOSURE)
    print(f"Exposure set to: {actual}")
    
    graph.release()

if __name__ == "__main__":
    set_camera_exposure(-10)