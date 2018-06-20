import sys
import numpy as np
import os
import cv2
import yaml

FULL_DATABASE_PATH = os.path.expanduser("~/ar_glasses/face_recognition/database")
LABEL_ID={}
def read_all_images():
    labels, frames, currid = [], [], 0
    for root,dirs,files in os.walk(FULL_DATABASE_PATH):
        for file in files:
            if file.endswith("jpg") or file.endswith("png"):
                path = os.path.join(root, file)
                label=os.path.basename(root).replace(" ","-").lower()
                if not label in LABEL_ID:
                    LABEL_ID[label]=currid
                    currid+=1
                id_= LABEL_ID[label]
                frame = cv2.imread(path)
                labels.append(LABEL_ID[label])
                frames.append(frame)
    return frames, labels

def read_info(label = False, index = False):
    if index == False:
        if label == False:
            print ("Invalid inputs")
            return dict()
        else:
            index = int(get_folder_index(label))

    yaml_path = os.path.join(FULL_DATABASE_PATH, os.listdir(FULL_DATABASE_PATH)[index], "data.yaml")
    data = yaml_loader(yaml_path)
    return data

def get_folder_index(label):
    folder_list = os.listdir(FULL_DATABASE_PATH)
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
    #read_all_images()
    print read_info(label ="saavi")
    #print A, B, C
    #data = yaml_loader("./database/savvi/data.yaml")
    #me = data.get('saavi yadav')
    #print me
    '''
    for text1, text2 in me.iteritems():
    print (text1)
    '''
    '''
    data1 = data["saavi yadav"]["images"][0]
    print data1
    image_display = cv2.imread(data1)
    cv2.imshow('see', image_display)
    cv2.waitKey(0)
    cv2.destroyAllwindows()
    #for text1, text2 in data.iteritems():
    # print text1, text2
    '''
