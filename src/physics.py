import vectorMath as VM

class RigidBody2D:

    Bodies = list()

    def __init__(self, position, dimensions, mass = 1):
        
        self.position = position                    
        self.rotation = 0                           
        self.dimensions = dimensions                

        self.mass = mass

        self.gravity = VM.Vector2(0, 100)
        self.force = VM.Vector2(0, 0)
        self.velocity = VM.Vector2(0, 0)            
        self.accleration = VM.Vector2(0, 0)          
        self.drag = 0.0                             

        if self not in self.Bodies:
            self.Bodies.append(self)


    def addForce(self, force):
        self.force += force

    def Update(self, dt):
        self.UpdatePos(dt)
    
    def UpdatePos(self, dt):
        self.accleration = self.force *(1/self.mass)
        self.accleration += self.gravity
        self.velocity += (self.accleration * dt)
        self.position += (self.velocity * (1 - self.drag) * dt )
        self.force = VM.Vector2(0, 0)

    def findVertices(self):
        xx = self.position.x
        yy = self.position.y

        ww = self.dimensions.x
        hh = self.dimensions.y

        v = [
            VM.Vector2(xx-ww/2, yy-hh/2),
            VM.Vector2(xx+ww/2, yy-hh/2),
            VM.Vector2(xx+ww/2, yy+hh/2),
            VM.Vector2(xx-ww/2, yy+hh/2)
        ]

        for i in range(4):
            v[i].rotate(self.position, self.rotation)
            
        return v        