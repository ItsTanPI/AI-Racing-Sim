from stable_baselines3 import PPO
import pygame
import os
import time
import logging
import sys
from model import Lilach
import csv
from torch.utils.tensorboard import SummaryWriter

logging.basicConfig(filename=r'data\log\training.log', level=logging.INFO)


env = Lilach()

model_path = r'data\model\car_model_Parallel.zip'
if os.path.isfile(model_path):
    model = PPO.load(model_path, env=env, device="cuda")
    logging.info("Loaded existing model.")
    print("Loaded existing model.")
else:
    model = PPO("MlpPolicy", env, verbose=1, device="cuda")
    print("Loaded new model.")

obs, info = env.reset()
screen = pygame.display.set_mode((800, 600))
env.screenNow(screen)

n_steps = 0
train_interval = 100000

timestamp = time.strftime("%Y%m%d-%H%M%S")
tb_writer = SummaryWriter(f'runs/{timestamp}')

# Initialize logging
logging.basicConfig(filename='data/log/training.log', level=logging.INFO)

# Create a CSV file to log rewards and episode lengths
csv_file = open('data/log/training_metrics.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['step', 'reward', 'episode_length'])  # Header



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    action, _states = model.predict(obs)
    obs, reward, done, truncated, info = env.step(action)
    env.render(reward)

    n_steps += 1

    if n_steps % train_interval == 0:
        
        model.learn(total_timesteps=train_interval)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        
        logging.info(f"Trained for {train_interval} steps.")
        print(f"Trained for {train_interval} steps.")
        logging.info(f"Model saved as {env.Name()}.zip")
        print(f"Model saved as {env.Name()}.zip")
        model.save(rf'Model saved as {env.Name()}.zip')

        obs, info = env.reset()

    if done:
        obs, info = env.reset()
        n_steps = 0