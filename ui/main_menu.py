import pygame

from ui.frame import Frame, set_frame
from ui.game_screen import GameScreen
from ui.widget import Button


class MainMenu(Frame):
    def __init__(self):
        self.title = None
        self.start_button = Button(160, 304, 128, 32)
        self.start_button.color = pygame.color.Color(0, 0, 0)
        self.start_button.set_text("start game")
        self.quit_button = Button(480, 304, 128, 32)
        self.quit_button.color = pygame.color.Color(0, 0, 0)
        self.quit_button.set_text("quit game")

        self.start_button.callback = self.start_game
        self.quit_button.callback = self.quit_game

        self.done = False
        self.fade_in = pygame.rect.Rect(0, 0, 768, 512)
        self.timer = 0.0

        self.title_card = pygame.image.load("./assets/tiles/pngs/title.png")

        pygame.mixer.music.load("./assets/03.mp3")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

    def update(self, dt):
        self.timer += dt

        self.start_button.update(dt)
        self.quit_button.update(dt)

        if self.timer > (1.0 / 8.0):
            self.timer = 0.0
            self.fade_in.y += 64

        all_keys = pygame.key.get_just_pressed()
        all_mods = pygame.key.get_pressed()
        if (
            all_keys[pygame.K_d]
            and all_mods[pygame.K_LSHIFT]
            and all_mods[pygame.K_LCTRL]
        ):
            Button.DEBUG_DRAGGABLE = not Button.DEBUG_DRAGGABLE

    def render(self, display=pygame.display.get_surface()):
        self.start_button.render(display)
        self.quit_button.render(display)
        pygame.draw.rect(display, (0, 0, 0), self.fade_in)
        display.blit(self.title_card)

    def start_game(self):
        set_frame(GameScreen())

    def quit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
