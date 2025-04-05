import pygame

from ui.widget import Button

class MainMenu:
    def __init__(self):
        self.title = None
        self.start_button = Button(0, 0, 128, 64)
        self.start_button.set_text("start game")
        self.quit_button = Button(100, 100, 128, 64)
        self.quit_button.set_text("quit game")

        self.start_button.callback = self.start_game
        self.quit_button.callback = self.quit_game

    def update(self, dt):
        self.start_button.update(dt)
        self.quit_button.update(dt)

        all_keys = pygame.key.get_just_pressed()
        all_mods = pygame.key.get_pressed()
        if all_keys[pygame.K_d] and all_mods[pygame.K_LSHIFT] and all_mods[pygame.K_LCTRL]:
            Button.DEBUG_DRAGGABLE = not Button.DEBUG_DRAGGABLE
    def render(self, display=pygame.display.get_surface()):
        self.start_button.render(display)
        self.quit_button.render(display)

    @staticmethod
    def start_game():
        print("game started!!!")
    @staticmethod
    def quit_game():
        pygame.event.post(pygame.event.Event(pygame.QUIT))