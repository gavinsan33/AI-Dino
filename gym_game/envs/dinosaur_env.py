import gym 
from gym import Env
from gym.spaces import Discrete, Box, Dict, Tuple, MultiBinary, MultiDiscrete 
import numpy as np
import random
import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.evaluation import evaluate_policy
import random
from gym_game.envs.pygame_2d import PyGame2D
from gym_game.envs import pygame_2d
# from pygame_2d import PyGame2D

class DinosaurGameEnv(Env):
    def __init__(self):
        self.pygame = PyGame2D()
        self.screen_width = 1500
        
        self.low = np.array([0])
        self.high = np.array([3000])
        
        self.action_space = Discrete(1000)
        self.observation_space = Box(low=self.low, high=self.high, dtype=float)
    
    def step(self, action): 
        assert self.action_space.contains(
            action
        ), f"{action!r} ({type(action)}) invalid"
        
        # print(action)
        if(action == 25 and self.pygame.dino.jump_state == 0):
            self.pygame.dino.jump_state = 1
        # else:
        #     self.pygame.dino.jump_state = 0
        
        self.pygame.update()
        self.pygame.view()
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}
    
    def reset(self):
        pygame_2d.cacti_on_screen.clear()
        del self.pygame
        self.pygame = PyGame2D()
        obs = self.pygame.observe()
        return obs 
    
    def render(self, mode="human", close=False):
        self.pygame.view()
