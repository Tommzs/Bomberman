import pygame
from bomb import Bomb

class Character:
    def __init__(self, pos):
        self.life = True
        self.posX = pos[0] * 4
        self.posY = pos[1] * 4
        self.direction = 0
        self.frame = 0
        self.animation = []
        self.bomb_range = 3
        self.bomb_limit = 1

    def plant_bomb(self, map, time, bombs, bonuses):
        if self.bomb_limit > 0:
            bomb = Bomb(self.bomb_range, round(self.posX/4), round(self.posY/4), map, self, time, bonuses)
            self.bomb_limit -= 1
            bombs.append(bomb)
            map[bomb.posX][bomb.posY] = 3

    def check_death(self, exp):
        for e in exp:
            for s in e.sectors:
                if int(self.posX / 4) == s[0] and int(self.posY / 4) == s[1]:
                    self.life = False

    def check_bonus(self, bonuses):
        to_remove = []
        for bonus in bonuses:
            if int(self.posX/4) == bonus.x and int(self.posY/4) == bonus.y:
                if bonus.type == 1:
                    self.bomb_range += 1
                elif bonus.type == 2:
                    self.bomb_limit += 1
                to_remove.append(bonus)
        for bonus in to_remove:
            bonuses.remove(bonus)