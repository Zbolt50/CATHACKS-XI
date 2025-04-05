from ui.frame import Frame
from ui.widget import Button, Group

import pygame

class GameScreen(Frame):
    def __init__(self):
        self.s_button = Button(0, 0, 64, 64)
        self.s_button.set_text("settings")
        self.settings = Group(128, 128, 256, 256)

        button = Button(128, 128, 64, 64)
        button.set_text("return to game")
        button.callback = self.toggle_settings

        self.settings.widgets.append(button)
        self.s_open = False

        self.s_button.callback = self.toggle_settings

    def update(self, dt):
        all_keys = pygame.key.get_just_pressed()
        all_mods = pygame.key.get_pressed()
        if all_keys[pygame.K_d] and all_mods[pygame.K_LSHIFT] and all_mods[pygame.K_LCTRL]:
            Button.DEBUG_DRAGGABLE = not Button.DEBUG_DRAGGABLE

        self.s_button.update(dt)
        if self.s_open:
            self.settings.update(dt)
    def render(self, display):
        self.s_button.render(display)
        if self.s_open:
            self.settings.render(display)
        pass

    def toggle_settings(self):
        self.s_open = not self.s_open