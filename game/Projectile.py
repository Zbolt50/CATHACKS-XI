import pygame 
class Projectile():
    def __init__(self, x, y, width, height, image, angle):
        self.x = x
        self.y = y
        self.angle= angle
        self.orginal_image = image
        self.image = pygame.transform.rotate(self.orginal_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.width = width
        self.height = height
        self.velocity = [0,0]
        self.collider = [width, height]
    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.image,(self.width,self.height)), (self.x, self.y))
    def rotate(self):
        self.image = pygame.transform.rotate(self.orginal_image, self.angle)
    def update(self, screen):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw(screen)
        self.rotate()
        
    