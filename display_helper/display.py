#!/usr/bin/python

import pygame
import cv2
import numpy as np

import text
import camera_driver

SCREEN_WIDTH=640
SCREEN_HEIGHT=480

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


#MODE[0] is for graphic display and MODE[1] is for camera display
MODE=[1,2]

#default mode set for graphic display
I = 1

def run(data):
    screen, clock = init_screen()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running = False


        if MODE[I] == 1:
            if data["is_face_present"] == True:
                display_image(screen, 'img.jpeg')
                #text.Text(screen, "Saavi", SCREEN_WIDTH/2, 200, font_size = 72).draw()
                text.Text(screen, data["face_info"]["full name"], SCREEN_WIDTH/2, 150).draw()
        else :
            video_feed = camera_driver.cam_read(data["camera"])
            pygame_frame = convert_cvimage(video_feed['frame'])
            screen.blit(pygame_frame, (0,0))
            window = pygame.surface.Surface((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            #window.fill((0,0,0), rect= [SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH/2, SCREEN_HEIGHT/2])
            display_image(window, 'resources/gui.jpg')
            window.set_alpha(200)
            screen.blit(window, (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            text.Text(screen, "Saavi", 480, 300, font_size = 72).draw()

        pygame.display.update()

    pygame.quit()
    quit()

def convert_cvimage(frame):
    frame = np.rot90(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame,(SCREEN_HEIGHT,SCREEN_WIDTH))
    pygame_frame = pygame.surfarray.make_surface(frame)
    return pygame_frame

if __name__ == "__main__":
    data = ["saavi", "machaxx"]
    run (True, data)
