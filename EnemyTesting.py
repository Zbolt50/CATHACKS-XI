import pygame
from Enemy import Enemy
from Enemy_Data import Enemy_data
from Waves import genterateWave
from World import World
pygame.init()

running = True
clock = pygame.time.Clock()
spwan_dely = 400
last_enemy_time = pygame.time.get_ticks()
enemy_index = 0

screen = pygame.display.set_mode((576,512))

map_image = pygame.image.load('game_loop.png')

grunt_image = pygame.image.load('TestingImages\pngtree-g-letter-alphabet-golden-text-and-font-png-image_2915469.jpg').convert_alpha()
armored_image = pygame.image.load('TestingImages\Armored_Testing.jpg').convert_alpha()
armoredHeavy_image = pygame.image.load('TestingImages\Heavy_testing.jpg').convert_alpha()
horse_image = pygame.image.load('TestingImages\Horse_Testing.jpg').convert_alpha()

grunt_image = pygame.transform.scale(grunt_image, 
                                     (grunt_image.get_width()*.1,
                                     grunt_image.get_height()*.1))
horse_image = pygame.transform.scale(horse_image, 
                                     (horse_image.get_width()*.1,
                                     horse_image.get_height()*.1))
armored_image = pygame.transform.scale(armored_image, 
                                     (armored_image.get_width()*.1,
                                     armored_image.get_height()*.1))
armoredHeavy_image = pygame.transform.scale(armoredHeavy_image, 
                                     (armoredHeavy_image.get_width()*.1,
                                     armoredHeavy_image.get_height()*.1))

Map = World(map_image)

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

wave = genterateWave(3)

enemy_group = pygame.sprite.Group()

Grunt = Enemy("Grunt", waypoints,grunt_image)
enemy_group.add(Grunt)

while running:

    clock.tick(60)

    enemy_group.update()

    screen.fill("Grey100")
    Map.draw(screen)

    pygame.draw.lines(screen, ("Grey0"),  False, waypoints)

    enemy_group.draw(screen)

    if pygame.time.get_ticks() - last_enemy_time > spwan_dely:
        if enemy_index < len(wave):
            enenmy_type = wave[enemy_index]
            if enenmy_type == "Grunt":
                enemy = Enemy(enenmy_type,waypoints, grunt_image)
            elif enenmy_type == "Armored":
                enemy = Enemy(enenmy_type,waypoints, armored_image)
            elif enenmy_type == "Heavy Armored":
                enemy = Enemy(enenmy_type,waypoints, armoredHeavy_image)
            elif enenmy_type == "Horse":
                enemy = Enemy(enenmy_type,waypoints, horse_image)
            
            enemy_group.add(enemy)
            enemy_index += 1
            last_enemy_time = pygame.time.get_ticks()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
    pygame.display.flip()

pygame.quit()

