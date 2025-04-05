import pygame

from ui.frame import Frame
from ui.widget import Button

class MainMenu(Frame):
    def __init__(self):
        self.title = None
        self.start_button = Button(160, 304, 128, 64)
        self.start_button.set_text("start game")
        self.quit_button = Button(480, 304, 128, 64)
        self.quit_button.set_text("quit game")

        self.start_button.callback = self.start_game
        self.quit_button.callback = self.quit_game

        self.done = False

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

    def start_game(self):
        self.done = True
        print("game started!!!")
    def quit_game(self):
        self.done = True
        pygame.event.post(pygame.event.Event(pygame.QUIT))