import vectorMath as VM
import numpy as np
import car
import pygame
import random
import gymnasium as gym

class Lilach(gym.Env):

    def __init__(self):
        super(Lilach, self).__init__()

        self.action_space = gym.spaces.MultiDiscrete([3, 2, 3, 2, 3])  
        self.observation_space = gym.spaces.Box(
                     low=np.array([-np.inf, -np.inf, 0, -np.inf, 0, 1, -np.inf, -np.inf, 0]),
                     high=np.array([np.inf, np.inf, np.inf, np.inf, 2, np.inf, np.inf, np.inf, np.inf]),  
                     dtype=np.float32
                    )

        pygame.init()
        self.screen = 0
        self.clock = pygame.time.Clock()

        self.car = car.Car(VM.Vector2(400, 300), VM.Vector2(30, 100))
        self.target_point = VM.Vector2(500, 300)
        self.distance = (self.car.position - self.target_point).magnitude()
        self.prev_distance = self.distance  
        self.prev_rpm = 0  

        self.prev_rot = 0
        self.step_count = 0  

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
        #self.car.handleInput(dt)
        self.car.Update(dt)

        self.step_count += 1

        reward = self.calculate_reward()
        done = self.check_done()
        obs = self._get_observation()

        truncated = False


        return obs, reward, done, truncated, {}

    def reset(self, seed=None, options=None):
        self.target_point = VM.Vector2(random.randint(100, 700), 300)
        self.car = car.Car(VM.Vector2(300, 300), VM.Vector2(30, 100))
        self.distance = (self.car.position - self.target_point).magnitude()
        self.prev_distance = self.distance 
        self.prev_rpm = 0  
        self.prev_rot = 0
        
        self.step_count = 0
        return self._get_observation(), {}

    def screenNow(self, screen):
        self.screen = screen    

    def render(self, reward, mode='human'):
        self.screen.fill((255, 255, 255))

        pygame.draw.line(self.screen, (0, 255, 0), (self.car.position.x, self.car.position.y), (self.target_point.x, self.target_point.y), 2)
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.target_point.x), int(self.target_point.y)), 10)
        
        
        self.car.Draw(self.screen)
        self.car.debugDraw(self.screen, reward)
        
        
        pygame.display.flip()

    def _get_observation(self):
        pos = self.car.position
        vel_mag = self.car.velocity.magnitude()
        rotation = self.car.rotation
        gear = self.car.gear
        rpm = self.car.CurRPM

        distance_to_target = (self.car.position - self.target_point).magnitude()

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
        return distance < 10

    def Name(self):
        return "Lilach"
    

class LilachV2(gym.Env):
    def __init__(self):
        super(LilachV2, self).__init__()

        self.action_space = gym.spaces.MultiDiscrete([3, 2, 3, 2])  
        self.observation_space = gym.spaces.Box(
                low=np.array([-np.inf, -np.inf, 0, 0, 0, -np.inf, -np.inf, 0, 0], dtype=np.float16),  
                high=np.array([np.inf, np.inf, 360, np.inf, np.inf, np.inf, np.inf, np.inf, 360], dtype=np.float16), 
                dtype=np.float16
            )

        
        pygame.init()
        self.screen = 0

        self.car = car.Car(VM.Vector2(400, 300), VM.Vector2(30, 100))
        self.target_point = VM.Vector2(500, 300)
        self.distance = (self.car.position - self.target_point).magnitude()
        self.prev_distance = self.distance  
        self.prev_rpm = 0  

        self.prev_rot = 0
        self.step_count = 0  

    def step(self, action):
        if isinstance(action, tuple):
            action = action[0]

        throttle = action[0] - 1
        brake = action[1]
        steer = action[2] - 1
        reverse_gear = action[3]

        self.step_count+= 1

        dt = 0.016
        self.car.handleAIInput(dt, throttle, brake, steer, reverse_gear, 2)
        #self.car.handleInput(dt)
        
        self.car.Update(dt)

        reward = self.calculate_reward()
        done = self.check_done()
        obs = self._get_observation()
        truncated = False

        return obs, reward, done, truncated, {}

    def reset(self, seed=None, options=None):
        self.target_point = VM.Vector2(random.randint(100, 1800), 300)
        self.car = car.Car(VM.Vector2(300, 300), VM.Vector2(30, 100))
        self.distance = (self.car.position - self.target_point).magnitude()
        
        self.prev_distance = self.distance 
        self.prev_rpm = 0  
        self.prev_rot = 0
        self.step_count = 0
        
        return self._get_observation(), {}

    
    def _get_observation(self):
        pos = self.car.position
        vel_mag = self.car.velocity.magnitude()
        rotation = self.car.rotation
        rpm = self.car.CurRPM

        distance_to_target = (self.car.position - self.target_point).magnitude()
        vec1 = (self.target_point-self.car.position)
        vec2 = (self.car.dir- self.car.position)
        cangle = vec1.angle_between(vec2)

        return np.array([
            pos.x,          
            pos.y,          
            rotation,       
            vel_mag,        
            rpm,

            self.target_point.x,
            self.target_point.y,
            distance_to_target,
            cangle,
        ], dtype=np.float16)

    def calculate_reward(self):
        Reward = 0

        distance = (self.car.position - self.target_point).magnitude()

        if distance < self.prev_distance:
            Reward += self.prev_distance - distance
            Reward += self.car.velocity.magnitude()/10
        else:
            Reward -= distance
        
        self.prev_distance = distance
        if self.check_done():
            Reward += 1000

        print(int(Reward))
        return int(Reward)
    
    def screenNow(self, screen):
        self.screen = screen    

    def render(self, reward, mode='human'):
        self.screen.fill((255, 255, 255))

        pygame.draw.line(self.screen, (0, 255, 0), (self.car.position.x, self.car.position.y), (self.target_point.x, self.target_point.y), 2)
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.target_point.x), int(self.target_point.y)), 10)

        self.car.Draw(self.screen)
        self.car.debugDraw(self.screen, reward)
                
        pygame.display.flip()

    def check_done(self):
        distance = (self.car.position - self.target_point).magnitude()
        return distance < 10

    def Name(self):
        return "Lilach"