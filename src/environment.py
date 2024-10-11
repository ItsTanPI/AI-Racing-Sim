import gymnasium as gym
from stable_baselines3 import PPO  
import numpy as np
import pygame
import car  # Ensure your car simulation code is accessible
import vectorMath as VM

import torch  # Import torch to check device

# Create the model with CUDA support
device = 'cuda' if torch.cuda.is_available() else 'cpu'

class CarEnv(gym.Env):
    def __init__(self):
        super(CarEnv, self).__init__()

        self.action_space = gym.spaces.MultiDiscrete([3, 2, 3, 2, 3])  # throttle, brake, steer, reverse_gear, gear
        self.observation_space = gym.spaces.Box(
                     low=np.array([-np.inf, -np.inf, 0, -np.inf, 0, 0, -np.inf, -np.inf]),  # Added low bounds for target coordinates
                     high=np.array([np.inf, np.inf, np.inf, np.inf, 2, np.inf, np.inf, np.inf]),  # Added high bounds for target coordinates
                     dtype=np.float32
                    )

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.car = car.Car(VM.Vector2(200, 200), VM.Vector2(30, 100))
        self.target_point = VM.Vector2(500, 500)
        self.distance = (self.car.position - self.target_point).magnitude()
        self.prev_distance = self.distance  # Initialize previous distance

    def step(self, action):
        if isinstance(action, tuple):
            action = action[0]

        throttle = action[0] - 1
        brake = action[1]
        steer = action[2] - 1
        reverse_gear = action[3]
        gear = action[4]

        dt = 0.016
        self.car.handleAIInput(dt, throttle, brake, steer, reverse_gear, 2)
        self.car.Update(dt)

        reward = self.calculate_reward()
        done = self.check_done()
        obs = self._get_observation()

        truncated = False  # Update this logic if needed

        return obs, reward, done, truncated, {}

    def reset(self, seed=None, options=None):
        self.target_point = VM.Vector2(500, 300)
        self.car = car.Car(VM.Vector2(200, 300), VM.Vector2(30, 100))
        self.distance = (self.car.position - self.target_point).magnitude()
        self.prev_distance = self.distance  # Reset previous distance
        return self._get_observation(), {}

    def render(self, mode='human'):
        self.screen.fill((255, 255, 255))
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.target_point.x), int(self.target_point.y)), 10)
        self.car.Draw(self.screen)
        self.car.debugDraw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

    def _get_observation(self):
        pos = self.car.position
        vel_mag = self.car.velocity.magnitude()
        rotation = self.car.rotation
        gear = self.car.gear

        distance_to_target = (self.car.position - self.target_point).magnitude()

        # Include target coordinates in the observation
        return np.array([
            pos.x,          # x position
            pos.y,          # y position
            vel_mag,        # velocity magnitude
            rotation,       # rotation angle
            gear,           # current gear
            distance_to_target,  # distance to target
            self.target_point.x,  # target x position
            self.target_point.y   # target y position
        ], dtype=np.float32)

    def calculate_reward(self):
        distance = (self.car.position - self.target_point).magnitude()
        rew = (self.prev_distance - distance)  # Reward based on change in distance

        # Penalize for moving backward
        if self.car.velocity.x > 5:
            rew +=10
        elif self.car.velocity.x > 10:
            rew +=20
        elif self.car.velocity.x > 15:
            rew +=40
        elif self.car.velocity.x > 20:
            rew +=100

        # Optional penalty for each step to encourage efficiency
        rew -= 0.01

        # Penalty for increasing distance to the target
        if distance > self.prev_distance:
            rew -= 10  # Adjust penalty as needed

        self.prev_distance = distance  # Update previous distance
        return rew

    def check_done(self):
        distance = (self.car.position - self.target_point).magnitude()
        return distance == 0

# Create the environment
env = CarEnv()

# Create the model
model = PPO("MlpPolicy", env, verbose=1)

# Train the model
model.learn(total_timesteps=10000)

# Test the model
obs, info = env.reset()
while not env.check_done():
    action = model.predict(obs)
    obs, reward, done, truncated, info = env.step(action)
    env.render()
    if done:
        obs, info = env.reset()
