#import os
import importlib

import pygame
import math
from game.Projectile import Projectile


class Tower(pygame.sprite.Sprite):
    def __init__(self,image, x, y, towerType,projectiles):
        pygame.sprite.Sprite.__init__(self)
        self.towerType = towerType
        self.x = x
        self.y = y
        self.angle = 0
        self.image = image
        if self.image is not None:
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
        else:
            self.rect = pygame.rect.Rect(0, 0, 0, 0)
        self.updgradeLevel = 1
        self.state = "idle"
        self.target = None
        self.direction = "right"
        self.cooldownFrames = 0
        self.cooldown = 0
        self.setTowerStats()
        self.attackCD = int((self.cooldown * 60) / 1000)
        self.projetiles = projectiles



    def setTowerStats(self):
        if self.towerType == "knight":
            self.range = 64
            self.attackSpeed = 1
            self.damage = 200
            self.cost = 100
            self.cooldown = 500
        elif self.towerType == "archer":
            self.range = 300 
            self.attackSpeed = 2
            self.damage = 5
            self.cost = 80
            self.cooldown = 3000
        elif self.towerType == "wizard":
            self.range = 200 
            self.attackSpeed = 1.5
            self.damage = 8
            self.cost = 120
            self.cooldown = 200

    def render(self, display):
        for p in self.projetiles:
            #print("bullet image")
            p.update(display)

    game_screen = None
    def update(self, dt, enemies): # enemies is Group
        if Tower.game_screen is None:
            Tower.game_screen = importlib.import_module("ui.game_screen")
        # self.anim_timer += dt
        # if self.anim_timer > 0.1:
            #pass
            #self.image =

        to_remove = []
        for p in self.projetiles:
            if p.x <= 0 or p.x >= 576 or p.y <= 0 or p.y >= 512:
                self.projetiles.remove(p)

            #print(p.rect)
            for e in enemies:
                if e.check_collisions(p):
                    #print("Hit")
                    e.takeDamage(100, Tower.game_screen.GameScreen.map)
                    #print(e.health)
                    to_remove.append(p)
        for k in to_remove:
            try:
                self.projetiles.remove(k)
            except:
                pass
        if self.state == "cooldown":
            #print("cooldown")
            self.cooldownFrames -= 5
            if self.cooldownFrames <= 0:
                self.cooldownFrames = 0
                self.state = "idle"
                self.target = None
                self.state = "wait"

        if self.state == "idle":
            #print("findTarget")
            self.findTarget(enemies)
            #print(enemies)
            if self.target != None:
                self.rotate()
        elif self.state == "attacking":
            #print("attack")
            self.attack()
            if self.target != None:
                self.rotate()
        elif self.state == "upgrading":
           # print("upgrading")
            self.upgradeTower() 
        elif self.state == "targeting":
            #print("targeting")
            if self.targetInRange():
                self.state = "attacking"
            else:
                self.target = None
                self.state = "idle"
        elif self.state == "wait":
            #print("wait")
            self.state = "idle"

    # call this in the game loop to upgrade the tower
    def upgradeTowerFlag(self):
        if self.updgradeLevel < 3:
            self.state = "upgrading"

    def upgradeTower(self):
        self.updgradeLevel += 1
        self.damage = self.damage * 1.5
        self.cooldownFrames = self.cooldownFrames * 0.8
        self.range = self.range * 1.2
        self.state = "idle"
        

    def targetInRange(self):
        if self.target is None:
            return False
        distance = ((self.x - self.target.pos[0]) ** 2 + (self.y - self.target.pos[1]) ** 2) ** 0.5 # pythagorean theorem
        return distance <= self.range

    def findTarget(self, enemies):
        x_dist = 0
        y_dist = 0
        for enemy in enemies:
            distance = 100000000
            if enemy.health > 0:
                distance = ((self.x - enemy.pos[0]) ** 2 + (self.y - enemy.pos[1]) ** 2) ** 0.5 # pythagorean theorem
            if distance <= self.range:
                self.target = enemy
                self.angle = math.degrees(math.atan2(-y_dist,x_dist))
                self.state = "targeting"
                #print(self.range)
                break

    def attack(self):
        if self.cooldownFrames > 0:
            self.state = "cooldown"
            return
        
        if self.target is not None and self.target.health <= 0:
            self.target = None
            self.state = "idle"
            return

        if self.target is not None and self.targetInRange():
            if self.towerType == "knight":
                self.target.takeDamage(self.damage, Tower.game_screen.GameScreen.map)
                self.cooldownFrames = self.attackCD
                self.state = "cooldown"
            else:
                #print("shooting")
                self.shoot(self.projetiles)
                self.cooldownFrames = self.attackCD
                self.state = "cooldown"
        else: 
            self.target = None
            self.state = "idle"

        if self.target != None and self.target.health <= 0:
            self.target = None
            self.state = "idle"

    def shoot(self,projectiles):
        tower_center = self.rect.center
        projectile = Projectile(tower_center[0], tower_center[1], 8, 8,
                                 pygame.image.load("./assets/tiles/pngs/sword_ui.png"),
                                 self.angle)
        target_center = self.target.rect.center
        direction_x = target_center[0] - tower_center[0]
        direction_y = target_center[1] - tower_center[1]

        distance = ((direction_x) ** 2 + (direction_y) ** 2) ** 0.5
        if distance > 0: 
            direction_x /= distance
            direction_y /= distance

        projectile_speed = 5
        projectile.velocity = [direction_x * projectile_speed, direction_y * projectile_speed]
        #self.target.takeDamage(self.damage)

        projectiles.append(projectile)

    def rotate(self):
        return
        dist = self.target.pos - [self.x, self.y]
        self.angle = math.degrees(math.atan2(-dist[1],dist[0]))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)