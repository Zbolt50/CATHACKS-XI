import pygame
import math

class Tower(pygame.sprite.Sprite):
    def __init__(self,image, x, y, towerType):
        pygame.sprite.Sprite.__init__(self)
        self.towerType = towerType
        self.x = x
        self.y = y
        self.angle = 0
        self.orginal_image = image
        self.image = pygame.transform.rotate(self.orginal_image, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.updgradeLevel = 1
        self.state = "idle"
        self.target = None
        self.direction = "right"
        self.cooldownFrames = 0
        self.setTowerStats(self)
        self.attackCD = int((self.cooldown * 60) / 1000)
        

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
            print("cooldown")
            self.cooldownFrames -= 5
            if self.cooldownFrames <= 0:
                self.cooldownFrames = 0
                self.state = "idle"

        if self.state == "idle":
            self.findTarget(enemies)
        elif self.state == "attacking":
            print("attack")
            self.attack()
        elif self.state == "upgrading":
            print("upgrading")
            self.upgradeTower() 
        elif self.state == "targeting":
            print("targeting")
            if self.targetInRange():
                self.updateDirection()
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
                self.createProjectile()
        else: 
            self.target = None
            self.state = "idle"

        if self.target.health == 0:
            self.target = None
            self.state = "idle"

    # idk how to do this lfg
    def createProjectile(self):
        pass