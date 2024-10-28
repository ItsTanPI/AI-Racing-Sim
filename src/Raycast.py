import vectorMath as VM
import math
import pygame

class RayCast:
    def __init__(self, start,rotation, distance):
        self.Start = start
        self.Rotation = rotation
        self.Distance = distance
        self.End = VM.Vector2()

    
    def Update(self, pos, rotation, dt):
        self.Start = pos

        x = self.Distance * math.cos(math.radians(self.Rotation + rotation))
        y = self.Distance * math.sin(math.radians(self.Rotation + rotation))

        self.End = VM.Vector2(self.Start.x + x, self.Start.y + y)


    def Collision(self,coords):
        centered_track = coords[0]
        inflated_track = coords[1]

        for i in range(len(centered_track)):
            p1 = centered_track[i]
            p2 = centered_track[(i + 1) % len(centered_track)]
            r1 = inflated_track[i]
            r2 = inflated_track[(i + 1) % len(inflated_track)]

            if ((i + 1) % len(centered_track) == 0 and i == (len(centered_track)-1)):
                return False

            if line_intersection(self.Start.rTuple(), self.End.rTuple(), p1.rTuple(), p2.rTuple()):                     # Collision with centered track
                return find_point(self.Start.rTuple(), self.End.rTuple(), p1.rTuple(), p2.rTuple())    
            
            if line_intersection(self.Start.rTuple(), self.End.rTuple(), r1.rTuple(), r2.rTuple()):                      # Collision with inflated track
                return find_point(self.Start.rTuple(), self.End.rTuple(), r1.rTuple(), r2.rTuple())

        return False
            
    def Draw(self, screen, intersection):
        pygame.draw.line(screen, (0, 0, 0), (self.Start.x, self.Start.y), (self.End.x, self.End.y), 2)

        #pygame.draw.circle(screen,(0,255,0),(self.Start.x, self.Start.y),10)
        if intersection:
            #pygame.draw.line(screen, (0, 0, 0), (self.Start.x, self.Start.y), (intersection.x, intersection.y), 2)

            line_color = (255,0,0)
            pygame.draw.circle(screen,(255,255,0),(intersection.x,intersection.y),10)
        else:
            #pygame.draw.line(screen, (0, 0, 0), (self.Start.x, self.Start.y), (self.End.x, self.End.y), 2)
            pass



def line_intersection(p1, p2, q1, q2): #Tuple
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    return ((ccw(p1, q1, q2) != ccw(p2, q1, q2) )and (ccw(p1, p2, q1) != ccw(p1, p2, q2)))


def find_point(p1,p2,q1,q2):                    
    A1 = p2[1] - p1[1]
    B1 = p1[0] - p2[0]
    C1 = A1 * p1[0] + B1 * p1[1]
    A2 = q2[1] - q1[1]
    B2 = q1[0] - q2[0]
    C2 = A2 * q1[0] + B2 * q1[1]
    determinant = A1 * B2 - A2 * B1

    if determinant == 0:
        return None                         
    
    x = (B2 * C1 - B1 * C2) / determinant   
    y = (A1 * C2 - A2 * C1) / determinant
    return VM.Vector2(x, y)


def DrawPoint(screen,color,points):
    pygame.draw.rect(screen,color,points,15,15)
