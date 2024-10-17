import vectorMath as VM
import numpy as np
import car
import pygame
import random
import gymnasium as gym
import math
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

        self.action_space = gym.spaces.MultiDiscrete([2, 3])  
        self.observation_space = gym.spaces.Box(
                    #    CarX    CarY   V   R   S   TX          TY   D       A    LX  LY
        low=np.array([-np.inf, -np.inf, -1, 0, -1, -np.inf, -np.inf, 0,      0, -1, -1], dtype=np.float32),
        high=np.array([np.inf,  np.inf,  1, 1,  1,  np.inf,  np.inf, np.inf, 1,  1,  1], dtype=np.float32),
        dtype=np.float32)
        
        pygame.init()
        self.screen = 0
        self.steps = 0

        self.car = car.Car(VM.Vector2(300, 300), VM.Vector2(30, 100))
        self.target_point = VM.Vector2(500, 300)
        self.distance = (self.car.position - self.target_point).magnitude()
        self.prev_distance = self.distance  

    def step(self, action, type = "A"):
        if isinstance(action, tuple):
            action = action[0]

        self.steps += 1
        throttle = action[0]
        steer = action[1] - 1

        dt = 0.016
        if (type == "A"):
            self.car.handleAIInput(dt, throttle, steer)
        elif (type == "H"):
            self.car.handleInput(dt)
        else:
            self.car.handleAIInput(dt, throttle, steer)

        
        self.car.Update(dt)
        
        obs = self._get_observation()
        done = self.check_done()
        reward = self.calculate_reward()
        truncated = False

        distanceVect = (self.target_point - self.car.position)
        TargetDistance = distanceVect.magnitude()

        return obs, reward, done, truncated, {"Distance": TargetDistance, "Action": action}

    def reset(self, seed=None, options=None):
        self.car = car.Car(VM.Vector2(960, 540), VM.Vector2(30, 100))
        self.car.rotation = random.randint(0, 360) 
        distance = 300
        self.rangle =0 #random.randint(-5, 5)
        x = distance * math.cos(math.radians(self.car.rotation - 90 + self.rangle))
        y = distance * math.sin(math.radians(self.car.rotation - 90 + self.rangle))
        self.target_point = VM.Vector2(960 + x, 540 + y)
        
        
        self.distance = (self.car.position - self.target_point).magnitude()
        
        self.prev_distance = self.distance 
        self.prev_rpm = 0  
        self.prev_rot = 0
        self.steps= 0
        
        return self._get_observation(), {}

    
    def _get_observation(self):
        
        Car = self.car

        CarX = Car.position.x
        CarY = Car.position.y

        CarRotation = Car.rotation
        CarRotation = ((CarRotation%360)/360)

        CarVelocity = Car.velocity.magnitude()
        if Car.velocity.y > 0:
            CarVelocity *= -1
        else:
            CarVelocity *= +1

        CarVelocity /= Car.MaxSpeed

        if(self.car.steerAngle > 270):
            CarSteer = self.car.steerAngle - 360
        else:
            CarSteer = self.car.steerAngle
        CarSteer = CarSteer/Car.MaxSteer

        TargetX = self.target_point.x
        TargetY = self.target_point.y

        distanceVect = (self.target_point - Car.position)
        TargetDistance = distanceVect.magnitude()
        
                
        CarFace = (Car.dir - Car.position)
        TragetAngle = distanceVect.angle_between(CarFace)
        TragetAngle = ((TragetAngle%360)/360)

        localVector = (Car.position).global_to_local(self.target_point, Car.rotation)
        localVector = localVector.normalize()

        LocalX = round(localVector.x, 4)
        LocalY = round(localVector.y, 4)

        return np.array([
            CarX,
            CarY,
            CarVelocity,  # Normalized
            CarRotation,  # Normalized
            CarSteer,     # Normalized 

            TargetX,
            TargetY,
            TargetDistance,
            TragetAngle,  # Normalized

            LocalX,       # Normalized
            LocalY        # Normalized  

        ], dtype=np.float32)

    def calculate_reward(self):
        Reward = 0

        distanceVect = (self.target_point - self.car.position)
        distance = distanceVect.magnitude()
        deltaDistance = self.prev_distance - distance

        velocityVect = self.car.velocity
        carNormal = (self.car.dir - self.car.position)
        angle = distanceVect.angle_between(carNormal)

        localVector = (self.car.position).global_to_local(self.target_point, self.car.rotation)
        localVector = localVector.normalize()
        stangle = 0
        if(self.car.steerAngle > 270):
            stangle = self.car.steerAngle - 360
        else:
            stangle = self.car.steerAngle

        
        self.prev_distance = distance

        if deltaDistance > 0:
            distcoeff = deltaDistance/2
        else:
            distcoeff = 0 

        speed_reward = max(0, velocityVect.magnitude()) 

        if angle <= 30:
            if velocityVect.y < 0:   
                Reward += ((30 - angle)) * 0.3
                Reward += ((speed_reward/2) * distcoeff * ((30 - angle)) * 0.3 )/10
        else:
            if (localVector.x > 0 and (stangle > 0)):
                Reward += stangle/5
                Reward += ((speed_reward/2) * distcoeff)/10
            elif (localVector.x < 0 and (stangle < 0)):
                Reward -= stangle/5
                Reward += ((speed_reward/2) * distcoeff)/10

        if (localVector.x <= 0 and (stangle > 0)):
            Reward -= ((abs(stangle)/4) * 5)
        elif (localVector.x >= 0 and (stangle < 0)):
            Reward -= ((abs(stangle)/4) * 5)


        if self.check_done():
            Reward += 8000
            print(f"Done, Pos({self.target_point.x}, {self.target_point.y}, Angle: {self.rangle})")

        if self.steps > 8000:
            Reward -= 8000
            print(f"Failed")
            self.reset()

        distanceVect = (self.target_point - self.car.position)
        TargetDistance = distanceVect.magnitude()

        if TargetDistance > 2000:
            Reward -= 800
            self.reset()
            print(f"Reset")        

        return Reward

    def screenNow(self, screen):
        self.screen = screen    

    def render(self, reward, Obs, mode='human'):
        self.screen.fill((255, 255, 255))

        pygame.draw.line(self.screen, (0, 255, 0), (self.car.position.x, self.car.position.y), (self.target_point.x, self.target_point.y), 2)
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.target_point.x), int(self.target_point.y)), 10)
        distanceVect = (self.target_point - self.car.position)
        velocityVect = self.car.velocity
        carNormal = (self.car.dir - self.car.position)
        angle = distanceVect.angle_between(carNormal)


        self.car.Draw(self.screen)
        self.car.debugDraw(self.screen, reward, Obs)
                
        pygame.display.flip()

    def check_done(self):
        distance = (self.car.position - self.target_point).magnitude()
        return distance < 15

    def Name(self):
        return "Lilach"