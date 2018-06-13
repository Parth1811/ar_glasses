import pygame, sys
from pygame.locals import *
 
pygame.init()
 
pygame.display.set_caption('font example')
size = [322,156]
screen = pygame.display.set_mode(size)
 
clock = pygame.time.Clock()
background_image = pygame.image.load('img.jpeg')
pygame.display.update()

screen.blit(background_image,(0,0))

basicfont = pygame.font.SysFont(None, 48)
text = basicfont.render('Hello World!', True, (255, 0, 0))
textrect = text.get_rect()
textrect.centerx = screen.get_rect().centerx
textrect.centery = 50
 

screen.blit(text, textrect)

pygame.display.update()
basicfont = pygame.font.SysFont(None, 48)
text = basicfont.render('Hello World!', True, (255, 0, 0))
textrect = text.get_rect()
textrect.centerx = screen.get_rect().centerx
textrect.centery = 100
 

screen.blit(text, textrect)

pygame.display.update()
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
    clock.tick(20)
