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

    def load_animations(self, scale):
        front = []
        back = []
        left = []
        right = []
        resize_width = scale
        resize_height = scale

        f1 = pygame.image.load('images/hero/pf0.png')
        f2 = pygame.image.load('images/hero/pf1.png')
        f3 = pygame.image.load('images/hero/pf2.png')

        f1 = pygame.transform.scale(f1, (resize_width, resize_height))
        f2 = pygame.transform.scale(f2, (resize_width, resize_height))
        f3 = pygame.transform.scale(f3, (resize_width, resize_height))

        front.append(f1)
        front.append(f2)
        front.append(f3)

        r1 = pygame.image.load('images/hero/pr0.png')
        r2 = pygame.image.load('images/hero/pr1.png')
        r3 = pygame.image.load('images/hero/pr2.png')

        r1 = pygame.transform.scale(r1, (resize_width, resize_height))
        r2 = pygame.transform.scale(r2, (resize_width, resize_height))
        r3 = pygame.transform.scale(r3, (resize_width, resize_height))

        right.append(r1)
        right.append(r2)
        right.append(r3)

        b1 = pygame.image.load('images/hero/pb0.png')
        b2 = pygame.image.load('images/hero/pb1.png')
        b3 = pygame.image.load('images/hero/pb2.png')

        b1 = pygame.transform.scale(b1, (resize_width, resize_height))
        b2 = pygame.transform.scale(b2, (resize_width, resize_height))
        b3 = pygame.transform.scale(b3, (resize_width, resize_height))

        back.append(b1)
        back.append(b2)
        back.append(b3)

        l1 = pygame.image.load('images/hero/pl0.png')
        l2 = pygame.image.load('images/hero/pl1.png')
        l3 = pygame.image.load('images/hero/pl2.png')

        l1 = pygame.transform.scale(l1, (resize_width, resize_height))
        l2 = pygame.transform.scale(l2, (resize_width, resize_height))
        l3 = pygame.transform.scale(l3, (resize_width, resize_height))

        left.append(l1)
        left.append(l2)
        left.append(l3)

        self.animation.append(front)
        self.animation.append(right)
        self.animation.append(back)
        self.animation.append(left)

    def next_frame(self):
        if self.frame == 2:
            self.frame = 0
        else:
            self.frame += 1
