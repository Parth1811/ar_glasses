import cv2
from datetime import datetime
from multiprocessing import Process
import sys
import threading
import time
'''
try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    camera = PiCamera()
except:
'''
camera = cv2.VideoCapture(0)

from face_recognition import face_recognition
from face_recognition import face_recognition_ml
from display_helper import display

CAMERA_PORT = 0
DELAY = 1
FULLSCREEN = False
ML_FLAG = False
DISPLAY = True


data = {
    "camera" : camera ,
    "first_run" : True,
    "display_flag" : True,
    "debug_database" : False,
    "debug_train" : False
}

def video_loop(ML_FLAG = False):
    global data
    running = True
    while running:
        start_time = datetime.now()
        if ML_FLAG:
            data = face_recognition_ml.run(data)
        else:
            data = face_recognition.run(data)
        dt = (datetime.now()-start_time).total_seconds()
        if  dt < DELAY:
            time.sleep(DELAY - dt)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for command in sys.argv[1:]:
            if command == "no_display":
                DISPLAY = False
            if command == "debug_train":
                data["debug_train"] = True
                DISPLAY = False
            if command == "debug_database":
                data["debug_database"] = True
            if command == "fullscreen":
                FULLSCREEN = True
            if command == "ml":
                ML_FLAG = True

    try:
        video_thread = threading.Thread(target = video_loop, args=[ML_FLAG])
        video_thread.daemon = True
        video_thread.start()
        if DISPLAY:
            display.run(data, FULLSCREEN)
        else:
            while video_thread.isAlive():
                video_thread.join(10)
    except KeyboardInterrupt:
        sys.exit()
