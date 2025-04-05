import pygame
from Enemy import Enemy
from Enemy_Data import Enemy_data
from Waves import genterateWave
pygame.init()

running = True
clock = pygame.time.Clock()
spwan_dely = 400
last_enemy_time = pygame.time.get_ticks()
enemy_index = 0

screen = pygame.display.set_mode((640,640))

enemy_image = pygame.image.load('Remove background project.png').convert_alpha()
grunt_image = pygame.image.load('pngtree-g-letter-alphabet-golden-text-and-font-png-image_2915469.jpg').convert_alpha()

grunt_image = pygame.transform.scale(grunt_image, 
                                     (grunt_image.get_width()*.1,
                                     grunt_image.get_height()*.1))
enemy_image = pygame.transform.scale(enemy_image, 
                                     (enemy_image.get_width()*.1,
                                     enemy_image.get_height()*.1))

waypoints = [
    (160, 80),    # Start middle-left (inside border)
    (480, 80),    # → middle-right
    (480, 160),   # ↓
    (160, 160),   # ←
    (160, 240),   # ↓
    (480, 240),   # →
    (480, 320),   # ↓
    (160, 320),   # ←
    (160, 400),   # ↓
    (480, 400),   # →
    (480, 480),   # ↓
    (160, 480),   # ←
    (160, 560)    # End near bottom-left (inside border)
]

wave = genterateWave(1)

enemy_group = pygame.sprite.Group()

Grunt = Enemy("Grunt", waypoints,grunt_image)
enemy_group.add(Grunt)

while running:

    clock.tick(60)

    enemy_group.update()

    screen.fill("Grey100")

    pygame.draw.lines(screen, ("Grey0"),  False, waypoints)

    enemy_group.draw(screen)

    if pygame.time.get_ticks() - last_enemy_time > spwan_dely:
        if enemy_index < len(wave):
            enenmy_type = wave[enemy_index]
            enemy = Enemy(enenmy_type,waypoints, grunt_image)
            enemy_group.add(enemy)
            enemy_index += 1
            last_enemy_time = pygame.time.get_ticks()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
    pygame.display.flip()

pygame.quit()

