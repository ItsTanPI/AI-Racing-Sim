import pygame
import numpy as np
import random
import vectorMath as VM
import Raycast as ray
from car import Car
# from vectorMath import line_intersection 


WIDTH, HEIGHT = 1920, 1080
N_CELLS = 50
TRACK_INFLATE = 150
FPS = 60
TRACK_SCALE = 0.75  # Scale factor to reduce track size

class TrackGenerator:
    def __init__(self):
        self.bbox = [0, WIDTH * TRACK_SCALE, 0, HEIGHT * TRACK_SCALE]  # bounding Box initialization

    def generate_track(self):                                           # generate points within bounds
        sites = [(random.uniform(self.bbox[0], self.bbox[1]),
                   random.uniform(self.bbox[2], self.bbox[3])) for _ in range(N_CELLS)]
        
        points = self.convex_hull(sites)       
        return np.array(points)

    def convex_hull(self, points):                              # finding the convex HULL
        points = sorted(set(map(tuple, points)))  

        if len(points) <= 1:
            return points

        lower = []
        for p in points:
            while len(lower) >= 2 and self.ccw(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)

        upper = []
        for p in reversed(points):
            while len(upper) >= 2 and self.ccw(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)

        return lower[:-1] + upper[:-1]  

    def ccw(self, p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
    

def inflate_polygon(poly, spacing):                             # Inflate the polygon uniformly
    center = np.mean(poly, axis=0)
    inflated = []
    for point in poly:
        direction = point - center
        norm = np.linalg.norm(direction)
        if norm == 0:
            continue
        direction = direction / norm 
        inflated_point = point + direction * spacing               # Move outward
        inflated.append(inflated_point)
    return np.array(inflated)

def center_polygon(poly):                                           # Translate polygon to center the track
    centroid = np.mean(poly, axis=0)
    screen_center = np.array([WIDTH // 2, HEIGHT // 2])
    translation = screen_center - centroid
    centered_poly = poly + translation
    return centered_poly

def convert_to_VM(centered_track, inflated_track):
    centered_vectors = [VM.Vector2(x, y) for x, y in centered_track]
    inflated_vectors = [VM.Vector2(x, y) for x, y in inflated_track]
    
    return centered_vectors, inflated_vectors

def generateTrack(inflate_ratio = TRACK_INFLATE):
    track_gen = TrackGenerator()
    current_track = track_gen.generate_track()
    centered_track = center_polygon(current_track)
    inflated_track = inflate_polygon(centered_track, inflate_ratio)
    return convert_to_VM(centered_track,inflated_track)     

def line_intersection(p1, p2, q1, q2):                                       # True if line intersects
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    
    return ((ccw(p1, q1, q2) != ccw(p2, q1, q2) )and (ccw(p1, p2, q1) != ccw(p1, p2, q2)))




pointMass = VM.Vector2(300, 100)
def main():
    Car1 = Car(VM.Vector2(200, 540))
    pygame.init()
    rotationAA = 0
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    track_gen = TrackGenerator()
    lines = []
    angle = 0
    for i in range(8):
        line = ray.RayCast(VM.Vector2(300, 100), angle,200)
        lines.append(line)
        angle+=(360/8)



    line_end = VM.Vector2(20, 100)
    line_speed = 5
    running = True 
    centered_track, inflated_track = ( [VM.Vector2(372.97078673872534, 598.7614370922374), VM.Vector2(422.10196697998197, 364.92408757601424), VM.Vector2(492.1517570782935, 198.09479774849905), VM.Vector2(657.9471713018057, 155.86112881208453), VM.Vector2(955.4317609547857, 149.42277455560037), VM.Vector2(1200.528786825163, 152.90208448232596), VM.Vector2(1589.4624902306825, 211.08240636809506), VM.Vector2(1735.350121743476, 385.44082000777473), VM.Vector2(1719.5180346051184, 794.7202468053138), VM.Vector2(1540.0135284346643, 868.1490329773305), VM.Vector2(1373.3699274007356, 891.7593650699018), VM.Vector2(891.7062111115587, 910.3051205331303), VM.Vector2(597.4917991716743, 919.5417975454379), VM.Vector2(477.0486436218857, 876.2748767009373), VM.Vector2(374.90701380144986, 622.7600237253167)] ,  [VM.Vector2(223.71668198617283, 613.7017253931398), VM.Vector2(279.46706259378334, 318.49905068060633), VM.Vector2(371.0450743245858, 109.58959229484904), VM.Vector2(565.2304014384641, 37.94759868891272), VM.Vector2(953.6774625803093, -0.5669665509610127), VM.Vector2(1279.6952473586157, 25.494582636456315), VM.Vector2(1722.4066772033157, 141.61411755812412), VM.Vector2(1882.4558323297715, 356.11659942305954), VM.Vector2(1861.7333583744605, 842.4151279266795), VM.Vector2(1670.56754193433, 942.0114020100737), VM.Vector2(1487.6069502385656, 988.9699746408181), VM.Vector2(864.5011452227405, 1057.8174399847105), VM.Vector2(493.88779642865734, 1028.013962710631), VM.Vector2(353.94976298765107, 961.9875687984235), VM.Vector2(226.3854237048119, 643.7680525516072)] )


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    centered_track, inflated_track = generateTrack()
                    print("(", centered_track,", " ,inflated_track, ")")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            pointMass.x += line_speed
            line_speed += 1 if line_speed <= 8 else 0
        if keys[pygame.K_a]:
            pointMass.x -= line_speed
            line_speed -= 1 if line_speed > 5 else 0
        if keys[pygame.K_s]:
            pointMass.y += line_speed
            line_speed += 1 if line_speed <= 8 else 0
        if keys[pygame.K_w]:
            pointMass.y -= line_speed
            line_speed -= 1 if line_speed > 5 else 0
        if keys[pygame.K_LEFT]:
            rotationAA -= 2
        if keys[pygame.K_RIGHT]:
            rotationAA += 2

        Car1.handleInput(0.016)
        Car1.Update(0.016)


        

        screen.fill((150, 150, 150))
        
        for line in lines:
            line.Update(Car1.position, Car1.rotation,0.016)
            intersection = line.Collision([centered_track,inflated_track])
            line.Draw(screen, intersection)
            if intersection:
                dist = (Car1.position - intersection).magnitude()
                if(dist < 15):
                    Car1 = Car(VM.Vector2(200, 540))
        Car1.Draw(screen)


        line_color = (255, 255, 255)  # Default line color


        pygame.draw.polygon(screen, (0, 255, 0), [(v.x, v.y) for v in centered_track], 3)
        pygame.draw.polygon(screen, (255, 0, 0), [(v.x, v.y) for v in inflated_track], 3)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
