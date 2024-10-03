import vectorMath as VM

class RigidBody2D:

    Bodies = list()

    def __init__(self, position, dimensions):
        
        self.position = position                    #Vector2
        self.rotation = 0                           #deg
        self.dimensions = dimensions                #Vector2

        self.velocity = VM.Vector2(0, 0)            #Vector2
        self.accleration = VM.Vector2(0, 0)         #Vector2 
        self.drag = 0.0                             #float

        if self not in self.Bodies:
            self.Bodies.append(self)

    def Update(self, dt):
        self.UpdatePos(dt)
    
    def UpdatePos(self, dt):
        self.velocity += (self.accleration * dt)
        self.position += (self.velocity * (1 - self.drag) * dt )

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