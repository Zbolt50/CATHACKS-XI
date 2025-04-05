import pygame
import main_menu

# pygame setup
pygame.init()
screen = pygame.display.set_mode((768, 512))
clock = pygame.time.Clock()
running = True
dt = 0
mm = main_menu.MainMenu()
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("red")

    # RENDER YOUR GAME HERE
    mm.update(dt)
    mm.render(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()
    dt = clock.tick(60) / 1000  # limits FPS to 60
pygame.quit()
