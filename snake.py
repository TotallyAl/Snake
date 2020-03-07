#!/Users/alexandre/opt/anaconda3/envs/Coding/bin/python

'''
This program is made to learn the pygame event loop
'''
import random
import pygame
from pygame.locals import *

pygame.init()

res_x = 1000
res_y = 500
margin = 50

# color definitions in (red, green, blue) format
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 127, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

def drawFruit (screen, fruit_coord, size=2, color=ORANGE):
    pygame.draw.circle(screen, color, fruit_coord, size)
    
def fruitsEaten (score, head, fruit):
    if head == fruit:
        score = score+1
        print(score)
    return score

''' This Function will only make a new fruit any where on the delimited screen(dimensions) except in the snake and out of the sreen dimesions'''
def newFruit(game_dimensions, snake):
    x = random.randint(game_dimensions[0][0], game_dimensions[0][0]+game_dimensions[1][0])
    y = random.randint(game_dimensions[0][1], game_dimensions[0][1]+game_dimensions[1][1])
    spawn_fruit = [x, y]
    return spawn_fruit

def drawDot(screen, coord, size=2, color=RED, thickness=1):
    # pygame.draw.rect(screen, color, [top_left_coord, dimensions], line_width)
    # top_left_coord = [x_coord, y_coord]
    # dimensions = [width, height]
    # pygame.draw.rect(screen, color, [[x_coord, y_coord], [width, height]], line_width)

    top_left = [coord[0]-size, coord[1]-size]
    side = size*2+1
    dimensions = [side, side]

    pygame.draw.rect(screen, color, [top_left, dimensions], 1)

'''gameDimensions: returns a vector with 2 components representing the x and y dimensions of the game area
   margin: the margin (in pixels) around the play areay. The margins will be deducted from the screen dimensions
   screen_dimensions: a vector with 2 components representing the x&y display size in pixels
'''
def gameArea(screen_dimensions, dot_size, board_size):
    dimensions = (dot_size*board_size[0], dot_size*board_size[1])
    top_left = [margin, margin]
    dimensions = (screen_dimensions[0]-2*margin, screen_dimensions[1]-2*margin)
    return [top_left, dimensions, dot_size]

def drawSides(screen, dimensions, color=GREEN):
    pygame.draw.rect(screen, color, dimensions, 1)

def snakeOutOfGame(snake, game_dimensions):
    head_snake = snake[0]
    top_left = game_dimensions[0]
    bottom_right = [top_left[0]+game_dimensions[1][0], top_left[1]+game_dimensions[1][1]]
    if head_snake[0] <= top_left[0]:
        return True
    elif head_snake[1] <= top_left[1]:
        return True
    elif head_snake[0] >= bottom_right[0]:
        return True
    elif head_snake[1] >= bottom_right[1]:
        return True
    return False

def sameCoordinates(coord1, coord2):
    if coord1[0] == coord2[0] and coord1[1] == coord2[1]:
        return True
    else:
        return False

def snakeBiteItself(snake):
    head_coord = snake[0]
    i=1
    while i < len(snake):
        if sameCoordinates(head_coord, snake[i]):
            return True
        i = i+1
    return False

def drawSnake(screen, snake, size=2, color=RED):
    drawDot(screen, snake[0], size, RED, 1)
    i = 1
    while i < len(snake):
        drawDot(screen, snake[i], size, color)
        i = i+1

def initSnake(coord, length, size=2):
    return [[coord[0]-(size*2+1)*x, coord[1]] for x in range(0, length)]

def __main__():
    # Initialize screen and window
    screen = pygame.display.set_mode((res_x, res_y))
    pygame.display.set_caption("Game Test")
    #draw the snake head
    head_coord = [res_x/2, res_y/2]
    dot_half_edge = 8
    dot_size = [2*dot_half_edge, 2*dot_half_edge]
    head_speed = [dot_size[0],0]

    snake = initSnake(head_coord, 10, dot_half_edge)

    # define the actual dimensions of the game.
    game_area = gameArea(margin, [res_x, res_y], dot_size)

    fruit = newFruit(game_area, snake)
    score = 0

    running = True
    while running:
        # Fill the screen with a color (here: black)
        screen.fill(BLACK)

        #Fruit score
        score = fruitsEaten(score, head_coord, fruit)

        # draw some stuff here
        drawSides(screen, game_area, color = GREEN)

        #drawDot(screen, head_coord, dot_half_edge, color=WHITE)
        drawSnake(screen, snake, dot_half_edge, color=YELLOW)
        drawFruit(screen, fruit)
        # brings the screen updated
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if (event.key == K_q) or (event.key == K_ESCAPE):
                    running = False
                
                elif (event.key == K_RIGHT):
                    if head_speed[0] >= 0:
                        head_speed[0] = dot_size[0]
                        head_speed[1] = 0
                elif (event.key == K_LEFT):
                    head_speed[0] = -dot_size[0]
                    head_speed[1] = 0
                elif (event.key == K_DOWN):
                    head_speed[0] = 0
                    head_speed[1] = dot_size[1]
                elif (event.key == K_UP):
                    head_speed[0] = 0
                    head_speed[1] = -dot_size[1]
            '''
            elif event.type == KEYUP:
                if (event.key == K_DOWN):
                    dot_direction[1] = 0
                elif (event.key == K_UP):
                    dot_direction[1] = 0
                elif (event.key == K_RIGHT):
                    dot_direction[0] = 0
                elif (event.key == K_LEFT):
                    dot_direction[0] = 0
            '''

        if (head_speed[0] != 0 or head_speed[1] != 0):
            head_coord[0] = head_coord[0]+head_speed[0]
            head_coord[1] = head_coord[1]+head_speed[1]
            snake.insert(0, [head_coord[0], head_coord[1]])
            snake.pop()
            if snakeBiteItself(snake):
                print("The snake tried to eat itself sorry GameOver !")
                running = False
            if snakeOutOfGame(snake, game_area):
                print("The snake ran out of the screen")
                running = False
            #print(snake)

            #     else:
            #         print("Key Down:")
            #         print(event.key)
            # elif event.type == KEYUP:
            #     print("Key Up:")
            #     print(event.key)
            # elif event.type == MOUSEMOTION:
            #     print("Mouse Motion")
            #     print(event.pos)
            # elif event.type == MOUSEBUTTONDOWN:
            #     pos = pygame.mouse.get_pos()
            #     print("Mouse Button Down")
            #     print(event.button)

    pygame.quit()

__main__()
