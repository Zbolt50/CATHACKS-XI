import math

from game.World import World
from ui.frame import Frame, set_frame
import importlib
from ui.widget import Button, Group, Player, TowerPlacer
from game.towers import Tower

# Pillow for gif conversion
from PIL import Image
import pygame
from functools import partial

# (480, 288, 128, 64)
# (160, 288, 128, 64)

towers = ["Knight", "Archer", "Wizard"]


class GameScreen(Frame):
    map = None
    def __init__(self):
        self.s_button = Button(512 + 128 + 64, 32, 32, 32)
        self.s_button.set_tip_text("settings")
        self.settings = Group(32, 32, 768 - 64, 512 - 64)

        button = Button(480, 288, 128, 64)
        button.set_tip_text("return to game")
        button.callback = self.toggle_settings
        self.settings.widgets.append(button)

        button = Button(160, 288, 128, 64)
        button.set_tip_text("exit to menu")
        button.callback = self.exit_to_menu
        self.settings.widgets.append(button)

        self.sprite_menu = Group(18 * 32, 0, 6 * 32, 16 * 32)
        self.sprite_menu.widgets.append(Player())
        for idx, t in enumerate(towers):
            x = 32 * (idx % 2) + 19 * 32
            y = 32 * (int(idx) // 2) + 128
            button = Button(x, y, 32, 32)
            button.set_tip_text(t)
            button.callback = partial(self.set_tower, idx + 1)
            self.sprite_menu.widgets.append(button)

        self.selected_tower = 0
        self.s_open = False
        self.s_button.callback = self.toggle_settings
        self.done = True

        if GameScreen.map is None:
            GameScreen.map = World(pygame.image.load("assets/tiles/game_loop.png"))

        self.tower_placer = TowerPlacer(None)
        self.towers = []

    def update(self, dt):
        all_keys = pygame.key.get_just_pressed()
        all_mods = pygame.key.get_pressed()
        if (
            all_keys[pygame.K_d]
            and all_mods[pygame.K_LSHIFT]
            and all_mods[pygame.K_LCTRL]
        ):
            Button.DEBUG_DRAGGABLE = not Button.DEBUG_DRAGGABLE

        if self.s_open:
            self.settings.update(dt)
            self.s_button.damp = 0
            self.s_button.display_tooltip = False
        else:
            self.s_button.update(dt)
            self.sprite_menu.update(dt)

            if self.selected_tower > 0:
                button = self.sprite_menu.widgets[self.selected_tower]
                button.damp = 1
                self.tower_placer.update(dt)

    def render(self, display):
        self.map.draw(display)
        self.sprite_menu.render(display)
        self.s_button.render(display)

        for t in self.towers:
            # t.render(display)
            pygame.draw.rect(display, (120, 120, 120, 255), t)

        if self.s_open:
            self.settings.render(display)

        if self.selected_tower != 0 and self.tower_placer.tower.x < 18 * 32:
            self.tower_placer.render(display)
            if pygame.mouse.get_just_pressed()[0]:
                # place tower
                pos_x = self.tower_placer.tower.x
                pos_y = self.tower_placer.tower.y
                pos_x = math.floor(pos_x / 32) * 32
                pos_y = math.floor(pos_y / 32) * 32

                self.tower_placer.tower.x = pos_x
                self.tower_placer.tower.y = pos_y
                self.towers.append(self.tower_placer.tower)

                self.tower_placer = TowerPlacer(Tower())
                set_tower(self)
                self.selected_tower = 0

    def toggle_settings(self):
        self.s_open = not self.s_open

    def exit_to_menu(self):
        main_menu = importlib.import_module("ui.main_menu")
        set_frame(main_menu.MainMenu())

    def set_tower(self, t):
        self.selected_tower = t
        animation_paths = {
            1: "assets/towers/knight.gif",
            2: "assets/towers/archer.gif",
            3: "assets/towers/wizard.gif",
        }
        tower_types = {
            1: "knight",
            2: "archer",
            3: "wizard",
        }
        animation_path = animation_paths.get(t)
        if animation_path:
            tower_image = pygame.image.load(animation_path)
