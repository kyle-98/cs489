import pygame
import random
import time

pygame.init()
displayWidth = 900 
displayHeight = 700

display = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

def message(msg, mType, x, y, color):
    msg = mType.render(msg, True, color)
    display.blit(msg, (x, y))


##################################################################################
#<---------- Players Class ---------->
##################################################################################
class Players():
    speed = 10

    def __init__(self, x, y, w, h):
        self.x, self.resetX = x, x
        self.y, self.resetY = y, y
        self.width = w
        self.height = h

    def drawPlayers(self):
        pygame.draw.rect(display, (255,255,255), (self.x, self.y, self.width, self.height))

    def movePlayer(self, up=True):
        if up:
            self.y -= self.speed
        else:
            self.y += self.speed
    
    def resetPlayers(self):
        self.x = self.resetX
        self.y = self.resetY

class AI():
    def __init__(self, x, y, w, h):
        self.x, self.resetX = x, x
        self.y, self.resetY = y, y
        self.width = w
        self.height = h
        self.speed = 10

        self.resetTime = time.time()
        self.failRate = .27
        self.failTime = .5
        self.nextFail = time.time()
    
    def drawAI(self):
        pygame.draw.rect(display, (255,255,255), (self.x, self.y, self.width, self.height))

    def moveAI(self, up=True):
        if time.time() > self.nextFail:
            if random.random() <= self.failRate:
                self.resetTime = time.time() + self.failTime
            self.nextFail = time.time() + 1.0
        
        if time.time() < self.resetTime:
            speed = 0
        else:
            speed = self.speed

        if up:
            self.y -= speed
        else:
            self.y += speed
        #print(speed)
    
    def resetAI(self):
        self.x = self.resetX
        self.y = self.resetY
        


##################################################################################
#<---------- Ball Class ---------->
##################################################################################
class Ball():
    maxSpeed = 11

    def __init__(self, x, y):
        self.x, self.resetX = x, x
        self.y, self.resetY = y, y
        self.radius = 10
        self.xVelocity = self.maxSpeed
        self.yVelocity = 0

    def drawBall(self):
        pygame.draw.circle(display, (255,255,255), (self.x, self.y), self.radius)
    
    def moveBall(self):
        self.x += self.xVelocity
        self.y += self.yVelocity

    def resetBall(self):
        self.x = self.resetX
        self.y = self.resetY
        self.xVelocity *= -1
        self.yVelocity = 0

# Render Assets on Screen
def render(players, ai, ball):
    display.fill((0,0,0))
    players.drawPlayers()
    ai.drawAI()
    #for player in players:
    #    player.drawPlayers()
    ball.drawBall()

    #draw walls
    #pygame.draw.line(display, (255,255,255), (0,0), (0, displayHeight), 10)
    #pygame.draw.line(display, (255,255,255), (0,0), (displayWidth, 0), 10)
    #pygame.draw.line(display, (255,255,255), (displayWidth,0), (displayWidth, displayHeight), 10)
    #pygame.draw.line(display, (255,255,255), (0,displayHeight), (displayWidth, displayHeight), 10)

# Check if keys pressed are the arrow keys.
# Allow player to move up and down with arrow keys
# Restrict player from moving off screen
def playerMovement(keysList, player):
    if keysList[pygame.K_UP] and player.y - player.speed >= 0:
        player.movePlayer(up=True)

    if keysList[pygame.K_DOWN] and player.y + player.speed + player.height <= displayHeight:
        player.movePlayer(up=False)

