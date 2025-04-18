import pygame
from Enemy import Enemy
from towers import Tower
from Waves import genterateWave
from World import World
from Projectile import Projectile
from Path import paths
import random

pygame.init()

running = True
clock = pygame.time.Clock()
spwan_dely = 400
last_enemy_time = pygame.time.get_ticks()
enemy_index = 0
projectiles = []

screen = pygame.display.set_mode((768, 512))

map_image = pygame.image.load("../assets/tilemap/game_loop.png")

grunt_image = pygame.image.load(
    "../TestingImages/pngtree-g-letter-alphabet-golden-text-and-font-png-image_2915469.jpg"
).convert_alpha()
armored_image = pygame.image.load("../TestingImages/Armored_Testing.jpg").convert_alpha()
armoredHeavy_image = pygame.image.load(
    "../TestingImages/Heavy_testing.jpg"
).convert_alpha()
horse_image = pygame.image.load("../TestingImages/Horse_Testing.jpg").convert_alpha()

grunt_image = pygame.transform.scale(
    grunt_image, (grunt_image.get_width() * 0.1, grunt_image.get_height() * 0.1)
)
horse_image = pygame.transform.scale(
    horse_image, (horse_image.get_width() * 0.1, horse_image.get_height() * 0.1)
)
armored_image = pygame.transform.scale(
    armored_image, (armored_image.get_width() * 0.1, armored_image.get_height() * 0.1)
)
armoredHeavy_image = pygame.transform.scale(
    armoredHeavy_image,
    (armoredHeavy_image.get_width() * 0.1, armoredHeavy_image.get_height() * 0.1),
)

Map = World(map_image)

waypoints = random.choice(paths)

wave = genterateWave(3)
#wave = ["Grunt", "Grunt","Grunt","Grunt","Grunt","Grunt","Grunt","Grunt","Grunt","Grunt","Grunt"]

enemy_group = pygame.sprite.Group()
tower_group = pygame.sprite.Group()

Grunt = Enemy("Grunt", waypoints, grunt_image)
Archer = Tower(grunt_image,400, 400, "archer", projectiles)
enemy_group.add(Grunt)
tower_group.add(Archer)

pygame.mixer.music.load("03.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

while running:

    clock.tick(60)

    enemy_group.update(Map)
    tower_group.update(enemy_group)

    screen.fill("Grey100")
    Map.draw(screen)

    #pygame.draw.lines(screen, ("Grey0"), False, waypoints)
    #pygame.draw.lines(screen, ("Grey100"), False, tilemap_coords_2)
    #pygame.draw.lines(screen, (255, 0, 0, 255), False, tilemap_coords_3)

    enemy_group.draw(screen)
    tower_group.draw(screen)

    if pygame.time.get_ticks() - last_enemy_time > spwan_dely:
        if enemy_index < len(wave):
            enenmy_type = wave[enemy_index]
            #waypoints = random.choice(paths)
            if enenmy_type == "Grunt":
                enemy = Enemy(enenmy_type, waypoints, grunt_image)
            elif enenmy_type == "Armored":
                enemy = Enemy(enenmy_type, waypoints, armored_image)
            elif enenmy_type == "Heavy Armored":
                enemy = Enemy(enenmy_type, waypoints, armoredHeavy_image)
            elif enenmy_type == "Horse":
                enemy = Enemy(enenmy_type, waypoints, horse_image)

            enemy_group.add(enemy)
            enemy_index += 1
            last_enemy_time = pygame.time.get_ticks()
    
    for p in projectiles:
        #print("bullet image")
        p.update(screen)
    
    for p in projectiles:
        if p.x <= 0 or p.x >= 576 or p.y <= 0 or p.y >= 512:
            projectiles.remove(p)
    
        for e in enemy_group:
            #print(projectiles)
            for p in projectiles:
                if e.check_collisions(p):
                    #print("Hit")
                    e.takeDamage(1)
                    #print(e.health)
                    #projectiles.remove(p)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
