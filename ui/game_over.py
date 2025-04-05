import pygame

from ui.frame import Frame


class GameOver(Frame):
    def render(self, display):
        display.blit(self.game_over_logo, (256, 128))
        pass

    def update(self, dt):
        pass

    def __init__(self):
        self.game_over_logo = pygame.image.load("./assets/tiles/pngs/game_over.png")
        self.game_over_logo = pygame.transform.scale(self.game_over_logo, (64 * 4, 32 * 4))
        pygame.mixer.stop()
        pygame.mixer.quit()
