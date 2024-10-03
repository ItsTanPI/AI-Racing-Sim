import math

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def set_vector2(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    @staticmethod
    def scalar_multiply(scalar, vector):
        return Vector2(vector.x * scalar, vector.y * scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        mag = self.magnitude()
        return Vector2(self.x / mag, self.y / mag)
    
    def rotate(self,center, deg):
        new_x = center.x + (self.x - center.x) * math.cos(math.radians(deg)) - (self.y - center.y) * math.sin(math.radians(deg)) 
        new_y = center.y + (self.x - center.x) * math.sin(math.radians(deg)) + (self.y - center.y) * math.cos(math.radians(deg))
        
        self.x = new_x
        self.y = new_y
 