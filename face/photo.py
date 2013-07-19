
import pygame
from tools.Tools import *

class Photo:
  def __init__(self):
    self.photo=[0,0,0]
    self.photo[0], self.p_rect = load_image("photo1.jpg",1)
    self.photo[1], self.p_rect = load_image("photo2.jpg",1)
    self.photo[2], self.p_rect = load_image("photo3.jpg",1)

  def draw(self,scr,n):
    index=int(n)
    scr.blit(self.photo[index],(0,0))
    pygame.display.flip()
        
