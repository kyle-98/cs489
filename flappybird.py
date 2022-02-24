import pygame
import random

pygame.init()
displayWidth = 700
displayHeight = 900

display = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()


lossFont = pygame.font.SysFont(None, 40)
scoreFont = pygame.font.SysFont(None, 100)
generalFont = pygame.font.SysFont(None, 100)

def message(msg, mType, x, y, color):
    msg = mType.render(msg, True, color)
    display.blit(msg, (x, y))
    pygame.display.update()

def dropShadowMessage(msg, mType, x, y, color):
    mesg = mType.render(msg, True, (0,0,0))
    display.blit(mesg, (x + 2, y + 2))
    mesg = mType.render(msg, True, color)
    display.blit(mesg, (x, y))   
    pygame.display.update()

##################################################################################
#<---------- Background Class ---------->
##################################################################################
class background:
    def __init__(self):
        self.bgImage = pygame.image.load('city_bg.png')
        self.rectBg = self.bgImage.get_rect()

        self.bgY = 0
        self.bgX = 0
        self.bgY2 = 0
        self.bgX2 = self.rectBg.width

        self.movingSpeed = 5

    def moveBG(self):
        self.bgX -= self.movingSpeed
        self.bgX2 -= self.movingSpeed

        if self.bgX <= -self.rectBg.width:
            self.bgX = self.rectBg.width

        if self.bgX2 <= -self.rectBg.width:
            self.bgX2 = self.rectBg.width
    
    def displayBG(self):
        display.blit(self.bgImage, (self.bgX, self.bgY))
        display.blit(self.bgImage, (self.bgX2, self.bgY2))

##################################################################################
#<---------- Pipes Object Class ---------->
##################################################################################
class pipes():
    def __init__(self):
        self.bottomPipeImage = pygame.image.load('pipe.png').convert_alpha()
        self.bottomPipeImage = pygame.transform.smoothscale(self.bottomPipeImage, (130, 700))
        self.topPipeImage = pygame.transform.flip(self.bottomPipeImage, False, True)
        self.rectTopPipe = self.topPipeImage.get_rect()
        self.rectBottomPipe = self.bottomPipeImage.get_rect()
        
        self.scoreBoxImage = pygame.image.load('score.png').convert_alpha()
        self.rectScoreBox = self.scoreBoxImage.get_rect()

        self.pScore = 0

        #<------ Top Pipe X Coords ------>
        self.topPipeX = 0
        self.topPipeX2 = displayWidth + 50

        #<------ Bottom Pipe X Coords ------>
        self.bottomPipeX = 0
        self.bottomPipeX2 = displayWidth + 50

        self.disApart = 150
        self.movingSpeed = 5

        #<------ Generate Y-Values for Pipes ------>
        self.height = random.randint(350,870)
        self.height2 = (displayHeight - self.height) + 100
        
    def movePipes(self):
        #<------ moving top pipe ------>
        self.topPipeX -= self.movingSpeed
        self.topPipeX2 -= self.movingSpeed

        if self.topPipeX <= -self.rectBottomPipe.width:
            self.topPipeX = displayWidth

        if self.topPipeX2 <= -self.rectBottomPipe.width:
            self.topPipeX2 = displayWidth

        #<------ moving bottom pipe ------>
        self.bottomPipeX -= self.movingSpeed
        self.bottomPipeX2 -= self.movingSpeed

        if self.bottomPipeX <= -self.rectBottomPipe.width:
            self.bottomPipeX = displayWidth

        if self.bottomPipeX2 <= -self.rectBottomPipe.width:
            self.bottomPipeX2 = displayWidth

    
    def spawnPipes(self):
        #<------ Render Pipes ------>
        display.blit(self.topPipeImage, (self.topPipeX2, -self.height2))
        display.blit(self.bottomPipeImage, (self.bottomPipeX2, self.height))
        
        #<------ Update Collision Boxes for Pipes ------>
        self.rectTopPipe = self.topPipeImage.get_rect(topleft=(self.topPipeX2, -self.height2)) 
        self.rectBottomPipe = self.bottomPipeImage.get_rect(topleft=(self.bottomPipeX2, self.height))

        #<------ Enable to Render HitBoxes ------>
        #pygame.draw.rect(display, (255,255,0), self.rectTopPipe)
        #pygame.draw.rect(display, (255,255,0), self.rectBottomPipe)

        #<------ Score Counter ------>
