import pygame
from ui.frame import set_frame, get_frame
from ui.main_menu import MainMenu

# pygame setup
pygame.init()
screen = pygame.display.set_mode((768, 512))
clock = pygame.time.Clock()
running = True
dt = 0

set_frame(MainMenu())

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    get_frame().update(dt)
    get_frame().render(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()
    dt = clock.tick(60) / 1000  # limits FPS to 60
pygame.quit()
