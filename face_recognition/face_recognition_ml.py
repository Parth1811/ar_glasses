# -*- coding: utf-8 -*-
import PIL.Image
import cv2
import dlib
import numpy as np
from datetime import datetime

import database
import camera_driver
import face_ml_api as api

face_encodings_array = []

def run(data):
    start_time = datetime.now()
    print start_time
    if data["first_run"]:
        #frames, labels = database.read_all_images(data,"char")
        frames = [
        api.load_image_file('/home/parth/ar_glasses/face_recognition/database/dhananjay/images/16.jpg'),
        api.load_image_file('/home/parth/ar_glasses/face_recognition/database/parth/images/16.jpg'),
        api.load_image_file('/home/parth/ar_glasses/face_recognition/database/saavi/images/0.jpg'),
        api.load_image_file('/home/parth/ar_glasses/face_recognition/database/rutvi/images/1.jpg')
        ]

        labels = [
        "dhananjay",
        "parth",
        "saavi",
        "rutvi"
        ]


        for frame in frames:
            face_encodings_array.append(api.face_encodings(frame)[0])
        data["first_run"] = False

    face_encoding_current, matches = [], []
    print (datetime.now()-start_time).total_seconds()
    video_feed = camera_driver.cam_read(data["camera"])
    small_frame = cv2.resize(video_feed["frame"], (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_location = api.face_locations(rgb_small_frame)
    face_encoding_current = api.face_encodings(rgb_small_frame, face_location)
    face_names = []
    for face_encoding in face_encoding_current:
        matches = api.compare_faces(face_encodings_array, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            print first_match_index

        face_names.append(name)
    print face_names
    return data
