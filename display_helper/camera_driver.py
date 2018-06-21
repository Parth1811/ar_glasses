import cv2
from datetime import datetime

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    on_laptop = False
except:
    on_laptop = True

CAMERA_PORT = 0
#camera = cv2.VideoCapture(CAMERA_PORT)

def cam_read(camera):
    if on_laptop:
        video_feed = cam_read_laptop(camera)
    else:
        video_feed = cam_read_rpi(camera)
    return video_feed

def cam_read_laptop(camera):
    rect, frame = camera.read()
    video_feed = dict()
    if rect:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        video_feed["is_read"] = True
        video_feed["frame"] = frame
        video_feed["timestamp"] = str(datetime.now())
    else:
        video_feed["is_read"] = False
        video_feed["frame"] = None
        video_feed["timestamp"] = str(datetime.now())
    return video_feed

def cam_read_rpi(picamera):
    #rect, frame = camera.read()
    raw = PiRGBArray(camera)
    picamera.capture(raw, format = "bgr")
    frame = raw.array
    rect = True
    video_feed = dict()
    if rect:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        video_feed["is_read"] = True
        video_feed["frame"] = frame
        video_feed["timestamp"] = str(datetime.now())
    else:
        video_feed["is_read"] = False
        video_feed["frame"] = None
        video_feed["timestamp"] = str(datetime.now())
    return video_feed



def disable_camera():
    camera.release()
    print("Disabling camera.............")
