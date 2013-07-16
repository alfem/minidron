
import pygame
from tools.Tools import *

class Mouth:
  def __init__(self,x,y):
    self.base, self.base_rect = load_image("mouth_base.png",1)
    self.smile, self.smile_rect = load_image("mouth_smile.png",1)
    self.sad, self.sad_rect = load_image("mouth_sad.png",1)
    self.a, self.a_rect = load_image("mouth_a.png",1)
    self.e, self.e_rect = load_image("mouth_e.png",1)
    self.i, self.i_rect = load_image("mouth_i.png",1)
    self.o, self.o_rect = load_image("mouth_o.png",1)
    self.u, self.u_rect = load_image("mouth_u.png",1)
    self.x=x-self.base_rect.width/2
    self.y=y-self.base_rect.height/2
    self.status="base"

  def draw(self,scr,status="base"):
    self.status=status
    if self.status=="base":
      scr.blit(self.base,(self.x,self.y))
    elif self.status=="sad":
      scr.blit(self.sad,(self.x,self.y))
    elif self.status=="open":
      scr.blit(self.open,(self.x,self.y))
    elif self.status=="a":
      scr.blit(self.a,(self.x,self.y))
    elif self.status=="e":
      scr.blit(self.e,(self.x,self.y))
    elif self.status=="i":
      scr.blit(self.i,(self.x,self.y))
    elif self.status=="o":
      scr.blit(self.o,(self.x,self.y))
    elif self.status=="u":
      scr.blit(self.u,(self.x,self.y))
    else:
      scr.blit(self.smile,(self.x,self.y))
    pygame.display.flip()
        
