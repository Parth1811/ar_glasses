#!/usr/bin/python


import pygame
import CONST as C

class Text():
    def __init__(self, screen_, label_, loc_x, loc_y, font_size = C.TEXT_FONT_SIZE,\
        color = C.WHITE, bg_color = None, font_style = None):
        self.screen = screen_
        self.label = label_
        self.x_location = loc_x
        self.y_location = loc_y
        self.size = font_size
        self.color = color
        self.bg_color = bg_color
        self.font_style = font_style


    def draw(self):
        basicfont = pygame.font.SysFont(self.font_style, self.size)
        text_surface = basicfont.render(self.label, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x_location , self.y_location) #self.screen.get_rect().centerx
        text_surface.set_alpha(128)
        self.screen.blit(text_surface, text_rect)

    def animate():
        pass

    def sketch_message(self):
        image_display = pygame.image.load('images.png')
        screen.blit(image_display,(0,0))
        pygame.display.flip()
        pygame.display.update()
