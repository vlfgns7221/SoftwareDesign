# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 20:28:34 2014

@author: pilhunchoi
"""

import json
import httplib, urllib
import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
import time
import math
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

IP="10.7.88.88"
def sign_up(user_name):
    params = urllib.urlencode({'user_id': user_name})
    conn = httplib.HTTPConnection(IP,9000)
    conn.request("POST", "/sign_up", params, headers)
    response = conn.getresponse()
    check_signup = response.read()
    conn.close()
    if check_signup == user_name:
        return True
    else:
        return False
    
def login(user_name):
    params = urllib.urlencode({'user_id': user_name})
    conn = httplib.HTTPConnection(IP,9000)
    conn.request("POST", "/login", params, headers)
    response = conn.getresponse()
    login_avail = response.read()
    conn.close()
    return login_avail
    
def startgame(user_name):
    params = urllib.urlencode({'user_id': user_name})
    conn = httplib.HTTPConnection(IP,9000)
    conn.request("POST", "/startgame", params, headers)
    response = conn.getresponse()
    game_id = response.read()
    conn.close()
    return game_id
    
def check_second_user(game_id):
    params = urllib.urlencode({'game_id': game_id})
    conn = httplib.HTTPConnection(IP,9000)
    conn.request("POST","/checkseconduser",params,headers)
    response = conn.getresponse()
    user_id_2 =response.read()
    conn.close()   
    return user_id_2
    
def send_action(game_id,turn,posx,angle,power,direction):
    params = urllib.urlencode({'game_id': game_id,'turn':turn,'posx':posx,'angle':angle,'power':power,'direction':direction})
    conn = httplib.HTTPConnection(IP,9000)
    conn.request("POST", "/action", params, headers)
    response = conn.getresponse()
    game_id = response.read()
    conn.close()
    
""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""   Tank   model   """""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""

class TankModel:
    def __init__(self):
        self.tanks = list()
        self.tank1=Tank(30,420,0)
        self.tank2=Tank(600,420,0)
        self.tanks.append(self.tank1)
        self.tanks.append(self.tank2)
        self.tank2.canon_angle=180;
        self.tank2.canon_direction =1;
                
class Tank:
    def __init__(self,x,y,canon_angle=0,power=0,canon_direction=0, hp = 1000):
        self.x = x
        self.y = y
        self.canon_angle = canon_angle
        self.power=power
        self.canon_direction = canon_direction
        self.hp = hp

