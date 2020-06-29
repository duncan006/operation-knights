class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.crouchHeight = 30
        self.standHeight = 50
        self.height = self.standHeight
        self.width = 20
        self.speed = 5
        self.score = 0
        
        self.jumpCount = 0
        self.jumping = False
        self.jumpMult = 3
        self.jumpList = [6,6,6,6,6,4,4,4,4,2,2,2,1,1,0,-1,-1,-2,-2,-2,-4,-4,-4,-4,-6,-6,-6,-6,-6]
        
        self.heldLeft = False
        self.heldRight = False
        self.crouch = False
        
        
    def special_move_handler(self):
        if self.jumping and not self.crouch:
            self.y -= self.jumpMult * self.jumpList[self.jumpCount]
            self.jumpCount += 1
            if self.jumpCount > len(self.jumpList)-1:
                self.jumpCount = 0
                self.jumping = False
                
    def movePlayer(self):
        if self.heldLeft == True:
            self.x -= self.speed
        if self.heldRight == True:
            self.x += self.speed
