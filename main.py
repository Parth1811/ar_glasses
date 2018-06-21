import cv2
from datetime import datetime
from multiprocessing import Process
import threading
import time

from face_recognition import face_recognition
from display_helper import display

CAMERA_PORT = 0
DELAY = 1

data = {
    "camera" : cv2.VideoCapture(0) ,
    "first_run" : True
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

video_thread = threading.Thread(target = video_loop)
video_thread.setDaemon(True)
video_thread.start()
display.run(data)
video_thread.join()
