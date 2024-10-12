import pygame
import sys
import random
import vectorMath as VM
import math


def randCoord(SrcHeight=600,SrcWidth=800):
    x = random.randint(0,SrcHeight)
    y = random.randint(0,SrcWidth)
    return (y,x)

def generate_random_points(num_points, width, height):
    coords = []
    for _ in range(num_points):
        x = random.randint(50, width - 50)
        y = random.randint(50, height - 50)
        coords.append((x, y))
    return coords

def sort_points(points):

    centroid_x = sum(x for x, y in points) / len(points)
    centroid_y = sum(y for x, y in points) / len(points)
    
    print(f"Centroid:{centroid_x},{centroid_y}")

    points.sort(key=lambda point: math.atan2(point[1] - centroid_y, point[0] - centroid_x))
    
    return points
            

def LoopGen(n):
    coords = generate_random_points(n,800,600)
    coords = sort_points(coords)
    pygame.draw.polygon(screen, GREEN, coords, 3)
    for i in coords:
        i = VM.Vector2(i)
    return coords

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Track-Generator")

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()
fps = 60

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)



# Game loop
def game_loop():
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(BLACK)

        coords = LoopGen(random.randint(4,20))
        print(coords)
        
        pygame.time.wait(3000)
        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(fps)

# Start the game loop
if __name__ == "__main__":
    game_loop()
