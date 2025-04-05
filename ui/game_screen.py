import math

from game.World import World
from ui.frame import Frame, set_frame
import importlib

from ui.game_over import GameOver
from ui.widget import Button, Group, Player, TowerPlacer, TowerStats
from game.towers import Tower

# Pillow for gif conversion
import pygame
from functools import partial

# (480, 288, 128, 64)
# (160, 288, 128, 64)

towers = ["Knight", "Archer", "Wizard"]

class GameScreen(Frame):
    map = None
    def __init__(self):
        self.tower_stats = None
        self.s_button = Button(18 * 32 + 32, 8 * 32, 128, 32)
        self.s_button.set_text("settings")
        self.s_button.color = pygame.color.Color(0, 0, 0)
        self.settings = Group(32, 32, 768 - 64, 512 - 64)

        button = Button(480, 288, 128, 32)
        button.set_text("return to game")
        button.color = pygame.color.Color(0, 0, 0)
        button.callback = self.toggle_settings
        self.settings.widgets.append(button)

        button = Button(160, 288, 128, 32)
        button.set_text("exit to menu")
        button.callback = self.exit_to_menu
        button.color = pygame.color.Color(0, 0, 0)
        self.settings.widgets.append(button)

        self.sprite_menu = Group(18 * 32, 0, 6 * 32, 16 * 32)
        self.sprite_menu.widgets.append(Player())
        self.images = []
        self.img_poses = []
        names = ["./assets/tiles/pngs/sword_ui.png", "./assets/tiles/pngs/arrow_ui.png", "./assets/tiles/pngs/wizard_ui.png"]
        for idx, t in enumerate(towers):
            x = 32 * (idx % 2) + 19 * 32
            y = 32 * (int(idx) // 2) + 128
            button = Button(x, y, 32, 32)
            button.set_tip_text(t)
            button.callback = partial(self.set_tower, idx + 1)
            self.sprite_menu.widgets.append(button)
            img = pygame.image.load(names[idx])
            self.images.append(img)
            self.img_poses.append((x, y))

        self.selected_tower = 0
        self.s_open = False
        self.s_button.callback = self.toggle_settings

        self.done = True

        if GameScreen.map is None:
            GameScreen.map = World(pygame.image.load("assets/tiles/game_loop.png"))

        self.tower_placer = TowerPlacer(None)


    def update(self, dt):
        all_keys = pygame.key.get_just_pressed()
        all_mods = pygame.key.get_pressed()
        if (
            all_keys[pygame.K_d]
            and all_mods[pygame.K_LSHIFT]
            and all_mods[pygame.K_LCTRL]
        ):
            Button.DEBUG_DRAGGABLE = not Button.DEBUG_DRAGGABLE

        GameScreen.map.update(dt)

        self.sprite_menu.widgets[0].health = GameScreen.map.health
        if self.sprite_menu.widgets[0].health <= 0:
            set_frame(GameOver())
        self.sprite_menu.widgets[0].money = GameScreen.map.money
        #print(GameScreen.map.money)




        for t in self.map.tower_group:
            if t.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_just_pressed()[0]:
                self.tower_stats = TowerStats(18 * 32, 12 * 32, t)

        if self.tower_stats is not None:
            self.tower_stats.update(dt)

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
        GameScreen.map.draw(display)
        for o in GameScreen.map.tower_group:
            o.render(display)
        self.sprite_menu.render(display)
        self.s_button.render(display)

        text_surface = Button.text_font.render(
            "wave: " + str(GameScreen.map.level), False, (232, 232, 232), (0, 0, 0)
        )
        display.blit(text_surface, (18 * 32 + 32, 8 * 32 - 32, 128, 32))

        for img, img_loc in zip(self.images, self.img_poses):
            display.blit(img, img_loc)

        if self.s_open:
            self.settings.render(display)

        if self.tower_stats is not None:
            self.tower_stats.render(display)

        if self.selected_tower != 0 and self.tower_placer.tower.x < 18 * 32:
            self.tower_placer.render(display)
            if pygame.mouse.get_just_pressed()[0] and GameScreen.map.money > self.tower_placer.tower.cost:
                # place tower
                pos_x = self.tower_placer.tower.rect.x
                pos_y = self.tower_placer.tower.rect.y
                pos_x = math.floor(pos_x / 32) * 32
                pos_y = math.floor(pos_y / 32) * 32

                self.tower_placer.tower.x = pos_x
                self.tower_placer.tower.y = pos_y
                self.tower_placer.tower.rect.x = pos_x
                self.tower_placer.tower.rect.y = pos_y
                self.tower_placer.tower.enemies = GameScreen.map.enemy_group
                GameScreen.map.tower_group.add(self.tower_placer.tower)
                self.tower_placer = TowerPlacer(Tower(None, 0, 0, "knight", []))
                self.selected_tower = 0
                GameScreen.map.money -= self.tower_placer.tower.cost

    def toggle_settings(self):
        self.s_open = not self.s_open

    def exit_to_menu(self):
        main_menu = importlib.import_module("ui.main_menu")
        GameScreen.map = World(pygame.image.load("./assets/tiles/game_loop.png"))
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
            tower_type = tower_types[t]
            self.tower_placer = TowerPlacer(Tower(tower_image, 0, 0, tower_type, []))
