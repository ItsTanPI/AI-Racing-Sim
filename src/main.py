import pygame
import sys
import vectorMath as VM
import car


SrcWidth = 1920
SrcHeight = 1080

pygame.init()
screen = pygame.display.set_mode((SrcWidth, SrcHeight))
clock = pygame.time.Clock()  

WHITE = (100, 100, 100)
RED = (255, 0, 0)

Car = car.Car(VM.Vector2(400, 300), VM.Vector2(30, 100))    #30, 100    45, 150
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)

    Car.handleInput(0.016)
    #Car.handleAIInput(0.016, 1, False, -1, False, 2)
    Car.Update(0.016)
    Car.Draw(screen)
    Car.debugDraw(screen, [1])
    #print(f"Speed: {Car.velocity.magnitude():5.1f}, RPM {Car.CurRPM: 5.0f}, Steer Angle {Car.steerAngle: 5.0f}, Body Angle {Car.rotation: 5.0f}")


    pygame.display.flip()
    clock.tick(60)