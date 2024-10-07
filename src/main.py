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
#rb.addForce(VM.Vector2(500, -5000))

while True:
    print(rb.velocity.magnitude())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        


        if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_RETURN:
                #rb.rotation += 15 
                #rb.addForce(VM.Vector2(1000, 0))

            if event.key == pygame.K_SPACE:
                pass
                #rb.addForce(VM.Vector2(0, -5000))
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        rb.rotation += 90 *rb.velocity.magnitude()/200 * (clock.get_time() / 1000) *  (-1 if keys[pygame.K_s] or keys[pygame.K_DOWN] else 1)# Rotate clockwise

    # Rotate counterclockwise with A or Left Arrow
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        rb.rotation -= 90 *(rb.velocity.magnitude()/200) * (clock.get_time() / 1000) *(-1 if keys[pygame.K_s] or keys[pygame.K_DOWN] else 1)  # Rotate counterclockwise

    # Move forward (apply force upward) with W or Up Arrow
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        forward_force = VM.Vector2(0, -500)  # Add a force upward
        rb.addForce(forward_force)

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        forward_force = VM.Vector2(0, 500)  # Add a force upward
        rb.addForce(forward_force)

    rb.Update(0.02)

    screen.fill(WHITE)
    

    vertices = rb.findVertices()

    points = [(int(v.x), int(v.y)) for v in vertices]

    pygame.draw.polygon(screen, RED, points)

    pygame.display.flip()

    clock.tick(60)
