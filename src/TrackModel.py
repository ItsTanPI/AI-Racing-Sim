import vectorMath as VM
import numpy as np
import car
import pygame
import random
import gymnasium as gym
import math
import Raycast as ray
import TrackGenerator

class Decan(gym.Env):
    def __init__(self):
        super(Decan, self).__init__()

        rays = 8

        RayLow = [0 for i in range(rays)]
        RayHigh = [1 for i in range(rays)]
        

        self.action_space = gym.spaces.MultiDiscrete([2, 3])  
        self.observation_space = gym.spaces.Box(
                    #     V   S
        low=np.array([ -1, -1, ] + RayLow, dtype=np.float32),
        high=np.array([ 1,  1, ] + RayHigh, dtype=np.float32),
        dtype=np.float32)
        
        
        
        pygame.init()

        self.RayCast = []
        angle = 0
        for i in range(rays):
            line = ray.RayCast(VM.Vector2(300, 100), angle,200)
            self.RayCast.append(line)
            angle+=(360/8)


        self.CollisionInt = [False for i in range(len(self.RayCast))]

        self.screen = 0
        self.steps = 0
        self.car = car.Car(VM.Vector2(300, 300), VM.Vector2(30, 100))
        self.CarRay = ray.RayCast(self.car.position, -90, 20) 

        self.centered_track, self.inflated_track = ( [VM.Vector2(372.97078673872534, 598.7614370922374), VM.Vector2(422.10196697998197, 364.92408757601424), VM.Vector2(492.1517570782935, 198.09479774849905), VM.Vector2(657.9471713018057, 155.86112881208453), VM.Vector2(955.4317609547857, 149.42277455560037), VM.Vector2(1200.528786825163, 152.90208448232596), VM.Vector2(1589.4624902306825, 211.08240636809506), VM.Vector2(1735.350121743476, 385.44082000777473), VM.Vector2(1719.5180346051184, 794.7202468053138), VM.Vector2(1540.0135284346643, 868.1490329773305), VM.Vector2(1373.3699274007356, 891.7593650699018), VM.Vector2(891.7062111115587, 910.3051205331303), VM.Vector2(597.4917991716743, 919.5417975454379), VM.Vector2(477.0486436218857, 876.2748767009373), VM.Vector2(374.90701380144986, 622.7600237253167)] ,  [VM.Vector2(223.71668198617283, 613.7017253931398), VM.Vector2(279.46706259378334, 318.49905068060633), VM.Vector2(371.0450743245858, 109.58959229484904), VM.Vector2(565.2304014384641, 37.94759868891272), VM.Vector2(953.6774625803093, -0.5669665509610127), VM.Vector2(1279.6952473586157, 25.494582636456315), VM.Vector2(1722.4066772033157, 141.61411755812412), VM.Vector2(1882.4558323297715, 356.11659942305954), VM.Vector2(1861.7333583744605, 842.4151279266795), VM.Vector2(1670.56754193433, 942.0114020100737), VM.Vector2(1487.6069502385656, 988.9699746408181), VM.Vector2(864.5011452227405, 1057.8174399847105), VM.Vector2(493.88779642865734, 1028.013962710631), VM.Vector2(353.94976298765107, 961.9875687984235), VM.Vector2(226.3854237048119, 643.7680525516072)] )

        self.Checkpoints = [[self.centered_track[i], self.inflated_track[i], False] for i in range(len(self.centered_track))]
        self.Checkpoints[1][2] = True
    
    def step(self, action, type = "A"):
        if isinstance(action, tuple):
            action = action[0]

        self.steps += 1
        throttle = action[0]
        steer = action[1] - 1

        dt = 0.016




        if (type == "A"):
            self.car.handleAIInput(dt, throttle, steer, gear=2)
        elif (type == "H"):
            self.car.handleInput(dt)
        else:
            self.car.handleAIInput(dt, throttle, steer, gear=2)
        self.CollisionInt = []
        for line in self.RayCast:
            line.Update(self.car.position, self.car.rotation, 0.016)
            intersection = line.Collision([self.centered_track,self.inflated_track])
            self.CollisionInt.append(intersection)
            if intersection:
                dist = (self.car.position - intersection).magnitude()

        
        self.car.Update(dt)
        

        
        obs = self._get_observation()
        reward = self.calculate_reward()
        truncated = False

        done = False
        dist = 0
        for i in range(len(self.CollisionInt)):
            if self.CollisionInt[i]:
                dist = ((self.CollisionInt[i] - self.car.position).magnitude())
                if dist < 5:
                    done = True
                    reward -= 50
                    print("Failed")
                    break

                
                    




        return obs, reward, done, truncated, { "Action": action}

    def reset(self, seed=None, options=None):

        c = TrackGenerator.GoToCenter(self.centered_track[0], self.centered_track[1], self.inflated_track[0], self.inflated_track[1])

        self.car = car.Car(c, VM.Vector2(30, 100))
        self.car.rotation = TrackGenerator.Angle(self.centered_track[0], self.centered_track[1])
        self.Checkpoints = [[self.centered_track[i], self.inflated_track[i], False] for i in range(len(self.centered_track))]
        self.Checkpoints[1][2] = True

        return self._get_observation(), {}
    
    def NewTrack(self):
        self.centered_track, self.inflated_track = TrackGenerator.generateTrack()

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

        CarVelocity /= 456#Car.MaxSpeed

        if(self.car.steerAngle > 270):
            CarSteer = self.car.steerAngle - 360
        else:
            CarSteer = self.car.steerAngle
        CarSteer = CarSteer/(Car.MaxSteer-5) 

        rayObs = []
        for i in range(len(self.CollisionInt)):
            if self.CollisionInt[i]:
                dist = ((self.CollisionInt[i] - self.car.position).magnitude())/(self.RayCast[i].Distance)

                rayObs.append(round(dist, 2))
            else:
                self.RayCast[i].Update(self.car.position, self.car.rotation, 0.016)
                dist = ((self.RayCast[i].End - self.car.position).magnitude())/(self.RayCast[i].Distance)

                rayObs.append(round(dist, 2))


        return np.array(([
            CarVelocity,  # Normalized
            CarSteer,     # Normalized

        ] + rayObs), dtype=np.float32)

    def calculate_reward(self):

        Reward = 0
        Reward += self.car.velocity.magnitude()//10
        self.CarRay.Update(self.car.position, self.car.rotation, 0.016)        
        
        for i in range(len(self.Checkpoints)):
            s, e, b = self.Checkpoints[i]
            if b:
                collide = ray.line_intersection(self.CarRay.Start.rTuple(), self.CarRay.End.rTuple(), s.rTuple(), e.rTuple())
                self.Checkpoints[i][2] = False if collide else True
                if collide:
                    print(i, "Done")
                    Reward += 100 if collide else 0
                    new = (i+1)%len(self.Checkpoints)
                    self.Checkpoints[new][2] = True


        return Reward

    def screenNow(self, screen):
        self.screen = screen    

    def render(self, reward, Obs,fps = 0, mode='human'):
        self.screen.fill((179, 114, 68))

        pygame.draw.polygon(self.screen, (169, 169, 169), [(v.x, v.y) for v in self.inflated_track])
        pygame.draw.polygon(self.screen, (76, 175, 80), [(v.x, v.y) for v in self.centered_track])
        
        self.car.Draw(self.screen)
        if(mode == "Debug"):
            for i in range(len(self.Checkpoints)):
                s, e, b = self.Checkpoints[i]
                if b:
                    pygame.draw.line(self.screen, (0, 0, 255), (s.x, s.y), (e.x, e.y), 2)


            for i in range(len(self.RayCast)):
                self.RayCast[i].Draw(self.screen, self.CollisionInt[i])
        
            self.car.debugDraw(self.screen, reward, Obs, fps)
        
        pygame.display.flip()

    def check_done(self):
        return False

    def Name(self):
        return "Decan"