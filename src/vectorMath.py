import math

def Clamp(value):
    if (value < 0):
        return 0
    elif(value > 1):
        return 1
    else:
        return value


def Lerp(a, b, t): 
    value =  a + (b - a) * Clamp(t)
    return value

def ease_in_out_quad(t):
    if t < 0.5:
        return 2 * t * t
    else:
        return -1 + (4 * t) - (2 * t * t)

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
        if(mag == 0): return Vector2(0, 0)  
        return Vector2(self.x / mag, self.y / mag)
    
    def rotate(self,center, deg):
        new_x = center.x + (self.x - center.x) * math.cos(math.radians(deg)) - (self.y - center.y) * math.sin(math.radians(deg)) 
        new_y = center.y + (self.x - center.x) * math.sin(math.radians(deg)) + (self.y - center.y) * math.cos(math.radians(deg))
        
        self.x = new_x
        self.y = new_y

    def angle_between(self, other):
        dot_product = self.dot(other)
        mag_self = self.magnitude()
        mag_other = other.magnitude()
        
        if mag_self == 0 or mag_other == 0:
            return 0
        
        cos_theta = dot_product / (mag_self * mag_other)
        cos_theta = Clamp(cos_theta)
        
        angle_rad = math.acos(cos_theta)  
        angle_deg = math.degrees(angle_rad) 
        
        return angle_deg

    def __repr__(self):
        return f"Vector2({self.x:5.1}, {self.y:5.1})"

    def __str__(self):
        return f"Vector2({self.x:5.1}, {self.y:5.1})"
        