""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""   Display part   """""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""        
        
class  PyGameWindowView:
    def __init__(self,model,screen,background_image):
        self.model = model      # list of stones
        self.screen = screen    # game window
        self.background_image=background_image
    #Fill Background Black
    def draw_background(self):
        self.screen.blit(self.background_image,(0,0))
        pygame.display.update()
    #Start Button     
    def draw_startbutton(self,image):
        self.screen.blit(image,(0,0))
        pygame.display.update()
    
    def draw_tank(self,model,screen):
        self.screen.blit(self.background_image,(0,0))
        img_tank1 = pygame.image.load('tank1.png')
        img_tank2 = pygame.image.load('tank2.png')
        if model.tank1.canon_direction == 0:
            screen.blit(img_tank1,(model.tank1.x, model.tank1.y))
        elif model.tank1.canon_direction == 1:
            screen.blit(img_tank2,(model.tank1.x, model.tank1.y))
       
        if model.tank2.canon_direction == 0:
            screen.blit(img_tank1,(model.tank2.x, model.tank2.y))
        elif model.tank2.canon_direction == 1:
            screen.blit(img_tank2,(model.tank2.x, model.tank2.y))
        pygame.display.update()

    def draw_angle(self,model,screen,user_turn):
        if user_turn == 1: 
            pos_tank=(model.tank1.x+50,model.tank1.y+30)
            angle=model.tank1.canon_angle
        elif user_turn == 2:
            pos_tank=(model.tank2.x+50,model.tank2.y+30)
            angle=model.tank2.canon_angle            
        vec_arrow=(pos_tank[0]+70*math.cos(math.radians(angle)),pos_tank[1]+70*math.sin(math.radians(angle)))
        pygame.draw.line( screen, (255,255,0), pos_tank, vec_arrow,2 )
        pygame.display.update()        
        
    def draw_power_gauge_bar(self,model,screen):
        pygame.draw.rect(screen,(255,255,255),Rect( (200,50),(600,20) ),1 )
        pygame.display.update()

    def draw_power_gauge(self,model,screen,user_turn):
        if user_turn == 1: 
            pygame.draw.rect(screen,(255,255,0),Rect( (200,50),(model.tank1.power,20) ))
        elif user_turn ==2:
            pygame.draw.rect(screen,(255,255,0),Rect( (200,50),(model.tank2.power,20) ))    
        pygame.display.update()
        
    def draw_win_message(self,stone_color):
        pygame.display.update()
    #Restart Button
    def draw_restart_button(self):
        self.screen.blit(pygame.image.load('restartbutton.jpg'),(500,0))
        pygame.display.update()
        
    def draw_missle(self,model,screen,missle,x,y):
        self.draw_tank(model,screen)
        screen.blit( missle, (x, y) )
        pygame.display.update()
        
    def draw_explosion(self,model,screen,explosion,x,y):
        self.draw_tank(model,screen)
        screen.blit( explosion, (x, y) )
        pygame.display.update()
        time.sleep(0.5)        
        
""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""   Fire  action   """""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""
class FireCanonMissle:
    def __init__(self,model,screen,view):
        self.model = model
        self.screen = screen
        self.view = view
        self.missle1 = pygame.image.load('mis1.png')
        self.missle2 = pygame.image.load('mis2.png')
        self.explosion = pygame.image.load('explosion.png')
        
    def missle_action(self,model,screen,turn):
        if turn == 1:
            xzero = model.tank1.x
            yzero = model.tank1.y
            angle =model.tank1.canon_angle
            power = model.tank1.power
            direction = model.tank1.canon_direction
        elif turn == 2:
            xzero = model.tank2.x
            yzero = model.tank2.y
            angle =model.tank2.canon_angle
            power = model.tank2.power
            direction = model.tank2.canon_direction
            
        angle = math.radians(-angle)
        power = power / 6
        if direction == 0:
            missle = self.missle1
        elif direction == 1:
            missle = self.missle2
        y = yzero # init
        x = xzero # init
        t = 0
        while y <= yzero :
            x = round(xzero + t * power * math.cos(angle))
            y = round(yzero - t * power * math.sin(angle) + 0.5 * 9.81 * t ** 2)
            view.draw_missle(model,screen,missle,int(x),int(y))
            t = t + 1
            time.sleep(0.1)
        view.draw_tank(model,screen) 
        view.draw_angle(model,screen,turn)
        view.draw_power_gauge_bar(model,screen)
        view.draw_explosion(model,screen,self.explosion,x,y)
        self.damage_cal(model,x,y)
        
    def damage_cal(self,model,x,y):
        dis_tank1=abs( math.sqrt( (x - model.tank1.x)**2 + (y - model.tank1.y)**2  ) )
        dis_tank2=abs( math.sqrt( (x - model.tank2.x)**2 + (y - model.tank2.y)**2  ) )
        if dis_tank1 < 60:
            model.tank1.hp = model.tank1.hp - 300 * (1.0 - dis_tank1/60.0)
        if dis_tank2 < 60:
            model.tank2.hp = model.tank2.hp - 300 * (1.0 - dis_tank2/60.0)    
             
