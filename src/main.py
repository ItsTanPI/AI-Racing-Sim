import pygame
import sys
import vectorMath as VM
import physics as phy
import car

import os

SrcWidth = 800
SrcHeight = 600

pygame.init()
screen = pygame.display.set_mode((SrcWidth, SrcHeight))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)

Car = car.Car(VM.Vector2(400, 300), VM.Vector2(30, 100))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)


    Car.Update(0.016)
    Car.Draw(screen)
    Car.debugDraw(screen)
    print(f"Speed: {Car.velocity.magnitude():5.1f}, RPM {Car.CurRPM: 5.0f} SteerAngle {Car.steerAngle: 5.0f}" )


    pygame.display.flip()
    clock.tick(60)
