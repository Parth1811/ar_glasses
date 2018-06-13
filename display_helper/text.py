#!/usr/bin/python


import pygame
import CONST as C

class Text():
    def __init__(self, screen_, label_, loc_x, loc_y, font_size = C.TEXT_FONT_SIZE,\
        color_ = C.WHITE, bg_color_ = None):
        self.screen = screen_
        self.label = label_
        self.x_location = loc_x
        self.y_location = loc_y
        self.size = font_size
        self.color = color_
        self.bg_color = bg_color_



    def draw(self):
        basicfont = pygame.font.SysFont(None, self.size)
        text_surface = basicfont.render(self.label, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x_location , self.y_location) #self.screen.get_rect().centerx
        self.screen.blit(text_surface, text_rect)

    def animate():
        pass

    def sketch_message(self):
        image_display = pygame.image.load('images.png')
        screen.blit(image_display,(0,0))
        pygame.display.flip()
        pygame.display.update()
