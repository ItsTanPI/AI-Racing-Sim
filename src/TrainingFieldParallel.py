
from stable_baselines3 import PPO
import logging
import torch
from stable_baselines3.common.vec_env import SubprocVecEnv
import os
from model import Lilach, LilachV2 

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
    n_agents = 16
    env = SubprocVecEnv([make_env() for _ in range(n_agents)])
    
    model_path = r'data\model\LilachV2_episode_1.zip'
    if os.path.isfile(model_path):
        model = PPO.load(model_path, env=env, device="cuda", n_steps=2048)
        logging.info("Loaded existing model.")
        print("Loaded existing model.")
    else:
        model = PPO("MlpPolicy", env, verbose=1, device="cuda")
        print("Loaded new model.")
    
    total_timesteps_per_episode = 400000  # Set timesteps per episode as needed
    num_episodes = 1

    for episode in range(num_episodes):
        print(f"Starting episode {episode + 1}/{num_episodes}")
        model.learn(total_timesteps=total_timesteps_per_episode)
        model.save(fr'data\model\LilachV2_episode_{episode + 1}.zip')
        print(f"Model saved as LilachV2_episode_{episode + 1}.zip for episode {episode + 1} with {total_timesteps_per_episode} steps")
        logging.info(f"Model saved as LilachV2_episode_{episode + 1}.zip for episode {episode + 1} with {total_timesteps_per_episode} steps")
