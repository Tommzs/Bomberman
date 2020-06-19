class Controls:
    def __init__(self, up, down, left, right, bomb):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.bomb = bomb

    def getRight(self):
        return self.right

    def getLeft(self):
        return self.left

    def getUp(self):
        return self.up

    def getDown(self):
        return self.down

    def getBomb(self):
        return self.bomb
