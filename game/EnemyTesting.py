import pygame
from Enemy import Enemy
from Waves import genterateWave
from World import World

pygame.init()

running = True
clock = pygame.time.Clock()
spwan_dely = 400
last_enemy_time = pygame.time.get_ticks()
enemy_index = 0

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

waypoints = [
    (160, 80),  # Start middle-left (inside border)
    (480, 80),  # → middle-right
    (480, 160),  # ↓
    (160, 160),  # ←
    (160, 240),  # ↓
    (480, 240),  # →
    (480, 320),  # ↓
    (160, 320),  # ←
    (160, 400),  # ↓
    (480, 400),  # →
    (480, 480),  # ↓
    (160, 480),  # ←
    (160, 560),  # End near bottom-left (inside border)
]

tilemap_coords_1 = [
    (496 + 64, 48),
    (368 + 64, 48),
    (368 + 64, 144),
    (464 + 64, 144),
    (464 + 64, 464),
    (368 + 64, 464),
    (368 + 64, 368),
    (176 + 64, 368),
    (176 + 64, 400),
    (80 + 64, 400),
]

waypoints1 = [
    (160, 80),  # Start middle-left (inside border)
    (480, 80),  # → middle-right
    (480, 160),  # ↓
    (160, 160),  # ←
    (160, 240),  # ↓
    (480, 240),  # →
    (480, 320),  # ↓
    (160, 320),  # ←
    (160, 400),  # ↓
    (480, 400),  # →
    (480, 480),  # ↓
    (160, 480),  # ←
    (160, 560),  # End near bottom-left (inside border)
]

waypoints = [
    (496 + 64, 48),
    (368 + 64, 48),
    (368 + 64, 144),
    (464 + 64, 144),
    (464 + 64, 464),
    (368 + 64, 464),
    (368 + 64, 368),
    (176 + 64, 368),
    (176 + 64, 400),
    (80 + 64, 400),
    (80, 400),
    (80, 304),
    (16, 304),
]

tilemap_coords_2 = [
    (496 + 64, 48),
    (368 + 64, 48),
    (368 + 64, 144),
    (464 + 64, 144),
    (464 + 64, 240),
    (432, 240),
    (432, 368),
    (240, 368),
    (240, 400),
    (80 + 64, 400),
    (80, 400),
    (80, 304),
    (16, 304),
]
tilemap_coords_3 = [
    (496 + 64, 48),
    (368 + 64, 48),
    (368 + 64, 144),
    (464 + 64, 144),
    (464 + 64, 240),
    (432, 240),
    (432, 240 - 32),
    (432 - 128 - 64, 240 - 32),
    (432 - 128 - 64, 240 + 32),
    (432 - 128 - 64 - 128 - 32, 240 + 32),
    (432 - 128 - 64 - 128 - 32, 240 + 32 + 32),
    (432 - 128 - 64 - 128 - 32 - 96, 240 + 32 + 32),
]

tilemap_coords_4 = [
    (496 + 64, 48),
    (368 + 64, 48),
    (368 + 64, 144),
    (464 + 64, 144),
    (464 + 64, 240),
    (432, 240),
    (432, 240 - 32),
    (432 - 128 - 64, 240 - 32),
    (432 - 128 - 64, 240 - 128 - 32),
    (432 - 128 - 64 - 128, 240 - 128 - 32),
    (432 - 128 - 64 - 128, 240 - 32 + 64),
    (432 - 128 - 64 - 128 - 32, 240 - 32 + 64),
    (432 - 128 - 64 - 128 - 32, 240 + 64),
    (432 - 128 - 64 - 128 - 32 - 96, 240 + 32 + 32),
]


wave = genterateWave(3)

enemy_group = pygame.sprite.Group()

Grunt = Enemy("Grunt", waypoints, grunt_image)
enemy_group.add(Grunt)

pygame.mixer.music.load("03.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

while running:

    clock.tick(60)

    enemy_group.update(Map)

    screen.fill("Grey100")
    Map.draw(screen)

    pygame.draw.lines(screen, ("Grey0"), False, waypoints)
    pygame.draw.lines(screen, ("Grey100"), False, tilemap_coords_2)

    enemy_group.draw(screen)

    if pygame.time.get_ticks() - last_enemy_time > spwan_dely:
        if enemy_index < len(wave):
            enenmy_type = wave[enemy_index]
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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
