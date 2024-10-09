
import vectorMath as VM
import physics as phy
import pygame
import math

clock = pygame.time.Clock()
RED = (255, 0, 0)
BLUE = (0, 0, 255)



class Car(phy.RigidBody2D): 

    def __init__(self, position = VM.Vector2(0, 0), dimensions = VM.Vector2(30, 100), mass = 1):
        super().__init__(position, dimensions, mass)
        self.steerAngle = 0
        self.MaxSteer = 50

        self.MaxSpeed = 300

        self.CurRPM = 0
        self.MaxRPM =1500


        self.DriftMomentum = VM.Vector2()
        self.traction = 0.01
        self.lateraldir = VM.Vector2()


        self.dv= VM.Vector2()

        self.fac = 0


    def TireUpdate(self):
        xx = self.position.x
        yy = self.position.y

        ww = self.dimensions.x
        hh = self.dimensions.y

        self.dir = VM.Vector2(xx, yy-hh/3)
        self.dir.rotate(self.position, self.rotation)

        self.dir2 = VM.Vector2(self.dir.x, self.dir.y-hh/4)
        

    def Update(self, dt):
        self.steerAngle %= 360
        self.handleInput(dt)
        #self.applyDrift(0)
        self.TireUpdate()
        self.PhyUpdate(dt)
        #print(self.lateraldir)

    def applyDrift(self, dir, dt):

        #if(not self.velocity.magnitude() > 300): return
        forward_dir = (self.position - self.dir).normalize()
        
        if(dir == 1  ):   
            self.lateraldir.x = VM.Lerp(self.lateraldir.x, -forward_dir.y, 5* dt)
            self.lateraldir.y = VM.Lerp(self.lateraldir.y, forward_dir.x, 5* dt)

        elif(dir == -1):
            
            self.lateraldir.x = VM.Lerp(self.lateraldir.x, forward_dir.y, 5* dt)
            self.lateraldir.y = VM.Lerp(self.lateraldir.y, -forward_dir.x, 5* dt)

        elif(dir==78):
            self.lateraldir.x = VM.Lerp(self.lateraldir.x, 0, 3* dt)
            self.lateraldir.y = VM.Lerp(self.lateraldir.y, 0, 3* dt)
    

        self.DriftMomentum = self.lateraldir * self.velocity.magnitude() 
        accleration = self.lateraldir * self.DriftMomentum.magnitude()

        velocity = VM.Vector2()

        d = 50 if (self.velocity.magnitude() < 300) else (20 if (self.velocity.magnitude() < 370) else 3)
        self.fac = VM.Lerp(self.fac, d, 3* dt)

        velocity += (accleration * dt)*self.velocity.magnitude() * (1/ self.fac)
        velocity *= (1 - self.traction)
        self.position += velocity * dt 


    def handleInput(self, dt):
        keys = pygame.key.get_pressed()
        self.drag = 0.05

        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) or (keys[pygame.K_w] or keys[pygame.K_UP]) and (not keys[pygame.K_SPACE]):
            if keys[pygame.K_w] or keys[pygame.K_UP] and self.velocity.magnitude() < self.MaxSpeed:
                self.acclerate(-1, dt)
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                if self.velocity.magnitude() < self.MaxSpeed - 50:
                    self.acclerate(1, dt)
        elif(keys[pygame.K_SPACE]):
            self.drag = 0.055
            self.redRPM(dt, 3)
        else:
            self.drag = 0.05
            self.redRPM(dt, 1)

        if keys[pygame.K_d] or keys[pygame.K_RIGHT] or keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.rotation += 120 * (self.velocity.magnitude() / 300) * dt * (-1 if keys[pygame.K_s] or keys[pygame.K_DOWN] else 1)
                self.steer(1, dt)
                if((not keys[pygame.K_s] or not keys[pygame.K_DOWN]) ):#and (keys[pygame.K_SPACE]
                    self.applyDrift(1, dt)
                else:
                    self.applyDrift(78, dt)


            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.rotation -= 120 * (self.velocity.magnitude() / 300) * dt * (-1 if keys[pygame.K_s] or keys[pygame.K_DOWN] else 1)
                self.steer(-1, dt)
                if((not keys[pygame.K_s] or not keys[pygame.K_DOWN]) ):#and (keys[pygame.K_SPACE])):
                    self.applyDrift(-1, dt)
                else:
                    self.applyDrift(78, dt)
        else:
            self.antisteer(dt)
            self.applyDrift(78, dt)


    def steer(self, angDir, dt):
        if(self.steerAngle < self.MaxSteer-5 or self.steerAngle > 360-self.MaxSteer+5):
            self.steerAngle += 90 * dt * angDir

    def antisteer(self, dt):
        if(abs(self.steerAngle)!= 0):
            if(self.steerAngle <= self.MaxSteer):
                self.steerAngle -= 190 * dt
            if(self.steerAngle >= 360-self.MaxSteer):
                self.steerAngle += 90 * dt
            

    def acclerate(self, dir, dt):
        self.CurRPM = VM.Lerp(self.CurRPM, self.MaxRPM, 1*dt)
        force = dir * self.CurRPM
        self.addForce(VM.Vector2(0, force))

    def redRPM(self,dt, factor):
        self.CurRPM = VM.Lerp(self.CurRPM, 0, factor*dt)
    

    def Draw(self, screen):
        image = pygame.image.load('assets\Cars\Red.png')
        vertices = self.findVertices()
        points = [(int(v.x), int(v.y)) for v in vertices]

        polygon_center = [(points[0][0] + points[2][0]) // 2, (points[0][1] + points[2][1]) // 2]


        image = pygame.transform.scale(image, (self.dimensions.x, self.dimensions.y -  self.dimensions.y/4))


        rotated_image = pygame.transform.rotate(image, 180-self.rotation)
        new_rect = rotated_image.get_rect(center=polygon_center)#(self.position.x, self.position.y))



        screen.blit(rotated_image, new_rect.topleft)


    def debugDraw(self, screen):
        font = pygame.font.SysFont('Arial', 30)
        text_surface = font.render(f"Speed: {self.velocity.magnitude() :5.1f} RPM: {self.CurRPM :5.0f}", True, (0, 0, 0))  # Render the text
        screen.blit(text_surface, (10, 10))

        vertices = self.findVertices()
        points = [(int(v.x), int(v.y)) for v in vertices]
        pygame.draw.polygon(screen, RED, points, 2)

        pygame.draw.line(screen, (255, 0, 255), (self.position.x, self.position.y), (self.position.x + self.lateraldir.x*self.DriftMomentum.magnitude() *(1/6), self.position.y + self.lateraldir.y*self.DriftMomentum.magnitude()*(1/6)))
        pass
        
        pygame.draw.line(screen, BLUE, (self.position.x, self.position.y) , (self.dir.x, self.dir.y))

        self.dir2.rotate(self.dir, self.steerAngle + self.rotation)

        pygame.draw.line(screen, (0, 0, 0), (self.dir.x, self.dir.y), (self.dir2.x, self.dir2.y), 2)


    def re(self):
        return (self.dir - self.position).angle_between(self.dir2- self.position)
    
    def forwarddir(self):
        
        t=  VM.Vector2(math.cos(math.radians(self.rotation)), math.sin(math.radians(self.rotation)))
        return str(t)
