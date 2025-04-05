import pygame

class World():
    def __init__(self, tileMap):
        self.health = 100
        self.image = tileMap
        self.money = 1000

    def draw(self, surface):
        surface.blit(self.image,(0,0)) 