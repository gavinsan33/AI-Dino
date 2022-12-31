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

def simulate():
    global epsilon, epsilon_decay

    # for t in range(MAX_EPISODES):

    #     # Init environment
    #     state = env.reset()
    #     total_reward = 0
    #     for episode in range(MAX_TRY):


    #         # In the beginning, do random action to learn
    #         if random.uniform(0, 1) < epsilon:
    #             action = env.action_space.sample()
    #         else:
    #             action = np.argmax(q_table[state])

    #         # Do action and get result
    #         next_state, reward, done, _ = env.step(action)
    #         total_reward += reward

    #         # Get correspond q value from state, action pair
    #         q_value = q_table[state][action]
    #         best_q = np.max(q_table[next_state])

    #         # Q(state, action) <- (1 - a)Q(state, action) + a(reward + rmaxQ(next state, all actions))
    #         q_table[state][action] = (1 - learning_rate) * q_value + learning_rate * (reward + gamma * best_q)

    #         # Set up for the next iteration
    #         state = next_state

    #         # Draw games
    #         env.render()

    #         # When episode is done, print reward
    #         if done or t >= MAX_TRY - 1:
    #             print("Episode %d finished after %i time steps with total reward = %f." % (episode, t, total_reward))
    #             break

    

if __name__ == "__main__":
    env = gym.make("Pygame-v0")

    folder = "C:/Users/Gavin/Documents/Coding Projects/Reinforcement Learning AI"
    log_path = os.path.join(folder, 'Training', 'Logs')
    PPO_Path = os.path.join(folder, 'Training', 'Saved Models', 'Dino')
    
    # model = PPO("MlpPolicy", env, verbose=0, tensorboard_log=log_path)
    model = PPO.load(PPO_Path, env=env)

    # print("Training...")
    # model.learn(total_timesteps=500000, progress_bar=True)
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
        print('Episode:{} Score:{}'.format(episode, score))

    env.close()


