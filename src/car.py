
import vectorMath as VM
import physics as phy



class car(phy.RigidBody2D):

    def __init__(self, position = VM.Vector2(0, 0), dimensions = VM.Vector2(30, 100), mass = 1):
        super().__init__(position, dimensions, mass)
    

    def printtest(self):
        
        print(self.position, self.rotation, self.dimensions, self.accleration, self.force, self.drag)

    