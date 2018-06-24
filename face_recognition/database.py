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


def read_single_images(data, path_instead_of_frame = False):
    labels, frames = [], []
    for name in LABEL_LIST:
        variables = yaml_loader(os.path.join(FULL_DATABASE_PATH, name, "data.yaml"))
        profile_pic_path = os.path.join(FULL_DATABASE_PATH,name,"images",variables["profile picture"])
        if path_instead_of_frame:
            frames.append(profile_pic_path)
        else:
            frames.append(cv2.imread(profile_pic_path))

    return frames, LABEL_LIST

def get_profile_picture(label):
    if label in LABEL_LIST:
        variables = yaml_loader(os.path.join(FULL_DATABASE_PATH, label, "data.yaml"))
        profile_pic_path = os.path.join(FULL_DATABASE_PATH,label,"images",variables["profile picture"])
        image =  cv2.imread(profile_pic_path)
        return image
    else:
        print ("NO such user exists")

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

def yaml_save(filepath, data):
    with open(filepath, 'w') as adding_data:
        yaml.dump(data, adding_data)

def add_user(name, filepaths = [], frames = [], profile_pic = "1.jpg",\
    meta_data = "Not available", add_from_terminal = False):            #adding data
    if add_from_terminal:
        full_name = raw_input("Full name: ")
        meta_data = raw_input("Descrption: ")
        name = name.lower()
    else :
        full_name = name
        name = full_name.split()[0].lower()

    counter = 1
    data = {
    "full name" : full_name ,
    "profile picture" : profile_pic ,
    "meta data" : meta_data ,
    "no of images" : len(frames) + len(filepaths)
    }

    if filepaths == [] and frames == []:
        print ("Please Provide either a frame a filepath to image..........")
        return
    else:
        try:
            os.mkdir(os.path.join(FULL_DATABASE_PATH, name))
            os.mkdir(os.path.join(FULL_DATABASE_PATH, name, "images"))
        except:
            pass
        if frames != []:
            for frame in frames:
                cv2.imwrite(os.path.join(FULL_DATABASE_PATH, name, "images", str(counter) + ".jpg"), frame)
                counter += 1
            yaml_save(os.path.join(FULL_DATABASE_PATH, name, "data.yaml"), data)

        if filepaths != []:
            for filepath in filepaths:
                os.system("cp "+ filepath +" "+ os.path.join(FULL_DATABASE_PATH, name, "images", str(counter) + ".jpg"))
                counter += 1
            yaml_save(os.path.join(FULL_DATABASE_PATH, name, "data.yaml"), data)
    global LABEL_LIST
    LABEL_LIST = os.listdir(FULL_DATABASE_PATH)
    LABEL_LIST.remove("data.yaml")
    print ("Added "+ name +" sucessfully to the database.........")

def remove_user(label):
    if label in LABEL_LIST:
        os.system("rm -r " + os.path.join(FULL_DATABASE_PATH, label))
        LABEL_LIST.remove(label)
    else:
        print("Invalid name............")
        print("Please type the exact name of the floder")


if __name__ == "__main__":
    print "+++++++++++DEBUG++++++++++++"
