from stable_baselines3 import PPO, A2C
import pygame
import os
import sys
from model import Lilach, LilachV2

env = LilachV2()

model_path = r'data\model\Best1.zip'
if os.path.isfile(model_path):
    model = PPO.load(model_path, env=env, device="cuda")
    print("Loaded existing model.")
else:
    model = PPO("MlpPolicy", env, verbose=1, device="cuda", gamma=0.5)
    print("Loaded new model.")

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

obs, info = env.reset()
screen = pygame.display.set_mode((1920, 1080))  
env.screenNow(screen)
clock = pygame.time.Clock()
type = "A"
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_r:
                env.reset()
            if event.key == pygame.K_t:
                if type == "A":
                    type = "H"
                elif (type == "H"):
                    type = "A"
                else:
                    type = "A"


    action, _states = model.predict(obs)
    obs, reward, done, truncated, info = env.step(action, type)
    env.render(reward, obs)

    #log_data(log_path, obs, action, reward, info)

    if info["Distance"] > 1500:
        env.reset()
    if done:
        obs, info = env.reset()
    
    clock.tick(60)