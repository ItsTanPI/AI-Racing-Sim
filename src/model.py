import vectorMath as VM
import numpy as np
import car
import pygame
import random
import gymnasium as gym
import math


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
        self.FirstDistance = self.distance

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
        reward = self.calculate_reward()
        truncated = False

        distanceVect = (self.target_point - self.car.position)
        TargetDistance = distanceVect.magnitude()

        done = ((self.steps > 750) or (TargetDistance > 2000) or (self.check_done()))


        return obs, reward, done, truncated, {"Distance": TargetDistance, "Action": action}

    def reset(self, seed=None, options=None):
        self.steps = 0
        self.car = car.Car(VM.Vector2(960, 540), VM.Vector2(30, 100))
        #self.car = car.Car(VM.Vector2(random.randint(150, 1800), random.randint(150, 850)))
        self.car.rotation = random.randint(0, 360) 
        distance = 200
        self.rangle =random.randint(-25, 25)
        x = distance * math.cos(math.radians(self.car.rotation - 90 + self.rangle))
        y = distance * math.sin(math.radians(self.car.rotation - 90 + self.rangle))
        self.target_point = VM.Vector2(960 + x, 540 + y)

        #self.target_point = VM.Vector2(random.randint(150, 1800), random.randint(150, 850))
        self.distance = (self.car.position - self.target_point).magnitude()
        self.prev_distance = self.distance 
        self.prev_rpm = 0  
        self.prev_rot = 0
        
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
        CarSteer = CarSteer/(Car.MaxSteer-5) 

        TargetX = self.target_point.x
        TargetY = self.target_point.y

        distanceVect = (self.target_point - Car.position)
        TargetDistance = distanceVect.magnitude()
        
                
        CarFace = (Car.dir - Car.position)
        TragetAngle = distanceVect.angle_between(CarFace)
        TragetAngle = ((TragetAngle%180)/180)

        localVector = (Car.position).global_to_local(self.target_point, Car.rotation)
        localVector = localVector.normalize()

        LocalX = round(localVector.x, 4)
        LocalY = round(localVector.y, 4)

        TragetAngle = TragetAngle if (LocalX > 0) else (-1* TragetAngle)

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

            LocalX,       # tells which side of the car the point is 
            LocalY        # Normalized  

        ], dtype=np.float32)

    def calculate_reward(self):
        Reward = 0

        distanceVect = (self.target_point - self.car.position)
        distance = distanceVect.magnitude()
        deltaDistance = int(self.prev_distance - distance)
        self.prev_distance = distance

        velocityVect = self.car.velocity
        carNormal = (self.car.dir - self.car.position)
        angle = distanceVect.angle_between(carNormal)

        localVector = (self.car.position).global_to_local(self.target_point, self.car.rotation)
        localVector = localVector.normalize()

        stangle = self.car.steerAngle - 360 if self.car.steerAngle > 270 else self.car.steerAngle

        stangle = 0
        if self.car.steerAngle > 270:
            stangle = self.car.steerAngle - 360
        else:
            stangle = self.car.steerAngle

        self.prev_distance = distance

        
        distcoeff = deltaDistance // 2 if deltaDistance > 0 else 0
        
        
        speed_reward = max(0, velocityVect.magnitude())
        distanceReward = (100*(self.FirstDistance - distance)/self.FirstDistance)//10

        AllignmentReward = int((180 - angle)//5)
        SpeedReward = (speed_reward//10) * distcoeff
        SteerReward = 0 
        if (localVector.y < 0):
            
            if (AllignmentReward >= 35):
                AllignmentReward += 75
            elif localVector.x <= 0 and stangle > 0:
                SteerReward -= 50
                SpeedReward = 0 
                AllignmentReward = 0
            elif localVector.x >= 0 and stangle < 0:
                SteerReward -= 50
                SpeedReward = 0
                AllignmentReward = 0
            elif localVector.x >= 0 and stangle > 0:
                SteerReward += (abs(stangle) //2) 
            elif localVector.x <= 0 and stangle < 0:
                SteerReward += (abs(stangle) //2) 
        else:
            SpeedReward = 0 
            distanceReward = 0
            AllignmentReward = 0
            if localVector.x <= 0 and stangle > 0:
                SteerReward -= 50
            elif localVector.x >= 0 and stangle < 0:
                SteerReward -= 50
            elif localVector.x >= 0 and stangle > 0:
                SteerReward += (abs(stangle) //2) 
            elif localVector.x <= 0 and stangle < 0:
                SteerReward += (abs(stangle) //2)
            else:
                SteerReward -= 50
        
        Reward = (SteerReward+ AllignmentReward) #+ (SpeedReward) + distanceReward)           
        
        if self.steps > 750 or distance > 2000:
            print(f"\nFailed,({self.steps}, Angle: {self.rangle}, Reward: {Reward/10})")
            Reward -= 50

        if self.check_done():
            Reward += 50    
            print(f"\nDone, Pos({self.target_point.x}, {self.target_point.y}), Angle: {self.rangle}, Reward: {Reward/10}")
        
        Reward /= 10

        return Reward


    def screenNow(self, screen):
        self.screen = screen    

    def render(self, reward, Obs,fps = 0, mode='human'):
        self.screen.fill((255, 255, 255))

        pygame.draw.line(self.screen, (0, 255, 0), (self.car.position.x, self.car.position.y), (self.target_point.x, self.target_point.y), 2)
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.target_point.x), int(self.target_point.y)), 10)
        distanceVect = (self.target_point - self.car.position)
        velocityVect = self.car.velocity
        carNormal = (self.car.dir - self.car.position)
        angle = distanceVect.angle_between(carNormal)


        self.car.Draw(self.screen)
        self.car.debugDraw(self.screen, reward, Obs, fps)
                
        pygame.display.flip()

    def check_done(self):
        distance = (self.car.position - self.target_point).magnitude()
        return distance < 15

    def Name(self):
        return "Lilach"