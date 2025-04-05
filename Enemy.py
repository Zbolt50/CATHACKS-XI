import pygame 
from pygame.math import Vector2
from Enemy_Data import Enemy_data
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, waypoints, image):
        pygame.sprite.Sprite.__init__(self)
        self.type = Enemy_data.get(type)
        self.orginal_image = image
        self.health = Enemy_data.get(type)["Health"]
        self.angle = 0
        self.image = pygame.transform.rotate(self.orginal_image, self.angle)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_pos = 1
        self.speed = Enemy_data.get(type)["Speed"]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.collider = [self.orginal_image.get_width(), self.orginal_image.get_height()]

    def update(self):
        self.move()
        self.rotate()
    
    def move(self):
        if self.target_pos < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_pos])
            self.movement = self.target - self.pos
        else:
            self.kill()

        dist = self.movement.length()

        if dist >= self.speed:
              self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_pos += 1

        self.rect.center = self.pos
    
    def rotate(self):
        dist = self.target - self.pos
        self.angle = math.degrees(math.atan2(-dist[1],dist[0]))
        self.image = pygame.transform.rotate(self.orginal_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def takeDamage(self, daamge):
        self.health -= daamge
        if self.health <= 0:
            self.kill()
    