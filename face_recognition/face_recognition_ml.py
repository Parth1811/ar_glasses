# -*- coding: utf-8 -*-
import PIL.Image
import cv2
import dlib
import numpy as np
from datetime import datetime
import time

import database
import camera_driver
import face_ml_api as api

face_encodings_array = []

def run(data):
    if data["first_run"]:
        #frames, labels = database.read_all_images(data,"char")
        paths, labels = database.read_single_images(data, path_instead_of_frame = True)
        print ("Trainning on database............")
        for path in paths:
            frame = api.load_image_file(path)
            face_encodings_array.append(api.face_encodings(frame)[0])
            time.sleep(1)
        data["first_run"] = False

    face_encoding_current, matches = [], []
    #video_feed = camera_driver.cam_read(data["camera"])
    small_frame = cv2.resize(data["frame"], (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_location = api.face_locations(rgb_small_frame)
    if face_location != []:
        data["is_face_present"] = True
        face_info = []
        data["location"] = face_location
        face_encoding_current = api.face_encodings(rgb_small_frame, face_location)
        for face_encoding in face_encoding_current:
            matches = api.compare_faces(face_encodings_array, face_encoding)

            if True in matches:
                first_match_index = matches.index(True)
                face_info.append(database.read_info(label = database.LABEL_LIST[first_match_index]))
            else:
                face_info.append({"full name" : "No match"})
        data["face_info"] = face_info
    else:
        data["is_face_present"] = False
        try:
            del data["location"], data["face_info"]
        except :
            pass

    return data
