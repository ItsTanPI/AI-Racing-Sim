
from stable_baselines3 import PPO
import logging
import torch
from stable_baselines3.common.vec_env import SubprocVecEnv
import os
from model import Lilach, LilachV2 

from datetime import datetime

if torch.cuda.is_available():
    print(f"CUDA available: {torch.cuda.get_device_name(0)}")

logging.basicConfig(filename=r'data\log\training.log', level=logging.INFO)

torch.cuda.synchronize()
torch.cuda.empty_cache()

def make_env():
    def _init():
        return LilachV2()
    return _init


if __name__ == '__main__':    
    n_agents = 20
    env = SubprocVecEnv([make_env() for _ in range(n_agents)])
    
    model_path = r'data\model\LilachV4-1.zip'
    if os.path.isfile(model_path):
        model = PPO.load(model_path, env=env, device="cuda", n_steps=3072, learning_rate = 0.001, batch_size=128, ent_coef=0.001)
        logging.info("Loaded existing model.")
        print("Loaded existing model.")
    else:
        model = PPO("MlpPolicy", env, verbose=1, device="cuda", n_steps=3072, learning_rate = 0.001, batch_size=128, ent_coef=0.001)
        print("Loaded new model.")
    env.reset()
    
    """model = PPO(
    'MlpPolicy',
    env,
    learning_rate=0.001,
    ent_coef=0.01,
    gamma=0.99,
    gae_lambda=0.95,
    n_epochs=10,
    batch_size=64,
    clip_range=0.2,
    max_grad_norm=0.5,
    verbose=1
)"""
    total_timesteps_per_episode = 100000  # Set timesteps per episode as needed
    num_episodes = 1

    for episode in range(num_episodes):
        print(f"Starting episode {episode + 1}/{num_episodes}")
        model.learn(total_timesteps=total_timesteps_per_episode)    
        model.save(fr'data\model\LilachV4-{episode + 1}.zip')

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = (f"Model saved as LilachV4-{episode + 1}.zip "
                   f"for episode {episode + 1} with {total_timesteps_per_episode} steps "
                   f"at {current_time}")
        
        print(message)
        logging.info(message)