""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""   Tank  action   """""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""
class PyGameKeyboardController:
    def __init__(self,model,screen,view,game_id,turnover,missle):
        self.model = model
        self.screen = screen
        self.view = view
        self.game_id = game_id
        self.turnover = turnover
        self.user_turn = self.turnover.turn
        self.missle = missle

    def keyboard_event(self,event):
        return_value = True
        pressed_move = pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_LEFT]
        pressed_angle = pygame.key.get_pressed()[K_UP] or pygame.key.get_pressed()[K_DOWN]
        pressed_gauge = pygame.key.get_pressed()[K_SPACE]
        if self.user_turn == 1:
            if pressed_move:
                while pressed_move:
                    pygame.event.get()
                    if event.key == pygame.K_RIGHT:
                        self.model.tank1.canon_direction=0
                        self.model.tank1.x+=1
                    elif event.key == pygame.K_LEFT:
                        self.model.tank1.canon_direction=1
                        self.model.tank1.x-=1
                    self.view.draw_tank(self.model,self.screen)
                    self.view.draw_angle(self.model,self.screen,self.user_turn)
                    pressed_move = pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_LEFT]
                    send_action(self.game_id, self.user_turn ,self.model.tank1.x,self.model.tank1.canon_angle,self.model.tank1.power,self.model.tank1.canon_direction)
                    time.sleep(0.001)
                    
            elif pressed_angle:
                while pressed_angle:
                    pygame.event.get()
                    if self.model.tank1.canon_direction == 0:
                        if event.key == pygame.K_UP:
                            self.model.tank1.canon_angle-=1
                        elif event.key == pygame.K_DOWN:
                            self.model.tank1.canon_angle+=1
                    elif self.model.tank1.canon_direction == 1:
                        if event.key == pygame.K_UP:
                            self.model.tank1.canon_angle+=1
                        elif event.key == pygame.K_DOWN:
                            self.model.tank1.canon_angle-=1

                    self.view.draw_tank(self.model,self.screen)
                    self.view.draw_angle(self.model,self.screen,self.user_turn)
                    self.view.draw_power_gauge_bar(self.model,self.screen)
                    pressed_angle = pygame.key.get_pressed()[K_UP] or pygame.key.get_pressed()[K_DOWN]
                    send_action(self.game_id, self.user_turn ,self.model.tank1.x,self.model.tank1.canon_angle,self.model.tank1.power,self.model.tank1.canon_direction)
                    time.sleep(0.01)
                    
            elif pressed_gauge:
                self.model.tank1.power=0
                self.view.draw_power_gauge_bar(self.model,self.screen)
                while pressed_gauge:
                    pygame.event.get()
                    self.model.tank1.power+=1
                    if model.tank1.power > 600:
                        model.tank1.power=1
                        self.view.draw_tank(self.model,self.screen)
                        self.view.draw_power_gauge_bar(self.model,self.screen)
                    self.view.draw_power_gauge(self.model,self.screen,self.user_turn)
                    pressed_gauge = pygame.key.get_pressed()[K_SPACE]
                    time.sleep(0.005)
                send_action(self.game_id, self.user_turn ,self.model.tank1.x,self.model.tank1.canon_angle,self.model.tank1.power,self.model.tank1.canon_direction)
                missle.missle_action(self.model,self.screen,self.user_turn)
                return_value=False
                self.model.tank1.power=0
                
        elif self.user_turn == 2:
            if pressed_move:
                while pressed_move:
                    pygame.event.get()
                    if event.key == pygame.K_RIGHT:
                        self.model.tank2.canon_direction=0
                        self.model.tank2.x+=1
                    elif event.key == pygame.K_LEFT:
                        self.model.tank2.canon_direction=1
                        self.model.tank2.x-=1
                    self.view.draw_tank(self.model,self.screen)
                    self.view.draw_angle(self.model,self.screen,self.user_turn)
                    pressed_move = pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_LEFT]
                    send_action(self.game_id, self.user_turn ,self.model.tank2.x,self.model.tank2.canon_angle,self.model.tank2.power,self.model.tank2.canon_direction)
                    time.sleep(0.001)
                    
            elif pressed_angle:
                while pressed_angle:
                    pygame.event.get()
                    if self.model.tank2.canon_direction == 0:
                        if event.key == pygame.K_UP:
                            self.model.tank2.canon_angle-=1
                        elif event.key == pygame.K_DOWN:
                            self.model.tank2.canon_angle+=1
                    elif self.model.tank2.canon_direction == 1:
                        if event.key == pygame.K_UP:
                            self.model.tank2.canon_angle+=1
                        elif event.key == pygame.K_DOWN:
                            self.model.tank2.canon_angle-=1                    
                    self.view.draw_tank(self.model,self.screen)
                    self.view.draw_angle(self.model,self.screen,self.user_turn)
                    self.view.draw_power_gauge_bar(self.model, self.screen)
                    pressed_angle = pygame.key.get_pressed()[K_UP] or pygame.key.get_pressed()[K_DOWN]
                    send_action(self.game_id, self.user_turn ,self.model.tank2.x,self.model.tank2.canon_angle,self.model.tank2.power,self.model.tank2.canon_direction)
                    time.sleep(0.01)
                    
            elif pressed_gauge:
                self.model.tank2.power=0
                self.view.draw_power_gauge_bar(self.model,self.screen)
                while pressed_gauge:
                    pygame.event.get()
                    self.model.tank2.power+=1
                    if model.tank2.power > 600:
                        model.tank2.power=1
                        self.view.draw_tank(self.model,self.screen)
                        self.view.draw_power_gauge_bar(self.model,self.screen)
                    self.view.draw_power_gauge(self.model,self.screen, self.user_turn)
                    pressed_gauge = pygame.key.get_pressed()[K_SPACE]
                    time.sleep(0.005)
                send_action(self.game_id, self.user_turn ,self.model.tank2.x,self.model.tank2.canon_angle,self.model.tank2.power,self.model.tank2.canon_direction)                    
                return_value=False
                missle.missle_action(self.model,self.screen,self.user_turn)
                self.model.tank2.power=0
            
        return return_value
""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""   Turn    Over   """""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""
class Turnover:
    def __init__(self, model,screen,view,turn,game_id):
        self.model = model
        self.screen = screen
        self.turn = turn
        self.view=view
        self.game_id=game_id
        
    def turncheck(self,missle):
         check=self.read_data()
         if self.turn != check['turn']:
             if check['power'] == 0:
                 return False
             else:
                 if self.turn == 1 :
                     other_turn = 2
                 elif self.turn == 2:
                     other_turn =1
                 missle.missle_action(self.model,self.screen,other_turn)
                 return True
             
    def read_data(self):
        params = urllib.urlencode({'game_id': self.game_id})
        conn = httplib.HTTPConnection(IP,9000)
        conn.request("POST", "/checkaction", params, headers)
        response = conn.getresponse()
        check_action = response.read()
        action=json.loads(check_action)
        conn.close()
        return {'turn':action['Turn'],'posx':action['posx'],'angle':action['angle'],'power':action['power'],'direction':action['direction']}
        
    def move_other_tank(self):
        data = self.read_data()
        if self.turn != data['turn']:
            if self.turn == 1:
                self.model.tank2.x=data['posx']
                self.model.tank2.canon_angle=data['angle']
                self.model.tank2.canon_direction = data['direction']
                self.model.tank2.power=data['power']
            elif self.turn == 2:
                self.model.tank1.x=data['posx']
                self.model.tank1.canon_angle=data['angle']
                self.model.tank1.power=data['power']
                self.model.tank1.canon_direction = data['direction']
                
        
