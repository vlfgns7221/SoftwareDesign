# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 13:14:32 2014

@author: pilhunchoi
"""

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

# Server class : connect to Server
class Server_call:
    def __init__(self):
        self.IP = "10.7.88.228" # Server IP
        self.conn = httplib.HTTPConnection(self.IP,9000)
        self.headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    
    # sign up function    
    def sign_up(self,user_name):
        params = urllib.urlencode({'user_id': user_name}) #information to update
        self.conn.request("POST", "/sign_up", params, self.headers) #connect to server and send the information
        response = self.conn.getresponse() #get return value from server
        check_signup = response.read()
        if check_signup == user_name:
            return True
        else:
            return False

    def startgame(self,user_name):
        params = urllib.urlencode({'user_id': user_name}) #information to update
        self.conn.request("POST", "/startgame", params, self.headers)  #connect to server and send the information
        response = self.conn.getresponse()#get return value from server
        game_id = response.read() # decode the data
        return game_id
        
    def check_second_user(self,game_id):
        params = urllib.urlencode({'game_id': game_id})   #information to update  
        self.conn.request("POST","/checkseconduser",params,self.headers)  #connect to server and send the information
        response = self.conn.getresponse()#get return value from server
        user_id_2 =response.read() # decode the data
        return user_id_2
        
    def send_action(self,game_id,turn,posx,angle,power,direction):
        #information to update
        params = urllib.urlencode({'game_id': game_id,'turn':turn,'posx':posx,'angle':angle,'power':power,'direction':direction}) 
        self.conn.request("POST", "/action", params, self.headers)  #connect to server and send the information
        response = self.conn.getresponse()#get return value from server
        game_id = response.read()# decode the data
        
    def read_data(self,game_id):
        params = urllib.urlencode({'game_id': game_id}) #information to update
        self.conn.request("POST", "/checkaction", params, self.headers)  #connect to server and send the information
        response = self.conn.getresponse()#get return value from server
        check_action = response.read()# decode the data
        action=json.loads(check_action) # make the data dictionary
        return {'turn':action['Turn'],'posx':action['posx'],'angle':action['angle'],'power':action['power'],'direction':action['direction']}
         
    def check_end(self,game_id):
        params = urllib.urlencode({'game_id': game_id}) #information to update
        self.conn.request("POST", "/check_end", params, self.headers)  #connect to server and send the information
        response = self.conn.getresponse()#get return value from server
        check_end = response.read()# decode the data
        return check_end

    def closegame(self,game_id):
        params = urllib.urlencode({'game_id': game_id}) #information to update
        self.conn.request("POST", "/closegame", params, self.headers)  #connect to server and send the information
               
""""""""""""""""""""""""""""""""""""""""""""""""    
"""""""""""""""   Tank   model   """""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""
# Tank model class
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
 #Draw class       
class  PyGameWindowView:
    def __init__(self,model,screen,background_image):
        self.model = model      # list of stones
        self.screen = screen    # game window
        self.background_image=background_image
    # Fill Background Black
    def draw_background(self):
        self.screen.blit(self.background_image,(0,0))
        pygame.display.update()
    # Start Button     
    def draw_startbutton(self,image):
        self.screen.blit(image,(0,0))
        pygame.display.update()
    # draw tank
    def draw_tank(self,model,screen):
        self.screen.blit(self.background_image,(0,0))
        img_tank11 = pygame.image.load('tank11.png') # user 1 tank image (direction right)
        img_tank12 = pygame.image.load('tank12.png') # user 1 tank image (direction left)
        img_tank21 = pygame.image.load('tank21.png') # user 2 tank image (direction right)
        img_tank22 = pygame.image.load('tank22.png') # user 2 tank image (direction left)
        if model.tank1.canon_direction == 0:
            screen.blit(img_tank11,(model.tank1.x-5, model.tank1.y))
        elif model.tank1.canon_direction == 1:
            screen.blit(img_tank12,(model.tank1.x-5, model.tank1.y))
       
        if model.tank2.canon_direction == 0:
            screen.blit(img_tank21,(model.tank2.x-5, model.tank2.y))
        elif model.tank2.canon_direction == 1:
            screen.blit(img_tank22,(model.tank2.x-5, model.tank2.y))
        pygame.display.update()
    
    # draw canon_angle 
    def draw_angle(self,model,screen,user_turn):
        if user_turn == 1: 
            pos_tank=(model.tank1.x+25,model.tank1.y+30)
            angle=model.tank1.canon_angle
        elif user_turn == 2:
            pos_tank=(model.tank2.x+25,model.tank2.y+30)
            angle=model.tank2.canon_angle            
        vec_arrow=(pos_tank[0]+70*math.cos(math.radians(angle)),pos_tank[1]+70*math.sin(math.radians(angle)))
        pygame.draw.line( screen, (255,255,0), pos_tank, vec_arrow,2 )
        pygame.display.update()        
    
    # draw power gauge bar    
    def draw_power_gauge_bar(self,model,screen):
        pygame.draw.rect(screen,(255,255,255),Rect( (200,50),(600,20) ),1 )
        pygame.display.update()
    
    # draw powewr gauge
    def draw_power_gauge(self,model,screen,user_turn):
        if user_turn == 1: 
            pygame.draw.rect(screen,(255,255,0),Rect( (200,50),(model.tank1.power,20) ))
        elif user_turn ==2:
            pygame.draw.rect(screen,(255,255,0),Rect( (200,50),(model.tank2.power,20) ))    
        pygame.display.update()
    
    # draw gameover message, win or lose    
    def draw_gameover_message(self,win_determine):
        if win_determine == 1:
            self.screen.blit(pygame.image.load('win.png'),((self.screen.get_width() / 2) - 75, (self.screen.get_height() / 2) - 10))
        elif win_determine == 0:
            self.screen.blit(pygame.image.load('lose.png'),((self.screen.get_width() / 2) - 75, (self.screen.get_height() / 2) - 10))            
        pygame.display.update()
        
    # draw missle image        
    def draw_missle(self,model,screen,missle,x,y):
        self.draw_tank(model,screen)
        screen.blit( missle, (x, y) )
        pygame.display.update()
    
    #draw explosion image    
    def draw_explosion(self,model,screen,explosion,x,y):
        self.draw_tank(model,screen)
        screen.blit( explosion, (x-20, y-20) )
        pygame.display.update()
        time.sleep(0.5)        
    
    # draw hp bar    
    def draw_hp_bar(self,model,screen):
        pygame.draw.rect(screen,(255,0,0),Rect( (model.tank1.x,model.tank1.y),(int(model.tank1.hp/15),5) ))
        pygame.draw.rect(screen,(255,0,0),Rect( (model.tank2.x,model.tank2.y),(int(model.tank2.hp/15),5) ))
        pygame.display.update()
        

""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""   Tank  action   """""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""
# Tank action class(keyboard order)
class PyGameKeyboardController:
    def __init__(self,servercall,model,screen,view,game_id,turnover,missle):
        self.servercall=servercall
        self.model = model
        self.screen = screen
        self.view = view
        self.game_id = game_id
        self.turnover = turnover
        self.user_turn = self.turnover.turn
        self.missle = missle

    # Keyboard action
    def keyboard_event(self,event):
        return_value = True
        pressed_move = pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_LEFT] # control key to move tank 
        pressed_angle = pygame.key.get_pressed()[K_UP] or pygame.key.get_pressed()[K_DOWN]  # control key yo change the canon angle 
        pressed_gauge = pygame.key.get_pressed()[K_SPACE] # control key to fire the missle
        if self.user_turn == 1:
            if pressed_move:
                while pressed_move: # if keep pressing the key(K_RIGHT or K_LEFT), keep to move the tank
                    pygame.event.get()
                    if event.key == pygame.K_RIGHT: 
                        self.model.tank1.canon_direction=0
                        self.model.tank1.x+=1
                    elif event.key == pygame.K_LEFT:
                        self.model.tank1.canon_direction=1
                        self.model.tank1.x-=1
                    self.view.draw_tank(self.model,self.screen)
                    self.view.draw_angle(self.model,self.screen,self.user_turn)
                    self.view.draw_hp_bar(self.model,self.screen)
                    pressed_move = pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_LEFT]
                    # send changed information to the server
                    self.servercall.send_action(self.game_id, self.user_turn ,self.model.tank1.x,self.model.tank1.canon_angle,self.model.tank1.power,self.model.tank1.canon_direction)
                    time.sleep(0.001)
                    
            elif pressed_angle: # # if keep pressing the key(K_UP or K_DOWN), keep to change the angle 
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
                    self.view.draw_hp_bar(self.model,self.screen)
                    pressed_angle = pygame.key.get_pressed()[K_UP] or pygame.key.get_pressed()[K_DOWN]
                    # send changed information to the server
                    self.servercall.send_action(self.game_id, self.user_turn ,self.model.tank1.x,self.model.tank1.canon_angle,self.model.tank1.power,self.model.tank1.canon_direction)
                    time.sleep(0.01)
                    
            elif pressed_gauge: # if keep pressing the key(K_SPACE), increase the power gauge
                self.model.tank1.power=0
                self.view.draw_power_gauge_bar(self.model,self.screen)
                while pressed_gauge: # if keep pressing the key
                    pygame.event.get()
                    self.model.tank1.power+=1
                    if model.tank1.power > 600:
                        model.tank1.power=1
                        self.view.draw_tank(self.model,self.screen)
                        self.view.draw_power_gauge_bar(self.model,self.screen)
                    self.view.draw_power_gauge(self.model,self.screen,self.user_turn)
                    self.view.draw_hp_bar(self.model,self.screen)
                    pressed_gauge = pygame.key.get_pressed()[K_SPACE]
                    time.sleep(0.005)
                # send changed information to the server
                self.servercall.send_action(self.game_id, self.user_turn ,self.model.tank1.x,self.model.tank1.canon_angle,self.model.tank1.power,self.model.tank1.canon_direction)
                missle.missle_action(self.model,self.screen,self.user_turn) # fire the missle
                return_value=False # end turn signal
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
                    self.view.draw_hp_bar(self.model,self.screen)
                    pressed_move = pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_LEFT]
                    self.servercall.send_action(self.game_id, self.user_turn ,self.model.tank2.x,self.model.tank2.canon_angle,self.model.tank2.power,self.model.tank2.canon_direction)
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
                    self.view.draw_hp_bar(self.model,self.screen)
                    pressed_angle = pygame.key.get_pressed()[K_UP] or pygame.key.get_pressed()[K_DOWN]
                    self.servercall.send_action(self.game_id, self.user_turn ,self.model.tank2.x,self.model.tank2.canon_angle,self.model.tank2.power,self.model.tank2.canon_direction)
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
                    self.view.draw_hp_bar(self.model,self.screen)
                    pressed_gauge = pygame.key.get_pressed()[K_SPACE]
                    time.sleep(0.005)
                self.servercall.send_action(self.game_id, self.user_turn ,self.model.tank2.x,self.model.tank2.canon_angle,self.model.tank2.power,self.model.tank2.canon_direction)                    
                return_value=False
                missle.missle_action(self.model,self.screen,self.user_turn)
                self.model.tank2.power=0
            
        return return_value # if return value is true, continue the turn; if false, change the turn 
        # when the user fire the missle, return_value becomes false
        
