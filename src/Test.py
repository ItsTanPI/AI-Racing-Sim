from stable_baselines3 import PPO, A2C
import pygame
import os
import sys
from model import Lilach, LilachV2

env = LilachV2()

model_path = r'data\model\LilachV2_episode_2.zip'
if os.path.isfile(model_path):
    model = PPO.load(model_path, env=env, device="cuda")
    print("Loaded existing model.")
else:
    model = PPO("MlpPolicy", env, verbose=1, device="cuda")
    print("Loaded new model.")

obs, info = env.reset()
screen = pygame.display.set_mode((1920, 1080))  
env.screenNow(screen)
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    action, _states = model.predict(obs)
    obs, reward, done, truncated, info = env.step(action)
    env.render(reward)

    if done:
        obs, info = env.reset()