""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""   login screen   """""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""
class Loginclass:
    def get_key(self):
        while 1:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                return event.key
            else:
                pass
      
    def display_login_box(self,screen, message):
        "Print a message in a box in the middle of the screen"
        fontobject = pygame.font.Font(None,18)
        pygame.draw.rect(screen, (0,0,0),
                         ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10, 200,20), 0)
        pygame.draw.rect(screen, (255,255,255),
                         ((screen.get_width() / 2) - 102, (screen.get_height() / 2) - 12, 204,24), 1)
        if len(message) != 0:
            screen.blit(fontobject.render(message, 1, (255,255,255)), ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
        pygame.display.flip()
    
    def ask_login(self,screen, question):
        "ask(screen, question) -> answer"
        pygame.font.init()
        current_string = []
        self.display_login_box(screen, question + ": " + string.join(current_string,""))
        check_exit=True;
        while check_exit:
            inkey = self.get_key()
            if inkey == K_BACKSPACE:
                current_string = current_string[0:-1]
                self.display_login_box(screen, question + ": " + string.join(current_string,""))
            elif inkey == K_RETURN:
                break
            elif inkey == K_MINUS:
                current_string.append("_")
            elif inkey <= 127:
                current_string.append(chr(inkey))
                self.display_login_box(screen, question + ": " + string.join(current_string,""))
        return string.join(current_string,"")

class LoadingScreen():
    def __init__(self,screen):
        self.screen = screen
        
    def loading(self):
        fontobject = pygame.font.Font(None,32)
        self.screen.blit(fontobject.render("Waiting for the other player", 1, (255,255,255)), ((self.screen.get_width() / 2) - 150, (self.screen.get_height() / 2) - 20))
        pygame.display.flip()
""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""   start button   """""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""

