import pygame
import math
from Projectile import Projectile

class Tower(pygame.sprite.Sprite):
    def __init__(self,image, x, y, towerType,projectiles):
        pygame.sprite.Sprite.__init__(self)
        self.towerType = towerType
        self.x = x
        self.y = y
        self.angle = 0
        self.orginal_image = image
        self.image = pygame.transform.rotate(self.orginal_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
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
            self.range = 100 
            self.attackSpeed = 1
            self.damage = 15
            self.cost = 100
            self.cooldown = 500
        elif self.towerType == "archer":
            self.range = 300 
            self.attackSpeed = 2
            self.damage = 5
            self.cost = 80
            self.cooldown = 300
        elif self.towerType == "wizard":
            self.range = 200 
            self.attackSpeed = 1.5
            self.damage = 8
            self.cost = 120
            self.cooldown = 200

    def update(self, enemies): # enemies is Group
        if self.state == "cooldown":
            #print("cooldown")
            self.cooldownFrames -= 5
            if self.cooldownFrames <= 0:
                self.cooldownFrames = 0
                self.state = "idle"

        if self.state == "idle":
            print("findTarget")
            self.findTarget(enemies)
            if self.target != None:
                self.rotate()
        elif self.state == "attacking":
            print("attack")
            self.attack()
            if self.target != None:
                self.rotate()
        elif self.state == "upgrading":
            #print("upgrading")
            self.upgradeTower() 
        elif self.state == "targeting":
            #print("targeting")
            if self.targetInRange():
                self.state = "attacking"
            else:
                self.target = None
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
            if enemy.health > 0:
                distance = ((self.x - enemy.pos[0]) ** 2 + (self.y - enemy.pos[1]) ** 2) ** 0.5 # pythagorean theorem
            if distance <= self.range:
                self.target = enemy
                self.angle = math.degrees(math.atan2(-y_dist,x_dist))
                self.state = "targeting"
                break

    def attack(self):
        if self.cooldownFrames > 0:
            return
        
        if self.target is not None and self.targetInRange():
            self.target.takeDamage(self.damage)
            self.cooldownFrames = self.attackCD
            self.state = "cooldown"

            if self.towerType == "archer" or self.towerType == "wizard":
                print("shooting")
                self.shoot(self.projetiles)
        else: 
            self.target = None
            self.state = "idle"

        if self.target != None and self.target.health <= 0:
            self.target = None
            self.state = "idle"

    # idk how to do this lfg
    def shoot(self,projectiles):
        tower_center = self.rect.center
        projectile = Projectile(tower_center[0], tower_center[1], 8, 8,
                                 pygame.image.load("../TestingImages/pngtree-g-letter-alphabet-golden-text-and-font-png-image_2915469.jpg"),
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
        projectiles.append(projectile)

    def rotate(self):
        dist = self.target.pos - [self.x, self.y]
        self.angle = math.degrees(math.atan2(-dist[1],dist[0]))
        self.image = pygame.transform.rotate(self.orginal_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)