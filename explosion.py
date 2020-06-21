from random import choice
from bonus import Bonus

class Explosion:

    bomber = None

    def __init__(self, x, y, r):
        self.sourceX = x
        self.sourceY = y
        self.range = r
        self.time = 300
        self.frame = 0
        self.sectors = []

    def explode(self, map, bombs, b):

        self.bomber = b.bomber
        self.sectors.extend(b.sectors)
        bombs.remove(b)
        self.bomb_chain(bombs, map)

    def bomb_chain(self, bombs, map):

        for s in self.sectors:
            for x in bombs:
                if x.posX == s[0] and x.posY == s[1]:

                    map[x.posX][x.posY] = 0
                    x.bomber.bomb_limit += 1
                    self.explode(map, bombs, x)

    def clear_sectors(self, map, bonuses):

        for i in self.sectors:
            for bonus in bonuses:
                if (bonus.x == i[0]) and (bonus.y == i[1]):
                    bonuses.remove(bonus)

            if map[i[0]][i[1]] != 0:
                map[i[0]][i[1]] = 0
                rand_bonus = choice([0, 0, 0, 0, 0, 0, 1, 1, 2, 2])
                if rand_bonus != 0:
                    bonuses.append(Bonus(i[0], i[1], rand_bonus))

    def update(self, dt):

        self.time = self.time - dt

        if self.time < 100:
            self.frame = 2
        elif self.time < 200:
            self.frame = 1
