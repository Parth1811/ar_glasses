import cv2
import numpy as np
import pygame
import sys
from pygame.locals import *
from datetime import datetime

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

cap = cv2.VideoCapture('test.avi')
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
counter = 0
rect = True
frame_array = []

while rect:
   rect, frame = cap.read()
   frame_array.append(frame)
   counter += 1

frame_array = np.array(frame_array)
counter2 = 0
screen = pygame.display.set_mode([640,360])
clock = pygame.time.Clock()

print (datetime.now())
try:
    while True:
        if counter2 >= counter:
            break
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_LEFT:
                    counter2 -= 60
                    if counter2 < 0:
                        counter2 = 0
                    cap.set(2,counter2)
                if event.key == pygame.K_RIGHT:
                    counter2 += 60
                    if counter2 > counter:
                        counter2 = 0
                    cap.set(2,counter2)
                if event.key == pygame.K_DOWN:
                    sys.exit(0)


        screen.fill([255,255,255])
        #ret, frame = cap.read()
        frame1 = cv2.cvtColor(frame_array[counter2], cv2.COLOR_BGR2RGB)
        frame2 = np.rot90(frame1)
        frame2 = cv2.resize(frame2,(360,640))
        frame3 = pygame.surfarray.make_surface(frame2)
        screen.blit(frame3, (0,0))
        pygame.display.update()

        #print counter2
        counter2 += 1
        clock.tick(30)

except :
    pygame.quit()
    cv2.destroyAllWindows()


print (datetime.now())
