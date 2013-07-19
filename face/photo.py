
import pygame
from tools.Tools import *

class Photo:
  def __init__(self):
    self.p, self.p_rect = load_image("photo.jpg",1)

  def draw(self,scr,n):
    scr.blit(self.p,(0,0))
    pygame.display.flip()
        
