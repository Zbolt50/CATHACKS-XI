import random
import pygame

from game.Enemy import Enemy
from game.Path import paths
from game.Waves import genterateWave
from game.towers import Tower

from PIL import Image


class World():
    waypoints = [
        (160, 80),  # Start middle-left (inside border)
        (480, 80),  # → middle-right
        (480, 160),  # ↓
        (160, 160),  # ←
        (160, 240),  # ↓
        (480, 240),  # →
        (480, 320),  # ↓
        (160, 320),  # ←
        (160, 400),  # ↓
        (480, 400),  # →
        (480, 480),  # ↓
        (160, 480),  # ←
        (160, 560),  # End near bottom-left (inside border)
    ]

    tilemap_coords_1 = [
        (496 + 64, 48),
        (368 + 64, 48),
        (368 + 64, 144),
        (464 + 64, 144),
        (464 + 64, 464),
        (368 + 64, 464),
        (368 + 64, 368),
        (176 + 64, 368),
        (176 + 64, 400),
        (80 + 64, 400),
    ]

    waypoints1 = [
        (160, 80),  # Start middle-left (inside border)
        (480, 80),  # → middle-right
        (480, 160),  # ↓
        (160, 160),  # ←
        (160, 240),  # ↓
        (480, 240),  # →
        (480, 320),  # ↓
        (160, 320),  # ←
        (160, 400),  # ↓
        (480, 400),  # →
        (480, 480),  # ↓
        (160, 480),  # ←
        (160, 560),  # End near bottom-left (inside border)
    ]

    waypoints = [
        (496 + 64, 48),
        (368 + 64, 48),
        (368 + 64, 144),
        (464 + 64, 144),
        (464 + 64, 464),
        (368 + 64, 464),
        (368 + 64, 368),
        (176 + 64, 368),
        (176 + 64, 400),
        (80 + 64, 400),
        (80, 400),
        (80, 304),
        (16, 304),
    ]

    tilemap_coords_2 = [
        (496 + 64, 48),
        (368 + 64, 48),
        (368 + 64, 144),
        (464 + 64, 144),
        (464 + 64, 240),
        (432, 240),
        (432, 368),
        (240, 368),
        (240, 400),
        (80 + 64, 400),
        (80, 400),
        (80, 304),
        (16, 304),
    ]
    tilemap_coords_3 = [
        (496 + 64, 48),
        (368 + 64, 48),
        (368 + 64, 144),
        (464 + 64, 144),
        (464 + 64, 240),
        (432, 240),
        (432, 240 - 32),
        (432 - 128 - 64, 240 - 32),
        (432 - 128 - 64, 240 + 32),
        (432 - 128 - 64 - 128 - 32, 240 + 32),
        (432 - 128 - 64 - 128 - 32, 240 + 32 + 32),
        (432 - 128 - 64 - 128 - 32 - 96, 240 + 32 + 32),
    ]

    tilemap_coords_4 = [
        (496 + 64, 48),
        (368 + 64, 48),
        (368 + 64, 144),
        (464 + 64, 144),
        (464 + 64, 240),
        (432, 240),
        (432, 240 - 32),
        (432 - 128 - 64, 240 - 32),
        (432 - 128 - 64, 240 - 128 - 32),
        (432 - 128 - 64 - 128, 240 - 128 - 32),
        (432 - 128 - 64 - 128, 240 - 32 + 64),
        (432 - 128 - 64 - 128 - 32, 240 - 32 + 64),
        (432 - 128 - 64 - 128 - 32, 240 + 64),
        (432 - 128 - 64 - 128 - 32 - 96, 240 + 32 + 32),
    ]


    def __init__(self, tileMap):
        World.grunt_image = pygame.image.load(
            "./assets/tiles/pngs/skeleton_test.png"
        ).convert_alpha()
        World.armored_image = pygame.image.load("./assets/tiles/pngs/armored_skeleton_test.png").convert_alpha()
        World.armoredHeavy_image = pygame.image.load(
            "./assets/tiles/pngs/heavy_armored_skeleton.png"
        ).convert_alpha()
        World.horse_image = pygame.image.load("./assets/tiles/pngs/skeleton_jockey.png").convert_alpha()
        self.health = 100
        self.image = tileMap
        self.money = 1000

        self.level = 1
        self.wave = genterateWave(self.level)

        self.enemy_group = pygame.sprite.Group()
        self.tower_group = pygame.sprite.Group()

        self.projectiles = []
        self.spwan_dely = 0.400
        self.last_enemy_time = 0
        self.enemy_index = 0

    def draw(self, surface):
        surface.blit(self.image,(0,0))
        for p in self.projectiles:
            p.update(surface)
        self.enemy_group.draw(surface)
        self.tower_group.draw(surface)

    def update(self, dt):
        self.enemy_group.update(self)
        self.tower_group.update(dt, self.enemy_group)
        self.last_enemy_time += dt
        if self.last_enemy_time > self.spwan_dely:
            self.last_enemy_time = 0
            if self.enemy_index < len(self.wave):
                waypoints = random.choice(paths)
                enenmy_type = self.wave[self.enemy_index]
                if enenmy_type == "Grunt":
                    enemy = Enemy(enenmy_type, waypoints, World.grunt_image)
                elif enenmy_type == "Armored":
                    enemy = Enemy(enenmy_type, waypoints, World.armored_image)
                elif enenmy_type == "Heavy Armored":
                    enemy = Enemy(enenmy_type, waypoints, World.armoredHeavy_image)
                elif enenmy_type == "Horse":
                    enemy = Enemy(enenmy_type, waypoints, World.horse_image)

                self.enemy_group.add(enemy)
                self.enemy_index += 1
            else:
                self.enemy_index = 0
                self.level += 1
                self.wave = genterateWave(self.level)