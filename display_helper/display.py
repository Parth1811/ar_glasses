import pygame 
import cv2
import text
#from ..drivers import camera_driver

SCREEN_WIDTH=640
SCREEN_HEIGHT=480

def init_screen():
 pygame.init()
 display_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
 pygame.display.set_caption("GRAPHIC DISPLAY")
 clock = pygame.time.Clock()
 return display_screen,clock

MODE=[1,2] #MODE[0] is for graphic display and MODE[1] is for camera display  
I = 0                          #default mode set for graphic display

def run(is_face_present, data):
 display, clock = init_screen()
 running = True
 text_display = text.Text(display, SCREEN_WIDTH, SCREEN_HEIGHT)
 while running:
  for event in pygame.event.get():
   if event.type==pygame.QUIT:
    running = False
  # frame = camera_driver.cam_read()
   
   if MODE[I] == 1:
    if is_face_present == True: 
      text_display.is_draw(data[0], 48, 50)
      text_display.is_draw(data[1], 36, 150)
     
 pygame.quit()
 quit()

def convert_cvimage(frame):
 frame=cv2.resize(frame,(640,480))
 pygame_display = pygame.surfarray.make_surface(frame)
 return pygame_display

if __name__ == "__main__":
 data = ["saavi", "machaxx"]
 run (True, data)




  
