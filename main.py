import cv2
from datetime import datetime
from multiprocessing import Process
from multiprocessing import Manager
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
from drivers import camera_driver


CAMERA_PORT = 0
DELAY = 1
FPS =30
FULLSCREEN = False
ML_FLAG = False
DISPLAY = True
PROCESS_FLAG = False

manager = Manager()
data = manager.dict()
data ["camera"] = camera
data["first_run"] = True
data["display_flag"] = True
data["debug_database"] = False
data["debug_train"] = False

def camera_feed():
    global data
    camera_ = camera
    running = True
    while running:
        start_time = datetime.now()
        delay = 1/float(FPS)
        data["frame"] = camera_driver.cam_read(camera)["frame"]
        dt = (datetime.now()-start_time).total_seconds()
        if  dt < delay:
            time.sleep(delay - dt)

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
            if command == "pro":
                PROCESS_FLAG = True

    try:
        video_feed = threading.Thread(target = camera_feed)
        video_feed.daemon = True
        video_feed.start()
        time.sleep(5)
        if PROCESS_FLAG:
            video_thread = Process(target = video_loop, args=[ML_FLAG])
        else:
            video_thread = threading.Thread(target = video_loop, args=[ML_FLAG])
        video_thread.daemon = True
        video_thread.start()
        if DISPLAY:
            display.run(data, FULLSCREEN)
        else:
            while video_feed.isAlive():
                video_thread.join(10)

        # while True:
        #     try:
        #         if data["frame"] == None:
        #             print data
        #     except:
        #         pass

    except KeyboardInterrupt:
        sys.exit()
