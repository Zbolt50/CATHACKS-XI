import pygame

class World():
    def __init__(self, tileMap):
        self.health = 100
        self.image = tileMap

    def draw(self, surface):
        surface.blit(self.image,(0,0)) 