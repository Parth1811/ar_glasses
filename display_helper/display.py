#!/usr/bin/python

from datetime import datetime
import pygame
import cv2
import numpy as np
import os

import text
import camera_driver

FULL_PACKAGE_PATH = os.path.expanduser("~/ar_glasses/display_helper")

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 30

#MODE 1 is for graphic display and MODE 2  is for camera display
MODE = 1

def init_screen():
    pygame.init()
    display_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("GRAPHIC DISPLAY")
    clock = pygame.time.Clock()
    return display_screen,clock

def display_image(screen, image_path):
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, screen.get_size())
    pygame.transform.scale(image, screen.get_size())
    screen.blit(image, (0,0))

def mode_transition (screen, image_path, duration = 0.5):
    global MODE
    screen_width , screen_height = screen.get_size()
    if MODE == 1:
        start_x = screen_width/2
        start_y = screen_height/2
        end_x , end_y = 0,0
        MODE = 2
    elif MODE == 2:
        end_x = screen_width/2
        end_y = screen_height/2
        start_x , start_y = 0,0
        MODE = 1
    start_time = datetime.now()
    image = pygame.image.load(image_path)
    transition = True
    while transition:
        dt = (datetime.now()-start_time).total_seconds()
        if (dt < duration) and (dt > 0.01):
            screen.fill((0,0,0))
            shift_x = (start_x - end_x)*dt/duration
            shift_y = (start_y - end_y)*dt/duration
            window = pygame.surface.Surface((screen_width - start_x + shift_x , screen_height - start_y + shift_y))
            image = pygame.transform.scale(image, window.get_size())
            window.blit(image, (0,0))
            screen.blit(window, (start_x - shift_x, start_y - shift_y))
            pygame.display.update()
        elif dt > duration:
            transition = False
            break
        else :
            continue


def run(data):
    screen, clock = init_screen()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mode_transition(screen, FULL_PACKAGE_PATH + '/resources/gui.jpg')
                if event.key == pygame.K_DOWN:
                    running = False
            if event.type == pygame.QUIT:
                running = False

        if MODE == 2:
            #if data["is_face_present"] == True:
            display_image(screen, FULL_PACKAGE_PATH + '/resources/gui.jpg')
            text.Text(screen, "Saavi", SCREEN_WIDTH/2, 200, font_size = 72).draw()
        elif MODE == 1:
            video_feed = camera_driver.cam_read(data["camera"])
            pygame_frame = convert_cvimage(video_feed['frame'])
            screen.blit(pygame_frame, (0,0))
            window = pygame.surface.Surface((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            #window.fill((0,0,0), rect= [SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH/2, SCREEN_HEIGHT/2])
            display_image(window, FULL_PACKAGE_PATH + '/resources/gui.jpg')
            window.set_alpha(180)
            screen.blit(window, (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            #text.Text(screen, "Saavi", 480, 300, font_size = 72).draw()
            try:
                text.Text(screen,  data['face_info']['full name'], 480, 300, font_size = 72).draw()
                #screen.fill((0,0,0), rect= [data["location"]["x"],data["location"]["y"],data["location"]["w"],data["location"]["h"]])

            except:
                pass


        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

def convert_cvimage(frame):
    frame = np.rot90(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame,(SCREEN_HEIGHT,SCREEN_WIDTH))
    pygame_frame = pygame.surfarray.make_surface(frame)
    return pygame_frame

if __name__ == "__main__":
    data = dict()
    data["camera"] = cv2.VideoCapture(0)
    data["is_face_present"] = True
    data["face_info"] = {"full name": "Partho"}

    run (data)
