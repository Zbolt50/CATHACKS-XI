import pygame
import random
from Enemy_Data import Enemy_data
def genterateWave(level):
    level = level
    base_threat = 10
    level_multiplayer = level + 10
    threat_total = base_threat * level_multiplayer
    wave = []
    while threat_total > 0:
        if threat_total >= 10 and random.random() > 0.2:
            wave.append("Horse")
            threat_total -= 10
        elif threat_total >= 5 and random.random() > 0.5:
            wave.append("Heavy Armored")
            threat_total -= 5
        elif threat_total >= 3 and random.random() > 0.75:
            wave.append("Armored")
            threat_total -= 3
        else:
            wave.append("Grunt")
            threat_total -= 1
            
    print(wave)
    return wave
