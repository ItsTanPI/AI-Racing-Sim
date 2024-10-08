import vectorMath as VM

class RigidBody2D:

    Bodies = list()

    def __init__(self, position, dimensions, mass = 1):
        
        self.position = position                    
        self.rotation = 0                           
        self.dimensions = dimensions                

        self.mass = mass
        self.gravity = VM.Vector2(0, 0)
        self.force = VM.Vector2(0, 0)
        self.velocity = VM.Vector2(0, 0)            
        self.accleration = VM.Vector2(0, 0)          
        self.drag = 0.05
        self.dir = VM.Vector2(0, 0)

        self.dir2 = VM.Vector2(0, 0)



        if self not in self.Bodies:
            self.Bodies.append(self)


    def addForce(self, force):
        self.force += force


    def PhyUpdate(self, dt):
        self.UpdatePos(dt)
    
    def UpdatePos(self, dt):
        self.rotation %= 360
        self.force += self.gravity * self.mass        
        self.accleration = self.force *(1/self.mass)

        self.velocity += (self.accleration * dt)
        self.velocity *= (1 - self.drag)

        mag = self.velocity.magnitude()
        nor = self.velocity.normalize()

        nor.rotate(VM.Vector2(0, 0), self.rotation)
        nor *= mag


        self.position += (nor * dt )
        self.force = VM.Vector2(0, 0)


    def findVertices(self):
        xx = self.position.x
        yy = self.position.y

        ww = self.dimensions.x
        hh = self.dimensions.y

        self.dir = VM.Vector2(xx, yy-hh/3)
        self.dir.rotate(self.position, self.rotation)

        self.dir2 = VM.Vector2(self.dir.x, self.dir.y-hh/3)

        v = [
            VM.Vector2(xx-ww/2, yy-hh/2),
            VM.Vector2(xx+ww/2, yy-hh/2),
            VM.Vector2(xx+ww/2, yy+hh/4),
            VM.Vector2(xx-ww/2, yy+hh/4)
        ]

        for i in range(4):
            v[i].rotate(self.position, self.rotation)
            
        return v