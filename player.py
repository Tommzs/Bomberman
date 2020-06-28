import pygame
import math

from controls import Controls
from character import Character

class Player(Character):
    def __init__(self, pos, controls, name):
        Character.__init__(self, pos)
        self.controls = controls
        self.name = name
        self.moving = False

    def stop(self):
        self.moving = False
    
    def change_direction(self, direction):
        self.direction = direction
        self.frame = 0
        self.moving = True

    def step(self, new_direction, grid, ene_blocks):
        if new_direction != self.direction:
            self.change_direction(new_direction)
        if self.direction == 0:
            self.move(0, 1, grid, ene_blocks)
            self.next_frame()
        elif self.direction == 1:
            self.move(1, 0, grid, ene_blocks)
            self.next_frame()
        elif self.direction == 2:
            self.move(0, -1, grid, ene_blocks)
            self.next_frame()
        elif self.direction == 3:
            self.move(-1, 0, grid, ene_blocks)
            self.next_frame()

    def move(self, dx, dy, grid, enemys):
        tempx = int(self.posX/4)
        tempy = int(self.posY/4)

        map = []

        for i in range(len(grid)):
            map.append([])
            for j in range(len(grid[i])):
                map[i].append(grid[i][j])

        for x in enemys:
            if x == self:
                continue
            elif not x.life:
                continue
            else:
                map[int(x.posX/4)][int(x.posY/4)] = 2

        if self.posX % 4 != 0 and dx == 0:
            if self.posX % 4 == 1:
                self.posX -= 1
            elif self.posX % 4 == 3:
                self.posX += 1
            return
        if self.posY % 4 != 0 and dy == 0:
            if self.posY % 4 == 1:
                self.posY -= 1
            elif self.posY % 4 == 3:
                self.posY += 1
            return

        # right
        if dx == 1:
            if map[tempx+1][tempy] in [0, 4]:
                self.posX += 1
        # left
        elif dx == -1:
            tempx = math.ceil(self.posX / 4)
            if map[tempx-1][tempy] in [0, 4]:
                self.posX -= 1

        # bottom
        if dy == 1:
            if map[tempx][tempy+1] in [0, 4]:
                self.posY += 1
        # top
        elif dy == -1:
            tempy = math.ceil(self.posY / 4)
            if map[tempx][tempy-1] in [0, 4]:
                self.posY -= 1             

    def load_animations(self, scale, secondPlayer):
        image_path = "images/hero/p"
        if secondPlayer:
            image_path += "2/p"
        else:
            image_path += "1/p"

        Character.load_animations(self, scale, image_path)


    def next_frame(self):
        if self.frame == 2:
            self.frame = 0
        else:
            self.frame += 1
