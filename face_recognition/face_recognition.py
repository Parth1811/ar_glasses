import os
import cv2
import numpy as np
from datetime import datetime
import time

import database
import camera_driver

FULL_PACKAGE_PATH = os.path.expanduser("~/ar_glasses/face_recognition/")
FACE_CLASSIFIER = cv2.CascadeClassifier(FULL_PACKAGE_PATH + 'haarcascade_frontalface_default.xml')
RECOGNIZER = cv2.face.LBPHFaceRecognizer_create()
#RECOGNIZER = cv2.face.EigenFaceRecognizer_create()
#RECOGNIZER = cv2.face.FisherFaceRecognizer_create()


SCALE_FACTOR = 1.5
MIN_NEIGHBORS = 5

DELAY = 1

def train():
    faces = []
    frames, labels = database.read_all_images()  ## DEBUG: label_type = "char"
    for face in frames:
        faces.append(FACE_CLASSIFIER.detectMultiScale(face, scaleFactor = SCALE_FACTOR, minNeighbors = MIN_NEIGHBORS))

    ## DEBUG:
    '''
    debug_counnter = -1
    for face in faces:
        debug_counnter +=1
        if face == ():
            print labels[debug_counnter]
            continue
        print face, labels[debug_counnter]
    '''

    counter, face_train_array, label_train_array = -1, [], []
    for face in faces:
        counter +=1
        if face == ():
            continue
        for (x, y, w, h) in face:
            crop_face = frames[counter][y:y+h, x:x+w]
            face_train_array.append(cv2.cvtColor(crop_face, cv2.COLOR_RGB2GRAY))
            label_train_array.append(labels[counter])

    RECOGNIZER.train(face_train_array, np.array(label_train_array))
    RECOGNIZER.save("trainner.yaml")

def recognise_face(data, frame = None):
    if frame == None:
        video_feed = camera_driver.cam_read(data["camera"])
    else:
        video_feed = {"frame": frame}
    face = FACE_CLASSIFIER.detectMultiScale(video_feed["frame"], scaleFactor = SCALE_FACTOR, minNeighbors = MIN_NEIGHBORS)
    if face == ():
        data["is_face_present"] = False
        return
    else:
        data["is_face_present"] = True
        for (x, y, w, h) in face:
            data['location'] = {'x':x,'y':y,'w':w,'h':h}
        crop_face = video_feed["frame"][y:y+h,x:x+w]
        crop_face = cv2.cvtColor(crop_face, cv2.COLOR_RGB2GRAY)
        label_index, confidence = RECOGNIZER.predict(crop_face)
        if confidence > 50:
            data["face_info"] = database.read_info(index = label_index)

def run(data):
    var = database.yaml_loader(os.path.join(database.FULL_DATABASE_PATH,"data.yaml"))
    if var["database"]["is_database_updated"]:
        print("Traning on updated database........")
        train()
    else:
        print("Loading already trainned data........")
        RECOGNIZER.read(FULL_PACKAGE_PATH + "trainner.yaml")

    running = True
    while running:
        start_time = datetime.now()
        recognise_face(data)
        dt = (datetime.now()-start_time).total_seconds()
        if  dt < DELAY:
            time.sleep(dt)


if __name__ == '__main__':
    print "++++++++++DEBUG++++++++++"
    data = dict()
    run(data)