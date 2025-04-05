import pygame

class World():
    def __init__(self, tileMap):
        self.image = tileMap

    def draw(self, surface):
        surface.blit(self.image,(0,0)) 