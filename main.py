import sys
import numpy as np
import math
import random
import gym
import gym_game
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
import os
from stable_baselines3.common.evaluation import evaluate_policy


if __name__ == "__main__":
    env = gym.make("Pygame-v0")

    folder = "C:/Users/gavin/OneDrive/Documents/Coding/Dinosaur Game Master"
    log_path = os.path.join(folder, 'Training', 'Logs')
    PPO_Path = os.path.join(folder, 'Training', 'Saved Models', 'Dino (meh)')
    
    # model = PPO("MlpPolicy", env, verbose=0, tensorboard_log=log_path)
    model = PPO.load(PPO_Path, env=env)

    # check_env(env)

    # print("Training...")
    # model.learn(total_timesteps=200000, progress_bar=True)
    # print("Finished Training")
    # model.save(os.path.join(folder, 'Training', 'Saved Models', 'Dino'))


    episodes = 20
    for episode in range(1, episodes+1):
        obs = env.reset()
        done = False
        score = 0 
        
        while not done:
            action, _ = model.predict(obs)
            obs, reward, done, info = env.step(action)
            score+=reward
            # print(score)
        print('Episode:{} Score:{}'.format(episode, score))

    env.close()