#        self.rectScoreBox = pygame.Rect((self.rectTopPipe[0] + self.rectTopPipe.width) + 30, self.rectTopPipe[1] + 670, 1, 350)
        self.rectScoreBox = self.scoreBoxImage.get_rect(topleft=((self.rectTopPipe[0] + self.rectTopPipe.width + 30), self.rectTopPipe[1] + 670))
        #pygame.draw.rect(display, (0,255,0), self.rectScoreBox)
        
    def pCollide(self): 
        return(self.rectTopPipe, self.rectBottomPipe, self.rectScoreBox)
"""
    def scoreCollide(self, pCoords):
        scoreAdd = pCoords.colliderect(self.rectScoreBox)
        #print(self.rectScoreBox)
        if scoreAdd:
            print(1)
            self.pScore += 1
            #self.rectScoreBox.move_ip(100,100)
            #print(1)

    def returnScore(self):
        return self.pScore
"""

##################################################################################
#<---------- Player Class ---------->
##################################################################################
class bird(pipes):
    
    def __init__(self):
        self.playerImage = pygame.image.load('bird.png').convert_alpha()
        self.playerImage = pygame.transform.smoothscale(self.playerImage, (70,45))
        self.playerRect = self.playerImage.get_rect(center=(100,400))
        self.pScore = 0
        self.loss = False
        
    def moveBird(self, val):
        self.playerRect[1] += val
        #print(self.playerRect.center)
        
    def spawnBird(self):
        display.blit(self.playerImage, self.playerRect)
        
        #<------ Enable to Render Player HitBox ------>
        #pygame.draw.rect(display, (255,0,0), self.playerRect)
        
    def collisions(self, coords):
        topCoords = coords[0]
        bottomCoords = coords[1]
        topLoss = self.playerRect.colliderect(topCoords)
        bottomLoss = self.playerRect.colliderect(bottomCoords)

        #print(self.playerRect)

        if self.playerRect[1] < 0 or self.playerRect[1] > 900:
            topLoss = True

        if topLoss or bottomLoss:
            #message("You Lost Press Q to quit or R to replay.", lossFont, 0, 500, (255,0,0))
            self.loss = True

    def returnLoss(self):
        return self.loss       

    def birdLoc(self):
        return self.playerRect

    def score(self, coords):
        scoreCoords = coords[2]
        scoreAdd = self.playerRect.colliderect(scoreCoords)
        if scoreAdd:
            self.pScore += 1

    def currScore(self):
        return self.pScore


def scoreCount(score):
    dropShadowMessage(str(score // 14), scoreFont, 320, 200, (255,255,255))
    #s = scoreFont.render(str(score // 14), True, (255,50,5))
    #display.blit(s, (0,0))


##################################################################################
#<---------- Game Function ---------->
##################################################################################
def game():
    pipesList = []
    count = 0
    BACKGROUND = background()
    BIRD = bird()
    PIPES = pipes()
    close = False
    start = True
    go = True
    while go:
        
        while close:
            message("You Lost Press Q to quit or R to replay.", lossFont, 100, 500, (255,0,0))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        go = False
                        close = False
                    if event.key == pygame.K_r:
                        game()
        while start:
            display.fill((0,0,0))
            message("Flappy Bird", generalFont, 150, 300, (255,255,255))
            message("Press Space To Start", lossFont, 200, 400, (255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                go = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
                BIRD.moveBird(-80)

        BACKGROUND.moveBG()
        BACKGROUND.displayBG()

        count += 1
        BIRD.spawnBird()
        BIRD.moveBird(6)
        #BIRD.returnLoss()

        if BIRD.returnLoss():
            close = True
    
        if count > 58:
            new_pipes = pipes()
            pipesList.append(new_pipes)
            count = 0
            print("len =",len(pipesList))
        
        for pipe in pipesList:
            pipe.movePipes()
            pipe.spawnPipes()
            returnInfo = pipe.pCollide()
            BIRD.collisions(returnInfo)  
            #pipe.scoreCollide(BIRD.birdLoc())
            #scoreCount(pipe.returnScore())    
            BIRD.score(returnInfo)
        
        if len(pipesList) > 3:
            print("deleting",pipesList[:1])
            del pipesList[:1]

        #scoreCount(PIPES.returnScore()) 
        scoreCount(BIRD.currScore())

        pygame.display.update()
        clock.tick(32)

game()
