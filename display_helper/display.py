#!/usr/bin/python

from datetime import datetime
import pygame
import cv2
import numpy as np
import os

import text
import camera_driver
import CONST as C


FULL_PACKAGE_PATH = os.path.expanduser("~/ar_glasses/display_helper")

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 30
PADDING_4_M1 = 20
ZOOM_FACTOR = 1

#MODE 1 is for graphic display and MODE 2  is for camera display
MODE = 1

def init_screen(fullscreen):
    pygame.init()
    if fullscreen:
        display_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        display_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("GRAPHIC DISPLAY")
    clock = pygame.time.Clock()
    return display_screen,clock

def display_image(screen, image_path):
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, screen.get_size())
    pygame.transform.scale(image, screen.get_size())
    screen.blit(image, (0,0))

def mode_transition (screen, image_path, duration = 0.5, set_mode = False):
    global MODE
    screen_width , screen_height = screen.get_size()
    if set_mode:
        if set_mode == 1:
            MODE = 2
        if set_mode == 2:
            MODE = 1
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

def zoom(increase = False, decrease = False):
    global ZOOM_FACTOR
    if increase:
        ZOOM_FACTOR += 0.2
    if decrease:
        ZOOM_FACTOR -= 0.2
    if ZOOM_FACTOR > 2:
        ZOOM_FACTOR = 2
    if ZOOM_FACTOR < 1:
        ZOOM_FACTOR = 1


def run(data, fullscreen = False):
    screen, clock = init_screen(fullscreen)
    running = True
    start_trip = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_m:
                    mode_transition(screen, FULL_PACKAGE_PATH + '/resources/gui.jpg')
                if event.key == pygame.K_DOWN:
                    running = False
                if event.key == pygame.K_EQUALS:
                    zoom(increase = True)
                if event.key == pygame.K_MINUS:
                    zoom(decrease = True)
            if event.type == pygame.QUIT:
                running = False

        if data["first_run"]:
            screen.fill(C.WHITE)
            time_diff = abs(datetime.now().microsecond/100000-5)/float(5)
            color = (255*time_diff, 255*time_diff, 255*time_diff)
            text.Text(screen, "Training! Be patient :)", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, font_size = 35 ,font_style= "tlwg typist", color=color).draw()
        else:
            if not start_trip:
                mode_transition(screen, FULL_PACKAGE_PATH + '/resources/gui.jpg', set_mode = 1)
                start_trip = True

            if MODE == 2:
                display_image(screen, FULL_PACKAGE_PATH + '/resources/gui.jpg')
                text_y = 200
                if 'face_info' in data:
                    for face in data["face_info"]:
                        text.Text(screen, face['full name'], SCREEN_WIDTH/2, text_y, font_size = 72, color=C.GREEN).draw()
                        text_y += 70
            elif MODE == 1:
                text_x, text_y = (3*SCREEN_WIDTH/4)-PADDING_4_M1/4, (3*SCREEN_HEIGHT/4)-PADDING_4_M1
                #video_feed = camera_driver.cam_read(data["camera"])
                pygame_frame = convert_cvimage(data['frame'])
                blit_x , blit_y = screen.get_size()[0]-pygame_frame.get_size()[0], screen.get_size()[1]-pygame_frame.get_size()[1]
                screen.blit(pygame_frame, (blit_x/2,blit_y/2))
                window = pygame.surface.Surface((SCREEN_WIDTH/2-PADDING_4_M1,SCREEN_HEIGHT/2-PADDING_4_M1))
                display_image(window, FULL_PACKAGE_PATH + '/resources/gui.jpg')
                window.set_alpha(180)
                screen.blit(window, (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
                if 'face_info' in data:
                    for face in data["face_info"]:
                        text.Text(screen,  face['full name'], text_x, text_y, font_size = 60).draw()
                        text_y += 50



        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

def convert_cvimage(frame):
    frame = np.rot90(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame,(int(SCREEN_HEIGHT*ZOOM_FACTOR),int(SCREEN_WIDTH*ZOOM_FACTOR)))
    pygame_frame = pygame.surfarray.make_surface(frame)
    return pygame_frame


if __name__ == "__main__":
    data = dict()
    data["camera"] = cv2.VideoCapture(0)
    data["is_face_present"] = True
    data["face_info"] = [{"full name": "Partho"}, {"full name": "Saavi"}]

    run (data)
