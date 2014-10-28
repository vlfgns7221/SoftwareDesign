# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 17:30:44 2014

@author: pilhunchoi
"""

import pygame, sys
from pygame.locals import *
import time

class YutModel:
    def __init__(self,color):
        self.yuts =list()
        for t in range(4):
            yut = Yut( color ,80,15, 30*t+200 ,90)
            self.yuts.append(yut)       

class HorseModel:
    def __init__(self,color,x,y):
        self.horses = list()
        horse = Horse(color,10,10,x,y)
        self.horses.append(horse)
                    
class Horse:
    def __init__(self,color,height,width,x,y):
        self.color = color
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        
class Yut:
    def __init__(self,color,height,width,x,y):
        self.color = color
        self.height = height    
        self.width = width
        self.x = x
        self.y = y

class  PyGameWindowView:
   def __init__(self,model1,model2,ymodel,screen):
        self.model1=model1
        self.model2=model2
        self.ymodel=ymodel
        self.screen = screen
        
   def drawback(self,image):
        self.screen.fill(pygame.Color(0,0,0))
        self.screen.blit(image,(0,0))
        pygame.display.update()

   def drawhorse(self):       
        for horse in self.model1.horses:
            pygame.draw.rect(self.screen, pygame.Color(horse.color[0],horse.color[1],horse.color[2]),pygame.Rect(horse.x,horse.y,horse.width,horse.height))
        for horse in self.model2.horses:
            pygame.draw.rect(self.screen, pygame.Color(horse.color[0],horse.color[1],horse.color[2]),pygame.Rect(horse.x,horse.y,horse.width,horse.height))        
        pygame.display.update()

   def drawyut(self):
        for yut in self.ymodel.yuts:
            pygame.draw.rect(self.screen, pygame.Color(yut.color[0],yut.color[1],yut.color[2]),pygame.Rect(yut.x,yut.y,yut.width,yut.height))
        pygame.display.update()       
      
class Yutaction:
    def __init__(self,ymodel):
        self.ymodel=ymodel

class horseaction:
    def __init__(self,model):
        self.model=model

if __name__ == '__main__':
    pygame.init()
    size = (800,800)
    ymodel=YutModel((100,100,100))
    model1=HorseModel((255,0,0),450,440)
    model2=HorseModel((0,255,50),430,440)
    
    screen = pygame.display.set_mode(size)
    view = PyGameWindowView(model1,model2,ymodel,screen)
    background = pygame.image.load('omokboard.jpg')
    view.drawback(background)        
    running= True;
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False;                
        view.drawhorse()
        view.drawyut()
        time.sleep(.001)
    
        
    pygame.quit()
