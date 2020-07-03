#!/Users/alexandre/opt/anaconda3/envs/Coding/bin/python
import pygame
from pygame.locals import *
from math import pi
import time
import random
import sys
import pickle

#colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

class Display:
    res_x = 1200
    res_y = 800
    dot_size = 20
    board_x = 51
    board_y = 31

    def __init__(self):
        self.screen = pygame.display.set_mode((self.res_x, self.res_y))
        pygame.display.set_caption("Snake")
        self.icon = pygame.image.load('graphics/snake.png')
        pygame.display.set_icon(self.icon)


    def marginCoord(self):
        margin_x = (self.res_x - self.board_x*self.dot_size)/2
        margin_y = (self.res_y - self.board_y*self.dot_size)/2 

        return margin_x, margin_y

    def drawMargins(self):
        margin_x, margin_y = self.marginCoord()
        pygame.draw.rect(self.screen, GREEN, ((margin_x, margin_y), (self.res_x - margin_x*2, self.res_y - margin_y*2)), 1)

class Snake:
    def __init__ (self, length, head_x, head_y):
        self.body = [(head_x, head_y)]
        self.direction_x = 1
        self.direction_y = 0
        self.elongate = length

    def move (self):
        head = self.body[0]
        new_head = (head[0]+self.direction_x, head[1]+self.direction_y)
        self.body.insert(0, new_head)
        if self.elongate > 0:
            self.elongate = self.elongate - 1
        else:
            self.body.pop()

    def render (self, display):
        margin_x, margin_y = display.marginCoord()
        index = 0
        while index<len(self.body):
            x = margin_x + self.body[index][0]*display.dot_size
            y = margin_y + self.body[index][1]*display.dot_size
            pygame.draw.rect(display.screen, RED, ((x, y), (display.dot_size, display.dot_size)))
            index = index+1

    def biteSelf (self):
        head = self.body[0]
        index = 1
        while index < len(self.body):
            if (head[0] == self.body[index][0]) and (head[1] == self.body[index] [1]):
                return True
            index = index +1
        return False

    def bitWall (self, display):
        head = self.body[0]
        if (head[0] < 0) or (head[1] < 0) or (head[0] >= display.board_x) or (head[1] >= display.board_y):
            return True
        return False

    def bitApple (self, apple):
        head = self.body[0]
        if (head[0] == apple.x) and (head[1] == apple.y):
            return True
        return False

class Apple:
    def __init__(self, display):
        self.x = random.randrange(display.board_x)
        self.y = random.randrange(display.board_y)
        self.image = pygame.image.load("graphics/apple.png")
        self.image = pygame.transform.scale(self.image, (display.dot_size, display.dot_size))
        self.eat_sound = pygame.mixer.Sound("sounds/Jump.wav")

    def render (self, display):
        margin_x, margin_y = display.marginCoord()
        x = margin_x + self.x*display.dot_size
        y = margin_y + self.y*display.dot_size
        #pygame.draw.rect(display.screen, GREEN, ((x, y), (display.dot_size, display.dot_size)))
        display.screen.blit(self.image, (x, y))

class Scoreboard:
    def __init__ (self, display, res_x, res_y):
        self.x = int(display.res_x/2)
        self.y = 0
        self.score = 0
        self.font = pygame.font.SysFont(None, 25)
        self.prepareText()


    def render (self, display):
        display.screen.blit(self.screen_text, [self.x , self.y])

    def prepareText (self):
        msg = "Score: {}".format(self.score)
        self.screen_text = self.font.render(msg, True, WHITE)

    def increaseScore (self):
        self.score = self.score +1
        self.prepareText()

    def store (self):
        pickle.dump(self.score, open("score.txt", "wb"))
        print(self.score)

class MainGame:
    def __init__(self, display):
        self.snake = Snake(5, int(display.board_x/2), int(display.board_y/2))
        self.scoreboard = Scoreboard(display, 1200, 800)
        self.apple = Apple(display)
        self.background = pygame.image.load("graphics/bg0.png")
        self.background = pygame.transform.scale(self.background, (display.res_x, display.res_y))
        pygame.mixer.music.load("sounds/popcorn.ogg")
        pygame.mixer.music.play()

    def __del__(self):
        pygame.mixer.music.stop()

    def loop (self, display):
        time.sleep(.05)
        #The border
        self.snake.move()
        #display.screen.fill(BLACK)
        display.screen.blit(self.background, [0,0])
        display.drawMargins()
        self.scoreboard.render(display)
        self.snake.render(display)
        self.apple.render(display)
        if self.snake.biteSelf() == True:
            print("SSSSSSSS NO I BIT MYSSSSSELF")
            pygame.mixer.music.play()
            return False
        if self.snake.bitWall(display) == True:
            print("SSSSS I BROKE A TOOTH")
            pygame.mixer.music.play()
            return False
        if self.snake.bitApple(self.apple) == True:
            self.scoreboard.increaseScore()
            pygame.mixer.Sound.play(self.apple.eat_sound)
            self.snake.elongate = self.snake.elongate + 4
            self.apple = Apple(display)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    return False
                if event.key == pygame.K_UP:
                    self.snake.direction_y = -1
                    self.snake.direction_x = 0
                if event.key == pygame.K_DOWN:
                    self.snake.direction_y = 1
                    self.snake.direction_x = 0
                if event.key == pygame.K_RIGHT:
                    self.snake.direction_x = 1
                    self.snake.direction_y = 0
                if event.key == pygame.K_LEFT:
                    self.snake.direction_x = -1
                    self.snake.direction_y = 0
                if event.key == pygame.K_SPACE:
                    self.snake.elongate = self.snake.elongate + 4
        return True

class MainMenu:
    def __init__ (self, display):
        self.x = display.res_x /2
        self.y = display.res_y /2
        self.font = pygame.font.SysFont(None, 35)
        self.prepareText()
        pygame.mixer.music.load("sounds/myriapod-theme.ogg")
        pygame.mixer.music.play()

    def __del__ (self):
        pygame.mixer.music.stop()

    def render (self, display):
        display.screen.fill(BLACK)
        width, height = self.screen_text.get_size()
        display.screen.blit(self.screen_text, [self.x-width/2, self.y-height/2])
        pygame.display.update()

    def prepareText (self):
        msg = "Press Space bar to start the game"
        self.screen_text = self.font.render(msg, True, RED)

    def loop (self, display):
        
        self.render(display)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    return False
                if event.key == pygame.K_SPACE:
                    return False
        return True


#Initialize pygame
pygame.init()
pygame.mixer.init()
#Making the screen
display = Display()
scoreboard = Scoreboard(display, 1200, 800)
while True:
    print("Main menu")
    menu = MainMenu(display)
    while menu.loop(display) == True:
        pass
    del menu

    print("Starting Game")
    game = MainGame(display)
    while game.loop(display) == True:
        pass
    del game

scoreboard.store()
pygame.quit()

