from stable_baselines3 import PPO, A2C
import pygame
import os
import sys
from model import LilachV2

env = LilachV2()

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

model_path = r'data\model\LilachV4-1.zip'
if os.path.isfile(model_path):
    print("!!!!!!!!!!Loded Old!!!!!!!!!!!")
    model = PPO.load(model_path, env = env, verbose=2, device="cuda",
                            policy_kwargs = dict(net_arch=[128, 128, 64])
                    )
                          
    print("Loaded existing model.")
else:
    model = PPO("MlpPolicy", env, verbose=1, device="cuda")
    print("Loaded new model.")


print_hyperparameters(model)
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
font = pygame.font.SysFont("Arial", 18)
obs, info = env.reset()
screen = pygame.display.set_mode((1920, 1080))  
env.screenNow(screen)
clock = pygame.time.Clock()
type = "A"
while True:
    fps = clock.get_fps()
    fps_text = font.render(f'FPS: {int(fps)}', True, (0, 0, 0))
 
    screen.blit(fps_text, (540, 540))

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
    env.render(reward, obs, fps=fps)

    #log_data(log_path, obs, action, reward, info)

    if done:
        obs, info = env.reset()
    
    clock.tick(60)  