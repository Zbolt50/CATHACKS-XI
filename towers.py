import pygame

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y, towerType):
        super().__init__()  
        self.towerType = towerType
        self.x = x
        self.y = y
        self.updgradeLevel = 1
        self.state = "idle"
        self.target = None
        self.direction = "right"
        self.lastAttackTime = pygame.time.get_ticks()
        self.setTowerStats(self)

    def setTowerStats(self):
        if self.towerType == "knight":
            self.image = pygame.image.load("knight.png")
            self.rect = self.image.get_rect(center=(self.x, self.y))
            self.range = 100 
            self.attackSpeed = 1
            self.damage = 15
            self.cost = 100
        elif self.towerType == "archer":
            self.image = pygame.image.load("archer.png")
            self.rect = self.image.get_rect(center=(self.x, self.y))
            self.range = 300 
            self.attackSpeed = 2
            self.damage = 5
            self.cost = 80
        elif self.towerType == "wizard":
            self.image = pygame.image.load("wizard.png")
            self.rect = self.image.get_rect(center=(self.x, self.y))
            self.range = 200 
            self.attackSpeed = 1.5
            self.damage = 8
            self.cost = 120

    def update(self, enemies): # enemies is Group
        if self.state == "idle":
            self.findTarget(enemies)
        elif self.state == "attacking":
            self.attack()
        elif self.state == "upgrading":
            self.upgradeTower() 
        elif self.state == "targeting":
            if self.targetInRange():
                self.updateDirection()
                self.state = "attacking"
            else:
                self.target = None
                self.state = "idle"

    # call this in the game loop to upgrade the tower
    def upgradeTowerFlag(self):
        self.state = "upgrading"

    def upgradeTower(self):
        self.updgradeLevel += 1
        if self.updgradeLevel > 3:
            self.updgradeLevel = 3
        self.damage = self.damage * 1.5
        self.attackSpeed = self.attackSpeed * 1.2
        self.range = self.range * 1.2
        self.state = "idle"

    def updateDirection(self):
        if (self.x > self.target.pos[0]):
            if ((self.x - self.target.pos[0]) > (self.y - self.target.pos[1])):
                self.direction = "right"
            else:
                if self.y > self.target.pos[1]:
                    self.direction = "up"
                else:
                    self.direction = "down"
        elif (self.x < self.target.pos[0]):
            if ((self.x - self.target.pos[0]) > (self.y - self.target.pos[1])):
                self.direction = "left"
            else:
                if self.y > self.target.pos[1]:
                    self.direction = "up"
                else:
                    self.direction = "down"
        else:
            if self.y > self.target.pos[1]:
                    self.direction = "up"
            else:
                self.direction = "down"

    def targetInRange(self):
        if self.target is None:
            return False
        distance = ((self.x - self.target.pos[0]) ** 2 + (self.y - self.target.pos[1]) ** 2) ** 0.5 # pythagorean theorem
        return distance <= self.range

    def findTarget(self, enemies):
        for enemy in enemies:
            distance = ((self.x - enemy.pos[0]) ** 2 + (self.y - enemy.pos[1]) ** 2) ** 0.5 # pythagorean theorem
            if distance <= self.range:
                self.target = enemy
                self.state = "targeting"
                break

    def attack(self):
        currentTime = pygame.time.get_ticks()
        cooldown = 1000 / self.attackSpeed
        if currentTime - self.lastAttackTime >= cooldown:
            if self.target is not None:
                self.target.takeDamage(self.damage)
                self.lastAttackTime = currentTime
        if self.target.health == 0 or not self.targetInRange():
            self.target = None
            self.state = "idle"