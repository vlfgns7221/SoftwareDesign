# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 11:46:50 2014

@author: pilhunchoi
"""

import pygame, sys
from pygame.locals import *
import time


class StoneModel:
    def __init__(self,color):
        self.stones = list()
        for x in range(53,457,31):
            for y in range(53,457,31):
                stone = Stone(color,x,y,2)
                self.stones.append(stone)
                    
class Stone:
    def __init__(self,color,x,y,stone_color):
        self.color = color
        self.x = x
        self.y = y
        self.stone_color= stone_color

class  PyGameWindowView:
    def __init__(self,model,screen):
        self.model=model
        self.screen = screen
        
    def draw_background(self,image):
        self.screen.fill(pygame.Color(0,0,0))
        self.screen.blit(image,(0,0))
        pygame.display.update()
        
    def draw_startbutton(self,image):
        self.screen.blit(image,(500,0))
        pygame.display.update()
        
    def draw_stone(self,model,screen,k,stone_color):       
        stone=model.stones[k]
        if stone_color == 0:
            stone.color = (255,255,255)
            stone.stone_color=stone_color
        elif stone_color ==1:
            stone.color = (0,0,0)            
            stone.stone_color=stone_color        
        pygame.draw.circle(self.screen,(stone.color[0],stone.color[1],stone.color[2]),(stone.x,stone.y),13)
        pygame.display.update()
        
    def draw_win_message(self,stone_color):
        if stone_color==0:
            self.screen.blit(pygame.image.load('white.png'),(200,200))
        elif stone_color==1:
            self.screen.blit(pygame.image.load('black.png'),(200,200))
        pygame.display.update()
    
    def draw_restart_button(self):
        self.screen.blit(pygame.image.load('restartbutton.jpg'),(500,0))
        pygame.display.update()

class Mouse_click_event:
    def __init__(self,model,board,screen,view,checkwin):
        self.model=model
        self.screen = screen
        self.view=view
        self.checkwin=checkwin
        self.board=board
        
    def handle_mouse_event(self,event,turn,stone_color):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            posx=int(round((pos[0]-25.5)/31.0))-1;
            posy=int(round((pos[1]-25.5)/31.0))-1;
            k=14*posx+posy
            if posx >= 0 and posx < 14 and posy >= 0 and posy < 14 and self.board.check_existance(self.model,k):
                self.view.draw_stone(self.model,self.screen,k,stone_color)
                self.checkwin.determine(self.model,k,stone_color)
                return turn.chagne_stone_color(stone_color)
            else:
                return stone_color

class Change_Turn:
    def chagne_stone_color(self, stone_color):
        if stone_color==0:
            return 1
        elif stone_color==1:
            return 0


class Board_situation:
    def __init__(self,model):
        self.model=model    
        
    def check_existance(self,model,k):
        if model.stones[k].stone_color == 0 or model.stones[k].stone_color == 1:
            return False
        else:
            return True       
            
class Determine_winner:
    def __init__(self,model,view):
        self.model=model
        self.view=view
    
    def determine(self,model,k,stone_color):
        count_horizontal_axis=1;
        count_vertical_axis=1;
        count_upper_diagonal=1;
        count_Lower_diagonal=1;
        coordinate_decreasing_vertical_axis=k;
        coordinate_increasing_vertical_axis=k;
        coordinate_decreasing_horizontal_axis=k;
        coordinate_increasing_horizontal_axis=k;
        coordinate_decreasing_upper_diagonal=k;
        coordinate_increasing_upper_diagonal=k;
        coordinate_decreasing_lower_diagonal=k;
        coordinate_increasing_lower_diagonal=k;
        check_run = True                
        while check_run:
            if coordinate_decreasing_vertical_axis>=14 and model.stones[coordinate_decreasing_vertical_axis-14].stone_color == stone_color:
               count_horizontal_axis+=1;
               coordinate_decreasing_vertical_axis -= 14;
            else:
               check_run = False
        check_run = True
        while check_run:
            if coordinate_increasing_vertical_axis<=181 and model.stones[coordinate_increasing_vertical_axis+14].stone_color == stone_color:
                count_horizontal_axis+=1;
                coordinate_increasing_vertical_axis += 14;
            else:
                check_run=False
        check_run = True
        while check_run:
            if coordinate_decreasing_horizontal_axis % 14 > 0 and model.stones[coordinate_decreasing_horizontal_axis-1].stone_color == stone_color:
                count_vertical_axis+=1;
                coordinate_decreasing_horizontal_axis -= 1;
            else:
                check_run = False
        check_run = True
        while check_run:
            if coordinate_increasing_horizontal_axis % 14 < 13 and model.stones[coordinate_increasing_horizontal_axis+1].stone_color == stone_color:
                count_vertical_axis+=1;
                coordinate_increasing_horizontal_axis += 1;
            else:
                check_run = False
        check_run = True
        while check_run:
            if coordinate_decreasing_upper_diagonal>=14 and coordinate_decreasing_upper_diagonal % 14>0 and model.stones[coordinate_decreasing_upper_diagonal-15].stone_color==stone_color:
                count_upper_diagonal+=1;
                coordinate_decreasing_upper_diagonal-=15;
            else:
                check_run=False
        check_run = True
        while check_run:
            if coordinate_increasing_upper_diagonal<=181 and coordinate_decreasing_upper_diagonal % 14<13 and model.stones[coordinate_increasing_upper_diagonal+15].stone_color==stone_color:
                count_upper_diagonal+=1;
                coordinate_increasing_upper_diagonal+=15;
            else:
                check_run=False 
        check_run = True
        while check_run:
           if coordinate_increasing_lower_diagonal>=14 and coordinate_decreasing_lower_diagonal % 14<13 and model.stones[coordinate_decreasing_lower_diagonal-13].stone_color==stone_color:
               count_Lower_diagonal+=1;
               coordinate_decreasing_lower_diagonal-=13;
           else:
               check_run=False 
        check_run = True
        while check_run:
           if coordinate_increasing_lower_diagonal<=181 and coordinate_decreasing_lower_diagonal % 14>0 and model.stones[coordinate_increasing_lower_diagonal+13].stone_color==stone_color:
               count_Lower_diagonal+=1;
               coordinate_increasing_lower_diagonal+=13;
           else:
               check_run=False 
        if count_horizontal_axis ==5 or count_vertical_axis ==5 or count_Lower_diagonal ==5 or count_upper_diagonal ==5 :
            self.view.draw_win_message(stone_color)
            
               
class Start_Button_Checker:
    def play_start_button(self,event):
        if event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] > 500 and pos[0] < 700 and pos[1] > 0 and pos[1] < 100:
                    return True
                    
    def play_restart_button(self,event):
        if event.type == MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if pos[0] > 500 and pos[0] < 700 and pos[1] > 0 and pos[1] < 100:
                pygame.quit()
                main()
                return False
            else:
                return True
                
def main():
    pygame.init()
    size = (700,500)    
    model=StoneModel((127,127,127))
    startbuttonchecker=Start_Button_Checker()
    board=Board_situation(model)
    screen = pygame.display.set_mode(size)
    view = PyGameWindowView(model,screen)
    background = pygame.image.load('omokboard.jpg')
    startbutton = pygame.image.load('startbutton.jpg')
    view.draw_background(background)
    view.draw_startbutton(startbutton)
    checkwin=Determine_winner(model,view)
    controller=Mouse_click_event(model,board,screen,view,checkwin)    
    turn=Change_Turn();
    stone_color=turn.chagne_stone_color(0)  # Black Start
    check_run_starter = True
    while check_run_starter:
        for event in pygame.event.get():
            if event.type == QUIT:
                check_run = False
                check_run_starter= False
            if event.type == MOUSEBUTTONUP:
                check_run=startbuttonchecker.play_start_button(event)
                view.draw_restart_button()
                while check_run:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            check_run = False
                            check_run_starter= False
                        if event.type == MOUSEBUTTONUP:
                            if startbuttonchecker.play_restart_button(event):
                                stone_color=controller.handle_mouse_event(event,turn,stone_color)                
                time.sleep(.001)
    pygame.quit()

if __name__ == '__main__':
    main()
    
file = 'some.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()