import sys
import numpy as np
import os
import cv2
import yaml

FULL_DATABASE_PATH = os.path.expanduser("~/ar_glasses/face_recognition/database")

LABEL_LIST = os.listdir(FULL_DATABASE_PATH)
LABEL_LIST.remove("data.yaml")

def read_all_images(data, label_type = "int"):
    labels, frames = [], []
    for root,dirs,files in os.walk(FULL_DATABASE_PATH):
        ## DEBUG:
        if data["debug_database"]:
            print '==========='
            print files , root
            print '==========='

        for file in files:
            if file.endswith("jpg"):
                frame = cv2.imread(os.path.join(root, file))
                label = root.split('/')[-2]
                if label_type == "int":
                    labels.append(LABEL_LIST.index(label))
                elif label_type == "char":
                    labels.append(label)
                frames.append(np.array(frame,dtype = 'uint8'))
    return frames, labels

def read_info(label = False, index = False):
    if index == False:
        if label == False:
            print ("Invalid inputs")
            return dict()
        else:
            index = int(get_folder_index(label))

    yaml_path = os.path.join(FULL_DATABASE_PATH, LABEL_LIST[index], "data.yaml")
    data = yaml_loader(yaml_path)
    return data

def get_folder_index(label):
    folder_list = LABEL_LIST
    index = folder_list.index(label)
    return index

def yaml_loader(filepath):               #loading information from yaml file
    with open(filepath, 'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def add_user(filepath, data):            #adding data
    with open(filepath, 'w') as adding_data:
        yaml.dump(data, adding_data)

if __name__ == "__main__":
    print "+++++++++++DEBUG++++++++++++"
