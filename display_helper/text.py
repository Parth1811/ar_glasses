import pygame

class Text():
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

    def is_draw(self, data, text_size, y ):
        display_image = pygame.image.load('img.jpeg')
        self.screen.blit(display_image, (0,0))
        basicfont = pygame.font.SysFont(None, text_size)
        text = basicfont.render(data, True, (255, 0, 0))
        textrect = text.get_rect()
        textrect.centerx = self.screen.get_rect().centerx
        textrect.centery = y
 
        self.screen.blit(text, textrect)
 
        pygame.display.update()
        pygame.display.flip()

    def animate():
        pass

    def sketch_message(self):
        image_display = pygame.image.load('images.png')
        screen.blit(image_display,(0,0))
        pygame.display.flip()
        pygame.display.update()
