import cv2
from datetime import datetime

def cam_read(camera):
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

def disable_camera():
    camera.release()
    print("Disabling camera.............")
