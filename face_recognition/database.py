import sys
import numpy as np
import os
import cv2
import yaml

FULL_DATABASE_PATH = os.path.expanduser("~/ar_glasses/face_recognition/database")
LABEL_ID={}
def read_all_images():
  labels = []
  frames = []
  
  currid=0
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
  #print LABEL_ID
  return frames, labels

def read_info(label_index = False, labels = False):
  data = yaml_loader("data.yaml")
  if label_index == False:
    if labels == False:
      print "error"

    else:
      DATA1 = data[labels]["data"]["META DATA"]
      print DATA1
      return data[labels]["data"]["FULL NAME"], data[labels]["data"]["PROFILE PICTURE"], data[labels]["data"]["META DATA"]
  
  else:
    for labels_ in LABEL_ID:
      if LABEL_ID[labels_] == label_index:
       # print labels_
        DATA1 = data[labels_]["data"]["META DATA"]
        #print DATA1
        return data[labels_]["data"]["FULL NAME"], data[labels_]["data"]["PROFILE PICTURE"], data[labels_]["data"]["META DATA"] 
  

def yaml_loader(filepath):               #loading information from yaml file
  with open(filepath, 'r') as file_descriptor:
    data = yaml.load(file_descriptor)

  return data

def add_user(filepath, data):            #adding data
  with open(filepath, 'w') as adding_data:
    yaml.dump(data, adding_data)



if __name__ == "__main__":
  read_all_images()
  print read_info(2, False)
 #print A, B, C
  data = yaml_loader("data.yaml")
  me = data.get('saavi yadav')
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
