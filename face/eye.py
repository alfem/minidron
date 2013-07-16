
import pygame
import time
from tools.Tools import *

class Eye:
  def __init__(self,x,y):
    self.ball, self.ball_rect = load_image("eye.png",-1)
    self.pupil, self.pupil_rect = load_image("pupil.png",-1)
    self.eyelid, self.eyelid_rect = load_image("eyelid.png",1)
    self.eyebrown, self.eyebrown_rect = load_image("eyebrown.png",1)
    self.pupil_x=x-self.pupil_rect.width/2
    self.pupil_y=y-self.pupil_rect.height/2
    self.x=x-self.ball_rect.width/2
    self.y=y-self.ball_rect.height/2
    self.eyebrown_x=self.x
    self.eyebrown_y=self.y-10
    self.status="open"

  def draw(self,scr,status="open"):
    self.status=status
    scr.blit(self.ball,(self.x,self.y))
    if self.status=="left":
      pupil_ix=-60
    elif self.status=="right":
      pupil_ix=60
    else:
      pupil_ix=0
    scr.blit(self.pupil,(self.pupil_x+pupil_ix,self.pupil_y))
    if self.status=="close":
      scr.blit(self.eyelid,(self.x,self.y))
    
    if self.status=="brownleft":
      eyebrown_iy=-15
      eyebrown=pygame.transform.rotate(self.eyebrown,10)
    elif self.status=="brownright":
      eyebrown_iy=-15
      eyebrown=pygame.transform.rotate(self.eyebrown,-10)
    else:
      eyebrown_iy=0
      eyebrown=self.eyebrown 

    if self.status != "up":
      scr.blit(eyebrown,(self.eyebrown_x,self.eyebrown_y+eyebrown_iy))

    pygame.display.flip()

  def blink(self,scr):
    status=self.status
    self.draw(scr,"close")
    time.sleep(0.10)
    self.draw(scr,status)

  def rotate_eyebrown(self,scr):
    self.eyebrown=pygame.transform.rotate(self.eyebrown,20)

