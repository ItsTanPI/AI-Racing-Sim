
from stable_baselines3 import PPO, A2C
import logging
import torch
from stable_baselines3.common.vec_env import SubprocVecEnv
import os
from TrackModel import Decan 

from datetime import datetime

if torch.cuda.is_available():
    print(f"CUDA available: {torch.cuda.get_device_name(0)}")

logging.basicConfig(filename=r'data\log\training.log', level=logging.INFO)

torch.cuda.synchronize()
torch.cuda.empty_cache()

def make_env():
    def _init():
        return Decan()
    return _init

def print_hyperparameters(model):
    print("==== PPO Hyperparameters ====")
    print("Learning Rate:", model.learning_rate)
    print("Gamma (Discount Factor):", model.gamma)
    print("Number of Environments:", model.n_envs)
    print("Entropy Coefficient:", model.ent_coef)
    print("Clip Range:", model.clip_range)
    print("GAE Lambda:", model.gae_lambda)
    print("Number of Epochs:", model.n_epochs)
    print("Max Gradient Norm:", model.max_grad_norm)
    print("Number of Steps per Rollout:", model.n_steps)
    print("Batch Size:", model.batch_size)
    print("Policy Architecture (Hidden Layers):", model.policy_kwargs)
    print("Device (CPU or GPU):", model.device)
    print("=============================")

if __name__ == '__main__':    
    n_agents = 20
    env = SubprocVecEnv([make_env() for _ in range(n_agents)])
    
    
    model_path = r'data\model\DecanDrift-New.zip'
    if os.path.isfile(model_path):
        print("!!!!!!!!!!Loded Old!!!!!!!!!!!")
        model = PPO.load(model_path, env = env, verbose=2, device="cuda",
                            learning_rate = 0.001,
                            batch_size=256,
                            n_steps=4096,
                            clip_range=0.2,
                            ent_coef=0.5,   
                            gae_lambda=0.65,
                            gamma=0.975,
                            n_epochs=20,
                            max_grad_norm=0.5,
                            policy_kwargs = dict(net_arch=[256, 256, 128])
                    )
    else:
        model = PPO("MlpPolicy", env = env, verbose=2, device="cuda",
                            learning_rate = 0.001,
                            batch_size=256,
                            n_steps=4096,
                            clip_range=0.2,
                            ent_coef=0.1,   
                            gae_lambda=0.65,
                            gamma=0.975,
                            n_epochs=20,
                            max_grad_norm=0.5,
                            policy_kwargs = dict(net_arch=[256, 256, 128])
                    )
        print("Loaded new model.")
    env.reset()
    
    print_hyperparameters(model)
    
    """
    model = PPO
    ('MlpPolicy',
    env,
    learning_rate=0.00,
    ent_coef=0.01,
    gamma=0.99,
    gae_lambda=0.95,
    n_epochs=10,
    batch_size=64,
    clip_range=0.2,
    max_grad_norm=0.5,
    verbose=1)"""
    total_timesteps_per_episode = 5000000  # Set timesteps per episode as needed
    num_episodes = 1

    for episode in range(num_episodes):
        print(f"Starting episode {episode + 1}/{num_episodes}")
        model.learn(total_timesteps=total_timesteps_per_episode)    
        model.save(fr'data\model\DecanDrift-New.zip')

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = (f"Model saved as DecanDrift-New.zip "
                   f"for episode DecanDrift-New with {total_timesteps_per_episode} steps "
                   f"at {current_time}")
        
        print(message)
        logging.info(message)
