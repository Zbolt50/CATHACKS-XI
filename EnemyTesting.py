import pygame
from Enemy import Enemy
pygame.init()

running = True
clock = pygame.time.Clock()

screen = pygame.display.set_mode((640,640))

enemy_image = pygame.image.load('Remove background project.png').convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, 
                                     (enemy_image.get_width()*.1,
                                     enemy_image.get_height()*.1))

waypoints = [
    (100,100),
    (400, 100),
    (400, 200),
    (100,200),
    (100,100)

]

enemy_group = pygame.sprite.Group()

EnemyOne = Enemy(waypoints,enemy_image,2,100)
enemy_group.add(EnemyOne)

while running:

    clock.tick(60)

    screen.fill("Grey100")
    pygame.draw.lines(screen, ("Grey0"),  False, waypoints)
    
    enemy_group.update()
    enemy_group.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
    pygame.display.flip()

pygame.quit()

