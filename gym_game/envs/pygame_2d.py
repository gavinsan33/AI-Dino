import pygame as pg
import math
import time
import random
import sys
import numpy as np

screen_width = 1500
screen_height = 800

START_Y = int(screen_height / 2)

class Dino:
    def __init__(self, pos):
        self.surface = pg.image.load('./Dinosaur Game Master/gym_game/assets/dino.png')
        self.surface = pg.transform.scale(self.surface, (100, 100))
        self.pos = pos
        self.jump_state = 0
        self.num_jumps = 0
        self.new_jump = False

    def draw(self, screen):
        screen.blit(self.surface, self.pos)
        # pg.draw.circle(screen, (255, 0, 0), self.get_left_hb(), 3)
        # pg.draw.circle(screen, (255, 0, 0), self.get_right_hb(), 3)
    
    def get_right_hb(self):
        return [self.pos[0] + 100, self.pos[1] + 100]
    
    def get_left_hb(self):
        return [self.pos[0], self.pos[1] + 100]
        
    def getX(self):
        return self.pos[0]
    
    def getY(self):
        return self.pos[1]

    def move(self, y):
        self.pos[1] += y

    def jump(self):
        self.jump_state = 1
        self.num_jumps += 1
        self.new_jump = True
    
cacti_on_screen = []

class Cactus:
    def __init__(self):
        self.surface = pg.image.load('./Dinosaur Game Master/gym_game/assets/cactus.png')
        self.surface = pg.transform.scale(self.surface, (100, 100))

        if(len(cacti_on_screen) == 0):
            self.pos = [random.randrange(screen_width, 2 * screen_width), START_Y]
        else:
            rand = cacti_on_screen[-1].getX() + 250
            self.pos = [random.randrange(rand, rand + screen_width), START_Y]
            
        cacti_on_screen.append(self)
    
    def draw(self, screen):
        screen.blit(self.surface, self.pos)
        # pg.draw.circle(screen, (255, 0, 0), self.get_left_hb(), 3)
        # pg.draw.circle(screen, (255, 0, 0), self.get_right_hb(), 3)

    def move(self, x):
        self.pos[0] -= x
    
    def get_left_hb(self):
        return [self.pos[0] + 30, self.pos[1]]    
    
    def get_right_hb(self):
        return [self.pos[0] + 70, self.pos[1]]   
    
    def getX(self):
        return self.pos[0]
    
    def getY(self):
        return self.pos[1]
    

class PyGame2D:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("Arial", 30)
        self.dino = Dino([20, START_Y])
        self.game_speed = 120
        self.game_over = False
        self.start_time = pg.time.get_ticks()
        self.new_cacti_jumped = 0
        self.total_cacti_jumped = 0
        self.ticks = 0

        self.total_reward = 0
        self.prev_reward = 0



    def evaluate(self):
        self.total_reward = self.ticks * 2
        reward = self.total_reward - self.prev_reward
        self.prev_reward = self.total_reward

        if(self.dino.jump_state != 0):
            reward -=3

        # if(self.dino.new_jump):
        #     reward = -15
        #     self.dino.new_jump = False

        if(self.new_cacti_jumped):
            reward = 500

        if(self.game_over):
            reward = -250

        self.new_cacti_jumped = 0
        return reward


    def is_done(self):
        return self.game_over      
    
    def get_nearest_cactus(self):
        
        index = 0
        for i in range(0, len(cacti_on_screen)):
            if(cacti_on_screen[i].get_right_hb()[0] > self.dino.get_left_hb()[0]):
                index = i
                break
    
        return index
    
    def observe(self):
        
        if len(cacti_on_screen) != 0:
            # print(np.array([cacti_on_screen[self.get_nearest_cactus()].get_left_hb()[0] - self.dino.get_right_hb()[0]]).astype(float))
            return np.array([cacti_on_screen[self.get_nearest_cactus()].get_left_hb()[0] - self.dino.get_right_hb()[0]])
        
        return np.array([3000])

 
    def update(self):
        self.ticks += 1
        CACTUS_SPEED = 7
        #normally 7
        
        for c in cacti_on_screen:
            c.move(CACTUS_SPEED)
            if(c.getX() < -100):
                cacti_on_screen.remove(c)
                self.new_cacti_jumped += 1
                self.total_cacti_jumped += 1
        
        JUMP_HEIGHT = 200
        JUMP_SPEED = 20
            
        if(self.dino.jump_state != 0):
            if(self.dino.jump_state == 1):
                if((self.dino.getY() - JUMP_HEIGHT) / JUMP_HEIGHT > 0.1):
                    self.dino.move(-JUMP_SPEED * ((self.dino.getY() - JUMP_HEIGHT) / JUMP_HEIGHT))
                    # self.dino.move(-JUMP_SPEED)
                else:
                    self.dino.jump_state = 2
            elif(self.dino.jump_state == 2):
                if((START_Y - self.dino.getY()) / JUMP_HEIGHT > 0.1):
                    self.dino.move(JUMP_SPEED * ((self.dino.getY() - JUMP_HEIGHT) / JUMP_HEIGHT))
                    # self.dino.move(JUMP_SPEED)
                else:
                    self.dino.jump_state = 0
            
            if(self.dino.jump_state == 0):
                self.dino.pos[1] = START_Y

        if(len(cacti_on_screen) > 0):
            c = self.get_nearest_cactus()
            dl = self.dino.get_left_hb()
            dr = self.dino.get_right_hb()
            cl = cacti_on_screen[c].get_left_hb()
            cr = cacti_on_screen[c].get_right_hb()

            # if(self.dino.num_jumps > 5):
            #     self.game_over = True
            # GAME OVER?
            if(dr[0] > cl[0]):
                if(dr[1] > cl[1]):
                    self.game_over = True
                    self.view()
                    

    
    def action(self, action):
        if(action == 1 and self.dino.jump_state == 0):
            self.dino.jump_state = 1

    def view(self):
        # draw game
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.action(1)

        if(not self.game_over):
            self.screen.fill((255, 255, 255))
        else:
            self.screen.fill((255, 0, 0))
        horizon = START_Y + 85
        pg.draw.line(self.screen, (0, 0, 0), (0, horizon), (screen_width, horizon))
        self.dino.draw(self.screen)

        if(len(cacti_on_screen) < 5):
            Cactus()
        for c in cacti_on_screen:
            c.draw(self.screen)

        text = self.font.render(f"Score: {self.ticks}", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (screen_width/2, 100)
        self.screen.blit(text, text_rect)

        pg.display.flip()
        # time.sleep(5)

        TRAINING = False
        if(not TRAINING):
            self.clock.tick(self.game_speed)