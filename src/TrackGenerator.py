import pygame
import numpy as np
import random
import vectorMath as VM


WIDTH, HEIGHT = 1920, 1080
N_CELLS = 50
TRACK_INFLATE = 50
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

t = generateTrack()
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    track_gen = TrackGenerator()
    last_track_time = pygame.time.get_ticks()
    
    running = True
    current_track = track_gen.generate_track()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        centered_track, inflated_track = t

        screen.fill((0, 0, 0))  
        pygame.draw.polygon(screen, (0, 255, 0), [(v.x, v.y) for v in centered_track], 3)
        pygame.draw.polygon(screen, (255, 0, 0), [(v.x, v.y) for v in inflated_track], 3)
        

        pygame.display.flip()  # Update the display
        clock.tick(FPS)  # Control the frame rate

    pygame.quit()

if __name__ == "__main__":
    main()
