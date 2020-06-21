class Bomb:
    frame = 0

    def __init__(self, r, x, y, map, bomber, time, bonuses):
        self.range = r
        self.posX = x
        self.posY = y
        self.time = time
        self.bomber = bomber
        self.sectors = []
        self.get_range(map, bonuses)

    def update(self, dt):

        self.time = self.time - dt

        if self.time < 1000:
            self.frame = 2
        elif self.time < 2000:
            self.frame = 1


    def has_bonus(self, x, y, bonuses):
        for bonus in bonuses:
            if (bonus.x == x) and (bonus.y == y):
                return True
        return False


    def get_range(self, map, bonuses):

        self.sectors.append([self.posX, self.posY])

        for x in range(1, self.range):
            if map[self.posX + x][self.posY] == 1:
                break
            elif self.has_bonus(self.posX+x, self.posY, bonuses):
                self.sectors.append([self.posX+x, self.posY])
                break
            elif map[self.posX+x][self.posY] in [0, 3]:
                self.sectors.append([self.posX+x, self.posY])
            elif map[self.posX+x][self.posY] == 2:
                self.sectors.append([self.posX+x, self.posY])
                break
            
        for x in range(1, self.range):
            if map[self.posX - x][self.posY] == 1:
                break
            elif self.has_bonus(self.posX-x, self.posY, bonuses):
                self.sectors.append([self.posX-x, self.posY])
                break
            elif map[self.posX-x][self.posY] in [0, 3]:
                self.sectors.append([self.posX-x, self.posY])
            elif map[self.posX-x][self.posY] == 2:
                self.sectors.append([self.posX-x, self.posY])
                break
            
        for x in range(1, self.range):
            if map[self.posX][self.posY + x] == 1:
                break
            elif self.has_bonus(self.posX, self.posY+x, bonuses):
                self.sectors.append([self.posX, self.posY+x])
                break
            elif map[self.posX][self.posY+x] in [0, 3]:
                self.sectors.append([self.posX, self.posY+x])
            elif map[self.posX][self.posY+x] == 2:
                self.sectors.append([self.posX, self.posY+x])
                break
            
        for x in range(1, self.range):
            if map[self.posX][self.posY - x] == 1:
                break
            elif self.has_bonus(self.posX, self.posY-x, bonuses):
                self.sectors.append([self.posX, self.posY-x])
                break
            elif map[self.posX][self.posY-x] in [0, 3]:
                self.sectors.append([self.posX, self.posY-x])
            elif map[self.posX][self.posY - x] == 2:
                self.sectors.append([self.posX, self.posY-x])
                break
            
