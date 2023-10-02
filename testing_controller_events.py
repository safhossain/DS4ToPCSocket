import pygame

pygame.init()
pygame.joystick.init()

# window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen =  pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Testing DS4 Events")

# clock for game frame rate
clock = pygame.time.Clock()
FPS = 60

# GAME LOOP
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        