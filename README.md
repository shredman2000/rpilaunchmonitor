# rpilaunchmonitor
Working on a DIY launch monitor.

## Overview
- Set up, calibrate, and synchronize cameras.
- Implement triangulation to determine 3D ball position
- Compute motion metrics:
  - Ball Speed
  - Launch angle (x, y)
  - Horizontal angle (z)
  - Explore methods for estimating spin rate and axis
    - Using landmarks on the golf ball. (dimples, drawn on markings?)
- Output shot data into simulation software (OpenGolfSim) 
       
## Hardware
- Raspberry Pi 3 Model B (Might need an upgrade/dedicated computer)
- 2x USB global shutter cameras (OV9281)
- Fixed housing for components
- Lighting, possible strobe
- Sound trigger sensor (TBD)
  
<img width="960" height="720" alt="Untitled drawing" src="https://github.com/user-attachments/assets/fa35548b-ea49-4134-add3-721317c1ed55" />

## System Architecture
1. Cameras continuously capture frames and stream them to the RPI
2. Frames from each camera are stored in a rolling buffer with timestamps
3. A sound sensor detects impact and signals an event
4. Upon trigger:
   - A window of frames is extracted from each buffer (pre-trigger + post-trigger)
   - Frames are aligned between cameras using timestamps
5. Image processing pipeline detects the ball in each frame within the extracted window
6. Corresponding ball positions between camera views are identified
7. Triangulation is used to compute the 3D position of the ball over time
8. Position data is used to calculate metrics
9. Additional processing estimates spin characteristics
10. Shot data is formatted for simulator integration

## Key issues to address
- Cameras are USB which will result in frame disalignment between the two cameras
  - Possible fixes to explore:
    - Nearest neighbor frame matching
    - Buffer delay to align streams
- Exposure/Lighting and shutter speed
  - Should be able to configure shutter speed to shorter exposure (1/2000ms?)
  - If this causes issues with darkness increase shutter length 
  
- Raspberry Pi 3b bottleneck
  - Consider offloading computations to external server

