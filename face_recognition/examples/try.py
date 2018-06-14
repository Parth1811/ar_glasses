import numpy as py
import cv2
import pickle

face_cascade=cv2.CascadeClassifier('/home/saavi/Downloads/opencvtut/opencv-3.4.1/data/haarcascades/haarcascade_frontalface_default.xml')
#eye_cascade=cv2.CascadeClassifier('/home/saavi/Downloads/opencvtut/opencv-3.4.1/data/haarcascades/haarcascade_eye.xml')
#smile_cascade=cv2.CascadeClassifier('/home/saavi/Downloads/opencvtut/opencv-3.4.1/data/haarcascades/haarcascade_smile.xml')


recog=cv2.face.LBPHFaceRecognizer_create()
recog.read("trainner.yml")

labels={"person_name":1}
with open("labels.pickel", 'rb') as f:
 og_labels=pickle.load(f)
 labels={v:k for k,v in og_labels.items()}

cap=cv2.VideoCapture(0)

while(True):
	ret,frame=cap.read()
	gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces=face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
	for (x,y,w,h) in faces:
		#print x,y,w,h
		roi_gray=gray[y:y+h,x:x+h]
		roi_c=frame[y:y+h,x:x+h]
		id_, conf=recog.predict(roi_gray)
		if conf>=45:# and conf<=85:
			print(id_)
			print(labels[id_])
			font=cv2.FONT_HERSHEY_SIMPLEX
			name= labels[id_]
			cv2.putText(frame,name, (x,y), font, 1,(0,100,200), 2, cv2.LINE_AA)

		ing="me>3.jpg"
		cv2.imwrite(ing,roi_c)
		cv2.rectangle(frame,(x,y),(x+w,y+h),(200,0,100),2)
		#eyes= eye_cascade.detectMultiScale(roi_gray)
		#for (ex,ey,ew,eh) in eyes:
		#	cv2.rectangle(frame,(ex,ey),(ex+ew,ey+eh),(200,0,100),2)
		#subit= smile_cascade.detectMultiScale(roi_gray)
		#for (sx,sy,sw,sh) in subit:
		#	cv2.rectangle(frame,(sx,sy),(sx+sw,sy+sh),(200,0,100),2)
		
	cv2.imshow('frame',frame)
	if cv2.waitKey(20) & 0xFF== ord('q'):
		break

cap.release()
cv2.destroyAllWindows()  

