#!/usr/bin/python3

import pygame
import random
pygame.init()

height = 600
width = 600
display = pygame.display.set_mode([width, height])
bg = pygame.image.load("grass.jpg").convert()
bg = pygame.transform.scale(bg, [width,height])

pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
snakeSpeed = 15
snakeSize = 20

fontType = pygame.font.SysFont(None, 40)
scoreFont = pygame.font.SysFont(None, 40)

def currScore(score):
    value = scoreFont.render("Score: " + str(score), True, (255,255,0))
    display.blit(value, [0,0])

def ourSnake(snakeSize, snakeList):
    for x in snakeList:
        pygame.draw.rect(display, (255,0,255), [x[0], x[1], snakeSize, snakeSize])
        #display.blit(snakeImage, [x[0], x[1], snakeSize, snakeSize])

def message(msg, w, h, color):
    msg = fontType.render(msg, True, color)
    display.blit(msg, [w, h])
    pygame.display.update()

def game():
    go = True
    close = False

    x = width / 2
    y = height / 2
    tempX = 0
    tempY = 0

    foodX = round(random.randrange(0, width - snakeSize) / 20.0) * 20.0
    foodY = round(random.randrange(0, width - snakeSize) / 20.0) * 20.0

    snakeList = []
    lengthOfSnake = 1

    while go:

        while close == True:
            message("You Lost! Press Q to quit or R to play again.", 0, 350, (255,0,0))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        go = False
                        close = False
                    if event.key == pygame.K_r:
                        game()

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                go = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tempX = -snakeSize
                    tempY = 0
                if event.key == pygame.K_RIGHT:
                    tempX = snakeSize
                    tempY = 0
                if event.key == pygame.K_UP:
                    tempX = 0
                    tempY = -snakeSize
                if event.key == pygame.K_DOWN:
                    tempX = 0
                    tempY = snakeSize
        
        if x >= width or x < 0 or y > height or y < 0:
            close = True

        x += tempX
        y += tempY
        display.blit(bg, [0,0])
        #pygame.draw.rect(display, (255,0,255),[x, y, snakeSize, snakeSize])
        pygame.draw.rect(display, (0,255,0), [foodX, foodY, snakeSize, snakeSize])
        #display.blit(snakeImage, [foodX, foodY, snakeSize, snakeSize])
        snakeHead = []
        snakeHead.append(x)
        snakeHead.append(y)
        snakeList.append(snakeHead)
        if len(snakeList) > lengthOfSnake:
            del snakeList[0]
        
        for i in snakeList[:-1]:
            if i == snakeHead:
                close = True

        ourSnake(snakeSize, snakeList)
        currScore(lengthOfSnake - 1)
        pygame.display.update()

        if x == foodX and y == foodY:
            foodX = round(random.randrange(0, width - snakeSize) / 20.0) * 20.0
            foodY = round(random.randrange(0, height - snakeSize) / 20.0) * 20.0
            lengthOfSnake += 1
       
        pygame.display.update()
        clock.tick(snakeSpeed)
        
    pygame.quit()
    quit()

game()
