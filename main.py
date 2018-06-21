import cv2
from datetime import datetime
from multiprocessing import Process
import sys
import threading
import time

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    camera = PiCamera()
except:
    camera = cv2.VideoCapture(0)

from face_recognition import face_recognition
from display_helper import display

CAMERA_PORT = 0
DELAY = 1


data = {
    "camera" : camera ,
    "first_run" : True,
    "display_flag" : True,
    "debug_database" : False,
    "debug_train" : False
}

def video_loop():
    global data
    running = True
    while running:
        try:
            start_time = datetime.now()
            data = face_recognition.run(data)
            dt = (datetime.now()-start_time).total_seconds()
            if  dt < DELAY:
                time.sleep(DELAY - dt)
        except KeyboardInterrupt:
            running = False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for command in sys.argv[1:]:
            if command == "no_display":
                data["display_flag"] = False
            if command == "debug_train":
                data["debug_train"] = True
            if command == "debug_database":
                data["debug_database"] = True

    video_thread = threading.Thread(target = video_loop)
    video_thread.setDaemon(True)
    video_thread.start()
    if data["display_flag"]:
        display.run(data)
    video_thread.join()
