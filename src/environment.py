import gymnasium as gym
from stable_baselines3 import PPO
import numpy as np
import pygame
import car
import vectorMath as VM
import os
import time
import logging
import random  # Import to randomize the x-coordinate for the target
import sys



# Setup logging
logging.basicConfig(filename=r'data\log\training.log', level=logging.INFO)

class CarEnv(gym.Env):
    def __init__(self):
        super(CarEnv, self).__init__()

        self.action_space = gym.spaces.MultiDiscrete([3, 2, 3, 2, 3])  # throttle, brake, steer, reverse_gear, gear
        self.observation_space = gym.spaces.Box(
                     low=np.array([-np.inf, -np.inf, 0, -np.inf, 0, 1, -np.inf, -np.inf, 0]),  # Added RPM to low bounds
                     high=np.array([np.inf, np.inf, np.inf, np.inf, 2, np.inf, np.inf, np.inf, np.inf]),  # Added RPM to high bounds
                     dtype=np.float32
                    )

        pygame.init()
        self.screen = 0
        self.clock = pygame.time.Clock()

        self.car = car.Car(VM.Vector2(400, 300), VM.Vector2(30, 100))
        self.target_point = VM.Vector2(500, 300)
        self.distance = (self.car.position - self.target_point).magnitude()
        self.prev_distance = self.distance  # Initialize previous distance
        self.prev_rpm = 0  # Track previous RPM for reward calculation

        self.prev_rot = 0
        self.step_count = 0  # Track the number of steps

    def step(self, action):
        if isinstance(action, tuple):
            action = action[0]

        throttle = action[0] - 1
        brake = action[1]
        steer = action[2] - 1
        reverse_gear = action[3]
        gear = action[4]

        dt = 0.016
        self.car.handleAIInput(dt, throttle, brake, steer, reverse_gear, int(gear))
        #0self.car.handleInput(dt)
        self.car.Update(dt)

        self.step_count += 1  # Increment the step counter

        reward = self.calculate_reward()
        done = self.check_done()
        obs = self._get_observation()

        truncated = False  # Update this logic if needed


        return obs, reward, done, truncated, {}

    def reset(self, seed=None, options=None):
        self.target_point = VM.Vector2(random.randint(100, 700), 300)  # Randomize x, y stays 300
        self.car = car.Car(VM.Vector2(300, 300), VM.Vector2(30, 100))
        self.distance = (self.car.position - self.target_point).magnitude()
        self.prev_distance = self.distance  # Reset previous distance
        self.prev_rpm = 0  # Reset RPM
        self.prev_rot = 0
        
        self.step_count = 0  # Reset the step count on reset
        return self._get_observation(), {}

    def screenNow(self, screen):
        self.screen = screen    

    def render(self, reward, mode='human'):
        self.screen.fill((255, 255, 255))

        vec = (self.target_point - self.car.position)
        pygame.draw.line(self.screen, (0, 255, 0), (self.car.position.x, self.car.position.y), (self.target_point.x, self.target_point.y), 2)


        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.target_point.x), int(self.target_point.y)), 10)
        self.car.Draw(self.screen)
        self.car.debugDraw(self.screen, reward)
        pygame.display.flip()
        self.clock.tick(60)

    def _get_observation(self):
        pos = self.car.position
        vel_mag = self.car.velocity.magnitude()
        rotation = self.car.rotation
        gear = self.car.gear
        rpm = self.car.CurRPM  # Assuming the car object has an RPM attribute

        distance_to_target = (self.car.position - self.target_point).magnitude()

        # Include target coordinates and RPM in the observation
        return np.array([
            pos.x,          # x position
            pos.y,          # y position
            vel_mag,        # velocity magnitude
            rotation,       # rotation angle
            gear,           # current gear
            distance_to_target,  # distance to target
            self.target_point.x,  # target x position
            self.target_point.y,  # target y position
            rpm             # RPM
        ], dtype=np.float32)

    def calculate_reward(self):
        distance = (self.car.position - self.target_point).magnitude()
        rew = 0
        rew += int((self.prev_distance - distance) * 10)
        rpm = self.car.CurRPM 
        if rpm > self.prev_rpm:
            rew += (rpm - self.prev_rpm) * 2 
            
        vec1 = (VM.Vector2(self.target_point.x - self.car.position.x, self.target_point.y - self.car.position.y).normalize())
        vec2 = (((self.car.dir- self.car.position)*100).normalize())
        cangle = vec1.angle_between(vec2)

        rew - cangle * 10

        if distance > self.prev_distance:
            pass
        else:
            rew += int(self.car.velocity.magnitude()) * 2
            
            self.prev_distance = distance

        self.prev_rpm = rpm  

        if self.check_done():
            rew += 2000

        return rew

    def check_done(self):
        distance = (self.car.position - self.target_point).magnitude()
        return distance < 8  # Finish when within 8 units of the target


# Create the environment
env = CarEnv()

# Load existing model if it exists
model_path = r'data\model\car_model_.zip'
if os.path.isfile(model_path):
    model = PPO.load(model_path, env=env)
    logging.info("Loaded existing model.")
    print("Loaded existing model.")
else:
    model = PPO("MlpPolicy", env, verbose=1)
    print("Loaded new model.")

# Train the model
#model.learn(total_timesteps=10000)

# Test the model
obs, info = env.reset()
screen = pygame.display.set_mode((800, 600))
env.screenNow(screen)

n_steps = 0
train_interval = 10000  # Number of steps after which training is performed
while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    action, _states = model.predict(obs)
    obs, reward, done, truncated, info = env.step(action)
    env.render(reward)

    n_steps += 1

    if (reward < -1000):
        # Save the model using the current timestamp
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        # Reset the environment
        obs, info = env.reset()
        n_steps = 0  # Reset step counter for the new episode

    # Train the model after a certain number of steps
    if n_steps % train_interval == 0:
        model.learn(total_timesteps=train_interval)  # Perform a training step
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        logging.info(f"Trained for {train_interval} steps.")
        print(f"Trained for {train_interval} steps.")
        logging.info(f"Model saved as car_model_{timestamp}.zip")
        print(f"Model saved as car_model_{timestamp}.zip")
        model.save(r'data\model\car_model_.zip')
        obs, info = env.reset()


    # Check if the episode is done
    if done:
        # Save the model using the current timestamp
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        # Reset the environment
        obs, info = env.reset()
        print(obs)
        print(info)
        n_steps = 0  # Reset step counter for the new episode