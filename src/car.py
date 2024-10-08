
import vectorMath as VM
import physics as phy
import pygame

clock = pygame.time.Clock()
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Car(phy.RigidBody2D): 

    def __init__(self, position = VM.Vector2(0, 0), dimensions = VM.Vector2(30, 100), mass = 1):
        super().__init__(position, dimensions, mass)
        self.steerAngle = 0
        self.MaxSteer = 50

        self.MaxSpeed = 250

        self.CurRPM = 0
        self.MaxRPM =1000

    def TireUpdate(self):
        xx = self.position.x
        yy = self.position.y

        ww = self.dimensions.x
        hh = self.dimensions.y

        self.dir = VM.Vector2(xx, yy-hh/3)
        self.dir.rotate(self.position, self.rotation)

        self.dir2 = VM.Vector2(self.dir.x, self.dir.y-hh/3)

    def Update(self, dt):
        self.steerAngle %= 360
        self.TireUpdate()
        self.handleInput(dt)        
        self.PhyUpdate(dt)



    def handleInput(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_s] or keys[pygame.K_DOWN] or keys[pygame.K_w] or keys[pygame.K_UP]:

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.acclerate(-1, dt)
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                if(self.velocity.magnitude()< self.MaxSpeed/2):
                    self.acclerate(1, dt)
        else:
            self.redRPM(dt)
    
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] or keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.rotation += 90 *self.velocity.magnitude()/200 * (dt) *  (-1 if keys[pygame.K_s] or keys[pygame.K_DOWN] else 1)
                self.steer(1)

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.rotation -= 90 *(self.velocity.magnitude()/200) * (dt) *(-1 if keys[pygame.K_s] or keys[pygame.K_DOWN] else 1)
                self.steer(-1)
        else:
            self.antisteer()


    def steer(self, angDir):
        if(self.steerAngle < self.MaxSteer-5 or self.steerAngle > 360-self.MaxSteer+5):
            self.steerAngle += 90 * 0.016 * angDir

    def antisteer(self):
        if(abs(self.steerAngle)!= 0):
            if(self.steerAngle <= self.MaxSteer):
                self.steerAngle -= 90 * 0.016
            if(self.steerAngle >= 360-self.MaxSteer):
                self.steerAngle += 90 * 0.016
            

    def acclerate(self, dir, dt):
        self.CurRPM = VM.Lerp(self.CurRPM, self.MaxRPM, 3*dt)
        force = dir * self.CurRPM
        self.addForce(VM.Vector2(0, force))

    def redRPM(self,dt):
        self.CurRPM = VM.Lerp(self.CurRPM, 0, 3*dt)

    def Draw(self, screen):
        vertices = self.findVertices()
        points = [(int(v.x), int(v.y)) for v in vertices]
        pygame.draw.polygon(screen, RED, points)

    def debugDraw(self, screen):
        pass
        
        pygame.draw.line(screen, BLUE, (self.position.x, self.position.y) , (self.dir.x, self.dir.y))

        self.dir2.rotate(self.dir, self.steerAngle + self.rotation)

        pygame.draw.line(screen, (0, 255, 0), (self.dir.x, self.dir.y), (self.dir2.x, self.dir2.y))
        pygame.draw.line(screen, (255, 255, 0), (self.position.x, self.position.y), (self.dir2.x, self.dir2.y))
    