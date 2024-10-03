import pygame
import sys
import vectorMath as VM
import physics as phy

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)

rb = phy.RigidBody2D(VM.Vector2(400, 300), VM.Vector2(30, 100))

while True:
    rb.velocity = VM.Vector2(200, -200)
    rb.Update(0.02)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                rb.rotation += 10  # Increment the rotation by 10 degrees

    screen.fill(WHITE)
    

    vertices = rb.findVertices()

    points = [(int(v.x), int(v.y)) for v in vertices]

    pygame.draw.polygon(screen, RED, points)

    pygame.display.flip()

    clock.tick(60)