""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""   Fire  action   """""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""
# missle action class
class FireCanonMissle:
    def __init__(self,model,screen,view):
        self.model = model
        self.screen = screen
        self.view = view
        self.missle1 = pygame.image.load('mis1.png') # missle image (to the right)
        self.missle2 = pygame.image.load('mis2.png') # missle image (to the left)
        self.explosion = pygame.image.load('explosion.png') # explosion image
        
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
        
        # calculation for the trace of the missle
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
        # draw part
        view.draw_tank(model,screen) 
        view.draw_angle(model,screen,turn)
        view.draw_power_gauge_bar(model,screen)
        view.draw_explosion(model,screen,self.explosion,x,y)
        view.draw_tank(model,screen)
        
        # damage calculation
        self.damage_cal(model,x,y)
    
    #damage calculation part    
    def damage_cal(self,model,x,y):
        dis_tank1=abs( math.sqrt( (x - model.tank1.x)**2 + (y - model.tank1.y)**2  ) )
        dis_tank2=abs( math.sqrt( (x - model.tank2.x)**2 + (y - model.tank2.y)**2  ) )
        if dis_tank1 < 70:
            model.tank1.hp = model.tank1.hp - 300 * (1.0 - dis_tank1/100.0)
            if model.tank1.hp <0:
                model.tank1.hp = 0
            
        if dis_tank2 < 70:
            model.tank2.hp = model.tank2.hp - 300 * (1.0 - dis_tank2/100.0)    
            if model.tank2.hp <0:
                model.tank2.hp = 0
                

""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""   Turn    Over   """""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""
# Turn change class
class Turnover:
    def __init__(self,servercall, model,screen,view,turn,game_id):
        self.servercall = servercall
        self.model = model
        self.screen = screen
        self.turn = turn
        self.view=view
        self.game_id=game_id
    
    # check if the other user fire the missle(that means that turn is changeds)  
    def turncheck(self,missle):
         check=self.servercall.read_data(self.game_id)
         if self.turn != check['turn']:
             if check['power'] == 0: 
                 return False # not tour turn
             else:
                 if self.turn == 1 :
                     other_turn = 2
                 elif self.turn == 2:
                     other_turn =1
                 missle.missle_action(self.model,self.screen,other_turn) # fire the missle of the other user
                 return True # now your turn
             
    def move_other_tank(self):
        data = self.servercall.read_data(self.game_id)
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
"""""""""""""""    Game  Over    """""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""
# check game over
class Gameover:
    def __init__(self,servercall,view,user_turn,game_id):
        self.servercall = servercall
        self.view=view
        self.user_turn = user_turn
        self.game_id = game_id
    
    # gameover when the other user quit the game    
    def check_afk(self):
        check = self.servercall.check_end(self.game_id)
        if check == 'False':
            self.view.draw_gameover_message(1)
            return False
        elif check == 'True':
            return True

    # when you quit the game, send the quit information to Server
    def close_game(self):
        self.servercall.closegame(self.game_id)

    # gameover when one of users'hp becomes less than 0
    def determine_gameover(self,model):
        if self.user_turn == 1:
            if model.tank1.hp <= 0:
                self.view.draw_gameover_message(0)
                return False #game end signal
            elif model.tank2.hp <=0:
                self.view.draw_gameover_message(1)
                return False #game end signal
            else:
                return True #game not end signal
        elif self.user_turn == 2:
            if model.tank1.hp <= 0:
                self.view.draw_gameover_message(1)
                return False #game end signal
            elif model.tank2.hp <=0:
                self.view.draw_gameover_message(0)
                return False #game end signal
            else:
                return True #game not end signal
                
