from gym.envs.registration import register

register(
    id='Pygame-v0',
    # CHANGE FOR TESTING:
    # entry_point='gym_game.training_envs:DinosaurGameEnv',
    entry_point='gym_game.envs:DinosaurGameEnv',
    
    max_episode_steps=10000,
)