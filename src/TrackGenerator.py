import pygame
import sys
import random
import vectorMath as VM

def randCoord(SrcHeight,SrcWidth):
    x = random.randint(0,SrcHeight)
    y = random.randint(0,SrcWidth)
    return VM.Vector2(x,y)

def LoopGen():
    coords=[]
    for i in range(10):
        coords.append(randCoord(SrcHeight=600,SrcWidth=800))

    for i in range(0,len(coords)-2):
        pygame.draw.line(screen,GREEN,coords[i].rTuple(),coords[i+1].rTuple(),3)
        
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

'''count = 0
while(True):
    pygame.draw.line(screen,GREEN,randCoord(height,width).rTuple(),randCoord(height,width).rTuple(),6)
    if count < 10:
        count+=1
    else:
        break
'''

LoopGen()

# Game loop
def game_loop():
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Game logic (update game state here)

        # Drawing (render the frame)

        # Draw a simple shape (e.g., rectangle)
    

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(fps)

# Start the game loop
if __name__ == "__main__":
    game_loop()