# Move the ball, bouce ball off the player and the ai and the top and bottom portions of the screen
def ballMovement(ball, player, ai):
    if ball.y + ball.radius >= displayHeight:
        ball.yVelocity *= -1
    elif ball.y - ball.radius <= 0:
        ball.yVelocity *= -1

    if ball.xVelocity < 0:
        if ball.y >= player.y and ball.y <= player.y + player.height:
            if ball.x - ball.radius <= player.x + player.width:
                ball.xVelocity *= -1
                yValue = player.y + player.height / 2
                fractionMaxSpeed = (player.height / 2) / ball.maxSpeed
                yVelocity = (yValue - ball.y) / fractionMaxSpeed
                ball.yVelocity = -1 * yVelocity
    
    else:
        if ball.y >= ai.y and ball.y <= ai.y + ai.height:
            if ball.x + ball.radius >= ai.x:
                ball.xVelocity *= -1
                yValue = ai.y + ai.height / 2
                fractionMaxSpeed = (ai.height / 2) / ball.maxSpeed
                yVelocity = (yValue - ball.y) / fractionMaxSpeed
                ball.yVelocity = -1 * yVelocity

# ai movement
def aiMovement(ai, ball):
    if ai.y + (ai.height / 2) < ball.y:
        ai.moveAI(up=False)

    if ai.y + (ai.height / 2) > ball.y:
        ai.moveAI(up=True)

# check if the ball is out of bounds and return which side it went out of bounds on
def pointCheck(ball):
    if ball.x <= 0:
        return 0
    if ball.x >= displayWidth:
        return 1


scoreFont = pygame.font.SysFont(None, 40)
def scoreCount(playerScore, aiScore):
    message("Player Score: " + str(playerScore), scoreFont, 100, 0, (255,255,0))
    message("AI Score: " + str(aiScore), scoreFont, 600, 0, (255,255,0))



##################################################################################
#<---------- Game Function ---------->
##################################################################################
def game():
    go, gameStart = True, True
    playerWidth, playerHeight = 15, 90
    playerScore, aiScore = 0, 0
    startFont, logoFont, winFont = pygame.font.SysFont(None, 40), pygame.font.SysFont(None, 80), pygame.font.SysFont(None, 30)

    player = Players(30, displayHeight // 2 - playerHeight // 2, playerWidth, playerHeight)
    ai = AI(displayWidth - playerWidth - 30, displayHeight // 2 - playerHeight // 2, playerWidth, playerHeight)
    ball = Ball(displayWidth // 2, displayHeight // 2)

    while go:

        while gameStart:
            playerScore = 0
            aiScore = 0
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameStart = False
                        go = False
                        pygame.quit()
                    if event.key == pygame.K_SPACE:
                        gameStart = False
                    if event.key == pygame.K_r:
                        display.fill((0,0,0))
                        message("Use UP and DOWN arrow keys to control the player.", startFont, 100, 100, (255,0,0))
                        message("Hit the pong ball to the enemy side and score points by outplaying the AI.", startFont, 100, 150, (255,0,0))
                        pygame.display.update()
                    if event.key == pygame.K_t:
                        display.fill((0,0,0))

            message("Pong", logoFont, displayWidth // 2 - 80, displayHeight // 2 - 80, (255,255,255))
            message("Press SPACE to begin, press Q to quit, or press R for rules.", startFont, 50, displayHeight // 2 + 40, (255,255,255))
            pygame.display.update()



        render(player, ai, ball)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                go = False
                pygame.quit()

        keysList = pygame.key.get_pressed()
        #print(player.y)
        playerMovement(keysList, player)

        ball.moveBall()
        ballMovement(ball, player, ai)
        aiMovement(ai, ball)
        scoreCount(playerScore, aiScore)
        
        if pointCheck(ball) == 0:
            aiScore += 1
            ball.resetBall()
            player.resetPlayers()
            ai.resetAI()

        if pointCheck(ball) == 1:
            playerScore += 1
            ball.resetBall()
            player.resetPlayers()
            ai.resetAI()


        if playerScore == 5:
            message("You Won!", winFont, displayWidth // 2, displayHeight // 2, (0,255,0))
            pygame.display.update()
            time.sleep(2)
            gameStart = True
            display.fill((0,0,0))
        
        if aiScore == 5:
            message("You Lost!", winFont, displayWidth // 2, displayHeight // 2, (255,0,0))
            pygame.display.update()
            time.sleep(2)
            gameStart = True
            display.fill((0,0,0))
        #print(ai.y + (ai.height / 2), ball.y)
        pygame.display.update()
        clock.tick(60)

game() 