""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""   login screen   """""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""
#login class
class Loginclass:
    # get id
    def get_key(self):
        while 1:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                return event.key
            else:
                pass
    
    #draw login box
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
    
    # represent asking the login 
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
            elif inkey == K_RETURN: #press enter, typing end and make ID
                break
            elif inkey == K_MINUS:
                current_string.append("_")
            elif inkey <= 127:
                current_string.append(chr(inkey))
                self.display_login_box(screen, question + ": " + string.join(current_string,""))
        return string.join(current_string,"")

""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""  Loading Screen  """""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""
# Waiting screen for user2
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
# game start button
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
    servercall = Server_call()
    pygame.init()
    backgroundimage=pygame.image.load('background.png')
    startbutton = pygame.image.load('startbutton.jpg')
    screen = pygame.display.set_mode((350,200))
    log=Loginclass()
    user_name=log.ask_login(screen, " ID ")
    servercall.sign_up(user_name)
    pygame.display.quit()
    # start button screen
    screen = pygame.display.set_mode((200,100))
    model=TankModel()
    
    view=PyGameWindowView(model,screen,backgroundimage)
    view.draw_startbutton(startbutton)
    startbutton=Start_Button_Checker()
    check_start_button =True
    
    # check if the start button is pressed
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
    game_id = int(servercall.startgame(user_name)) # get the game if from server
    user_id_2 = servercall.check_second_user(game_id) # check if user2 is existed(0 : not exist, 1: exist)
    check_user_id_2 = True
   
    if user_id_2 == "1": # if user2 is existed, the user2 is you
        check_game_run = True
        user_turn=2
        check_game_run2 = False
    else: # if user2 is not existed, the user1 is you
        user_turn=1 
        load=LoadingScreen(screen)
        load.loading()  # open the loading screen for waiting for user2
        check_game_run2 = True
        while check_user_id_2:
            user_id_2 = servercall.check_second_user(game_id) #check if user2 enters the game
            time.sleep(0.5)
            if user_id_2 == "1": # if user2 is entered, start the game
                check_user_id_2 = False
                check_game_run = True
            for event in pygame.event.get():
                if event.type == QUIT: # if you quit the game, deactivate the game and close the game
                    check_user_id_2 = False
                    check_game_run = False 
                    gameover = Gameover(servercall,view,user_turn,game_id)
                    gameover.close_game()
    
    # game start
    model = TankModel() # declare the tank models
    view=PyGameWindowView(model,screen,backgroundimage) # declare draw class
    view.draw_background()
    view.draw_tank(model,screen)
    view.draw_power_gauge_bar(model,screen)
    turnover = Turnover(servercall,model,screen,view,user_turn,game_id) # declare Turn over class
    gameover = Gameover(servercall,view,user_turn,game_id)#declare gameover class
    missle = FireCanonMissle(model,screen,view)          # declare missle class
    control=PyGameKeyboardController(servercall,model,screen,view,game_id,turnover,missle) #declare control class
    Firecheck = True
    while check_game_run:
        checkafk = gameover.check_afk() # check if the other user quit the game
        while check_game_run2:    
            checkafk = gameover.check_afk() 
            checkwin = gameover.determine_gameover(model) # check if one of the users' hp beomes less than 0
            for event in pygame.event.get():
                if event.type == QUIT:
                    checkafk = False
                    check_game_run= False
                elif event.type == pygame.KEYDOWN:
                    Firecheck=control.keyboard_event(event) 
            # if you fire the missle, end turn or if you win or lose or the other quit the game, end the game
            check_game_run2 = checkafk and checkwin and Firecheck 
        time.sleep(0.1)
        turnover.move_other_tank() # update the other user's tank
        checkwin = gameover.determine_gameover(model) # check if one of the users' hp beomes less than 0
        Firecheck = turnover.turncheck(missle)# check if the other user fire the canon
        check_game_run2 = checkafk and checkwin and Firecheck # if Firecheck is True, turn is yours
        check_game_run = checkafk and checkwin 
        
        view.draw_tank(model,screen)
        view.draw_angle(model,screen,user_turn)
        view.draw_power_gauge_bar(model,screen)
        view.draw_hp_bar(model,screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                check_game_run= False
    
    gameover.close_game() # if you quit the game, send this information to Server
    servercall.conn.close()#close server
    pygame.quit()         #close the game
            
            