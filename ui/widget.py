import math

# necessary for annotation
from abc import ABC, abstractmethod
from typing import List

import pygame
from PIL import Image


class Widget(ABC):
    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def render(self, display):
        pass


class Group(Widget):
    def __init__(self, x, y, width, height):
        self.widgets: List[Widget] = []
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.surf = pygame.surface.Surface((width, height))
        self.color = pygame.color.Color((200, 200, 200, 255))

    def update(self, dt):
        for w in self.widgets:
            w.update(dt)

    def render(self, display):
        display.blit(self.surf, self.rect)
        for w in self.widgets:
            w.render(display)


class Button(Widget):
    DEBUG_DRAGGABLE = False

    text_font = None

    def __init__(self, x, y, width, height):
        if Button.text_font is None:
            Button.text_font = pygame.font.Font(
                "./assets/fonts/Ac437_IBM_VGA_8x16.ttf", 32
            )

        self.rect = pygame.rect.Rect(x, y, width, height)
        self.surf = pygame.surface.Surface((width, height))
        self.color = pygame.color.Color((200, 200, 200, 255))

        self.text = ""
        self.text_surface = Button.text_font.render(
            self.text, False, (232, 232, 232), self.color
        )

        self.display_tooltip = False
        self.tip_text = ""
        self.tip_text_surface = Button.text_font.render(
            self.tip_text, False, (232, 232, 232), (0, 0, 0)
        )

        self.damp = 0
        self.callback = None
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.display_tooltip = True
            if pygame.mouse.get_pressed()[0]:
                self.damp = 2

                if Button.DEBUG_DRAGGABLE:
                    mouse_pos = list(pygame.mouse.get_pos())
                    mouse_pos[0] = math.floor(mouse_pos[0] / 16) * 16
                    mouse_pos[1] = math.floor(mouse_pos[1] / 16) * 16
                    self.rect = pygame.rect.Rect(
                        mouse_pos[0] - self.rect.width / 2,
                        mouse_pos[1] - self.rect.height / 2,
                        self.rect.width,
                        self.rect.height,
                    )
            else:
                self.damp = 1

            if pygame.mouse.get_just_released()[0]:
                if self.callback is not None and not Button.DEBUG_DRAGGABLE:
                    self.callback()
        else:
            self.damp = 0
            self.display_tooltip = False

        if Button.DEBUG_DRAGGABLE and self.timer > 1.0:
            if len(self.tip_text) != 0:
                print("DEBUG: " + self.tip_text + ": " + str(self.rect))
            else:
                print("DEBUG: _rectangle: " + str(self.rect))
            self.timer = 0

    def render(self, display=pygame.display.get_surface()):
        # render text

        new_color = self.color.lerp("black", 0.3 * self.damp)
        self.surf.fill(new_color)
        display.blit(self.surf, self.rect)
        self.text_surface = Button.text_font.render(
            self.text, False, (232, 232, 232), new_color
        )
        if len(self.tip_text) != 0 and self.display_tooltip:
            mouse_pos = list(pygame.mouse.get_pos())
            mouse_pos[0] = math.floor(mouse_pos[0] / 32 + 1) * 32
            mouse_pos[1] = math.floor(mouse_pos[1] / 32 + 1) * 32
            display.blit(self.tip_text_surface, (mouse_pos[0], mouse_pos[1]))
        display.blit(self.text_surface, self.rect)

    def set_text(self, text):
        self.text = text

    """Set hover text in this button.
    Make sure to use this; it re-bakes the surface so it displays an updated render
    """

    def set_tip_text(self, text):
        self.tip_text = text
        self.tip_text_surface = Button.text_font.render(
            self.tip_text, False, (232, 232, 232), (0, 0, 0)
        )


class Player(Widget):
    UI_POS = (18 * 32, 0)

    def __init__(self):
        self.health = 100
        self.money = 250
        self.health_icon = pygame.image.load("assets/tiles/pngs/heart.png")
        self.health_icon = pygame.transform.scale(
            self.health_icon,
            (self.health_icon.get_width() * 2.0, self.health_icon.get_height() * 2.0),
        )

        self.money_icon = pygame.image.load("assets/tiles/pngs/money.png")
        self.money_icon = pygame.transform.scale(
            self.money_icon,
            (self.money_icon.get_width() * 2.0, self.money_icon.get_height() * 2.0),
        )

    def update(self, dt):
        pass

    def render(self, display):
        health_text = Button.text_font.render(
            str(self.health), False, (232, 18, 18), (0, 0, 0)
        )
        money_text = Button.text_font.render(
            str(self.money), False, (180, 180, 18), (0, 0, 0)
        )
        display.blit(health_text, (Player.UI_POS[0] + 32, Player.UI_POS[1]))
        display.blit(self.health_icon, Player.UI_POS)
        display.blit(self.money_icon, (Player.UI_POS[0], Player.UI_POS[1] + 32))
        display.blit(money_text, (Player.UI_POS[0] + 32, Player.UI_POS[1] + 32))


class TowerStats(Widget):
    def __init__(self, x, y):
        self.rect = pygame.rect.Rect(x, y, 128, 196)
        self.surf = pygame.surface.Surface((128, 196))
        self.close_button = Button(x, y, 64, 64)

    def update(self, dt):
        pass

    def render(self, display):
        pass


class TowerPlacer(Widget):
    def __init__(self, tower):
        self.surf = pygame.surface.Surface((32, 32))
        # Render animation here
        self.tower = tower
        self.animation_frames = []
        self.animation_index = 0
        self.animation_timer = 0
        self.frame_duration = 0.1

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.tower.x = mouse_pos[0]
        self.tower.y = mouse_pos[1]

        if self.animation_frames:
            self.animation_timer += dt
            if self.animation_timer > self.frame_duration:
                self.animation_timer = 0
                self.animation_index = (self.animation_index + 1) % len(
                    self.animation_frames
                )

    def render(self, display):
        if self.animation_frames:
            frame = self.animation_frames[self.animation_index]
            display.blit(frame, (self.tower.x, self.tower.y))
        else:
            pygame.draw.rect(display, (120, 120, 120, 255), self.tower)

    def set_animation(self, path_to_gif):
        self.animation_frames = []
        self.animation_index = 0
        self.animation_timer = 0

        pil_image = Image.open(path_to_gif)
        try:
            while True:
                frame = pil_image.convert("RGBA")
                pygame_image = pygame.image.frombytes(
                    frame.tobytes(), frame.size, "RGBA"
                )
                self.animation_frames.append(pygame_image)
                pil_image.seek(pil_image.tell() + 1)

        except EOFError:
            pass
