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


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                rb.rotation += 0 
            if event.key == pygame.K_SPACE:
                rb.addForce(VM.Vector2(0, -5000))
    rb.Update(0.02)

    screen.fill(WHITE)
    

    vertices = rb.findVertices()

    points = [(int(v.x), int(v.y)) for v in vertices]

    pygame.draw.polygon(screen, RED, points)

    pygame.display.flip()

    clock.tick(60)