class Start_Button_Checker:
    # return true when clicking start button = TRUE
    def play_start_button(self,event,view):
        if event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] > 0 and pos[0] < 250 and pos[1] > 0 and pos[1] < 100: 
                    return True

""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""     M a  i n     """""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""

if __name__ == '__main__':
    # login part
    pygame.init()
    screen = pygame.display.set_mode((350,200))
    log=Loginclass()
    user_name=log.ask_login(screen, " ID ")
    sign_up(user_name)
    pygame.display.quit()
    # game screen
    screen = pygame.display.set_mode((200,100))
    model=TankModel()
    backgroundimage=pygame.image.load('background.png')
    view=PyGameWindowView(model,screen,backgroundimage)
    view.draw_startbutton(pygame.image.load('startbutton.jpg'))
    startbutton=Start_Button_Checker()
    check_start_button =True
    
    while check_start_button:
        for event in pygame.event.get():
            if event.type == QUIT:
                check_start_button =False
                check_game_run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if startbutton.play_start_button(event,view):
                    check_start_button =False
                    
    pygame.display.quit()        
    
    screen = pygame.display.set_mode((970,546))
    game_id = int(startgame(user_name))
    user_id_2 = check_second_user(game_id) 
    check_user_id_2 = True

    if user_id_2 == "1":
        check_game_run = True
        user_turn=2
        Firecheck = False
    else:
        user_turn=1
        load=LoadingScreen(screen)
        load.loading()
        Firecheck = True
        while check_user_id_2:
            user_id_2 = check_second_user(game_id)
            time.sleep(0.5)
            if user_id_2 == "1":
                check_user_id_2 = False
                check_game_run = True
            for event in pygame.event.get():
                if event.type == QUIT:
                    check_user_id_2 = False
                    check_game_run = False
    model = TankModel()
    backgroundimage=pygame.image.load('background.png')
    view=PyGameWindowView(model,screen,backgroundimage)
    view.draw_background()
    view.draw_tank(model,screen)
    view.draw_power_gauge_bar(model,screen)
    turnover = Turnover(model,screen,view,user_turn,game_id)
    missle = FireCanonMissle(model,screen,view)
    control=PyGameKeyboardController(model,screen,view,game_id,turnover,missle)
    while check_game_run:
        while Firecheck:
            for event in pygame.event.get():
                if event.type == QUIT:
                    check_game_run= False
                elif event.type == pygame.KEYDOWN:
                    Firecheck=control.keyboard_event(event)
        time.sleep(0.1)
        turnover.move_other_tank()
        Firecheck = turnover.turncheck(missle)
        view.draw_tank(model,screen)
        view.draw_angle(model,screen,user_turn)
        view.draw_power_gauge_bar(model,screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                check_game_run= False
                
    pygame.quit()   
            
            
            