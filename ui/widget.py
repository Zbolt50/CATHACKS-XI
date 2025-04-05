import importlib
import math

# necessary for annotation
from abc import ABC, abstractmethod
from functools import partial
from typing import List

import pygame
from PIL import Image

from game.World import World
from game.towers import Tower


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
            if pygame.mouse.get_just_pressed()[0]:
                s = pygame.mixer.Sound("./sounds/whenUserClick.wav")
                s.set_volume(0.3)
                s.play(0)
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
            self.text, False, pygame.color.Color(232, 232, 232).lerp("black", 0.3 * self.damp), new_color
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
    def __init__(self, x, y, tower: Tower):
        self.rect = pygame.rect.Rect(x, y, 6 * 32, 6 * 32)
        self.surf = pygame.surface.Surface((6 * 32, 6 * 32))
        self.close_button = Button(x, y, 32, 32)
        self.close_icon = pygame.image.load("./assets/tiles/pngs/exit.png")
        self.upgrade_button = Button(x+64, y, 32, 32)
        self.upgrade_icon = pygame.image.load("./assets/tiles/pngs/upgrade.png")

        self.target_tower: Tower = tower

        upgrader = partial(self.upgrade_tower, self.target_tower)
        self.upgrade_button.callback = upgrader
        self.hidden = False

        self.close_button.callback = self.hide

    def update(self, dt):
        if not self.hidden:
            self.close_button.update(dt)
            self.upgrade_button.update(dt)

    def render(self, display):
        if not self.hidden:
            pygame.draw.rect(display, (80, 80, 80), self.rect)
            self.close_button.render(display)
            display.blit(self.close_icon, self.close_button.rect)
            self.upgrade_button.render(display)
            display.blit(self.upgrade_icon, self.upgrade_button.rect)

    def hide(self):
        self.hidden = True
    game_screen = None
    def upgrade_tower(self, tower):
        if TowerStats.game_screen is None:
            TowerStats.game_screen = importlib.import_module("ui.game_screen")

        upgrade_money = 0
        match tower.towerType:
            case "knight": upgrade_money = 100
            case "archer": upgrade_money = 80
            case "wizard": upgrade_money = 120
        if TowerStats.game_screen.GameScreen.map.money > upgrade_money:
            tower.upgradeTowerFlag()
            TowerStats.game_screen.GameScreen.map.money -= upgrade_money


class TowerPlacer(Widget):
    def __init__(self, tower):
        self.surf = pygame.surface.Surface((32, 32))
        # Render animation here
        self.tower = tower

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.tower.rect.x = mouse_pos[0]
        self.tower.rect.y = mouse_pos[1]

    def render(self, display):
        display.blit(self.tower.image)
