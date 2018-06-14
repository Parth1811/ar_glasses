import os
import cv2
import pickle
import numpy as np
from PIL import Image
xtrain=[]
ylabel=[]
currid=0
labelid={}

facec = cv2.CascadeClassifier('/home/saavi/Downloads/opencvtut/opencv-3.4.1/data/haarcascades/haarcascade_frontalface_default.xml')
recog=cv2.face.LBPHFaceRecognizer_create()

for root,dirs,files in os.walk("."):
 for file in files:
  if file.endswith("jpg") or file.endswith("png"):
   path = os.path.join(root, file)
   label=os.path.basename(root).replace(" ","-").lower()
   #print(path,label)
   if not label in labelid:
    labelid[label]=currid
    currid+=1

   id_=labelid[label]
   #print(labelid)
   #ylabel.append(label)
   #xtrain.append(path)
   pil_image=Image.open(path).convert("L")
   size=(550,550)
   final_image=pil_image.resize(size, Image.ANTIALIAS)
   imagea=np.array(final_image, "uint8")
   #print(imagea)
   faces = facec.detectMultiScale(imagea, scaleFactor=1.5, minNeighbors=5)
   for (x,y,w,h) in faces:
    roi=imagea[y:y+h, x:x+w]
    xtrain.append(roi)
    ylabel.append(id_)

#print(ylabel)
#print(xtrain)

with open("labels.pickel", 'wb') as f:
 pickle.dump(labelid, f)

recog.train(xtrain, np.array(ylabel))
recog.save("trainner.yml")
