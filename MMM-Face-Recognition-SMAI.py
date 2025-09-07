# SMAI V1.01 - Face Recognition Module

# Modified by: Pratik & Eben
# This is a modified script from the open source face recognition repo:
#https://github.com/ageitgey/face_recognition
# Patch update to fix bugs

import face_recognition
import picamera
import cv2
import numpy as np
import sys
import os
import time
import argparse

class VideoSource:
    """Class to handle different video sources (PiCamera, RTSP, USB camera)"""
    
    def __init__(self, source_type="picamera", rtsp_url=None, usb_camera_index=0):
        self.source_type = source_type
        self.rtsp_url = rtsp_url
        self.usb_camera_index = usb_camera_index
        self.camera = None
        self.cap = None
        self.output = np.empty((240, 320, 3), dtype=np.uint8)
        
    def initialize(self):
        """Initialize the appropriate video source"""
        try:
            if self.source_type == "picamera":
                self.camera = picamera.PiCamera()
                self.camera.resolution = (320, 240)
                print("PiCamera initialized successfully")
                return True
            elif self.source_type == "rtsp":
                if not self.rtsp_url:
                    print("Error: RTSP URL not provided")
                    return False
                self.cap = cv2.VideoCapture(self.rtsp_url)
                if not self.cap.isOpened():
                    print(f"Error: Could not open RTSP stream: {self.rtsp_url}")
                    return False
                print(f"RTSP stream initialized successfully: {self.rtsp_url}")
                return True
            elif self.source_type == "usb":
                self.cap = cv2.VideoCapture(self.usb_camera_index)
                if not self.cap.isOpened():
                    print(f"Error: Could not open USB camera with index: {self.usb_camera_index}")
                    return False
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
                print(f"USB camera initialized successfully with index: {self.usb_camera_index}")
                return True
            else:
                print(f"Error: Unknown source type: {self.source_type}")
                return False
        except Exception as e:
            print(f"Error initializing video source: {e}")
            return False
    
    def capture_frame(self):
        """Capture a frame from the video source"""
        try:
            if self.source_type == "picamera":
                self.camera.capture(self.output, format="rgb")
                return self.output
            elif self.source_type in ["rtsp", "usb"]:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Could not read frame from video source")
                    return None
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Resize to match expected dimensions
                frame_resized = cv2.resize(frame_rgb, (320, 240))
                return frame_resized
        except Exception as e:
            print(f"Error capturing frame: {e}")
            return None
    
    def release(self):
        """Release video source resources"""
        try:
            if self.camera:
                self.camera.close()
            if self.cap:
                self.cap.release()
        except Exception as e:
            print(f"Error releasing video source: {e}")

# Configuration
def parse_arguments():
    parser = argparse.ArgumentParser(description='Face Recognition Module with multiple video sources')
    parser.add_argument('--source', choices=['picamera', 'rtsp', 'usb'], default='picamera',
                       help='Video source type (default: picamera)')
    parser.add_argument('--rtsp-url', type=str, help='RTSP stream URL (required for rtsp source)')
    parser.add_argument('--usb-index', type=int, default=0, help='USB camera index (default: 0)')
    return parser.parse_args()

# Parse command line arguments
args = parse_arguments()

# Initialize video source
video_source = VideoSource(
    source_type=args.source,
    rtsp_url=args.rtsp_url,
    usb_camera_index=args.usb_index
)

if not video_source.initialize():
    print("Failed to initialize video source. Exiting.")
    sys.exit(1)

# Load a sample picture and learn how to recognize it.
print("Loading known face image(s)")
rec_image = face_recognition.load_image_file("/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/public/face.png")
rec_face_encoding = face_recognition.face_encodings(rec_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []

id_check = 0

try:
    while True:
        print("Capturing image.")
        # Grab a single frame of video from the video source as a numpy array
        output = video_source.capture_frame()
        
        if output is None:
            print("Failed to capture frame. Retrying...")
            time.sleep(1)
            continue

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(output)
        print("Found {} faces in image.".format(len(face_locations)))
        face_encodings = face_recognition.face_encodings(output, face_locations)
    
    face_id = "Guest"
    

    # Loop over each face found in the frame to see if it's someone we know.
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces([rec_face_encoding], face_encoding)
        name = "<Unknown Person>"
   
        if id_check == 0:
            for file in os.listdir("/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/public"):
                if file.endswith("-id.png"):
                    face_id = file.replace('-', ' ').split(' ')[0]
                    #print(face_id)
            id_check = 0
            #print(face_id) -- print the name you saved as the MM picture


        if match[0]:
            name = face_id
        
            

        print("Person Detected: {}!".format(face_id))
        f = open("/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/sample.txt", "w")
        f.write(name)
        f.close()
        #time taken before the user is logged off from the mirror
        time.sleep(15)
        
        f = open("/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/sample.txt", "w")
        f.write(face_id)
        f.close()

except KeyboardInterrupt:
    print("\nShutting down gracefully...")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Clean up video source resources
    video_source.release()
    print("Video source released.")
