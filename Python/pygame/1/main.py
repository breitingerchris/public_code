import pygame
import colors
import random


class Game(object):
    def __init__(self):
        

pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Game')
pygame.display.update()
Colors = colors.Colors()
clock = pygame.time.Clock()


def draw(color, rect):
    gameDisplay.fill(color, rect=rect)


def main():
    xPos = 300
    yPos = 300
    width = 3
    height = 1
    snake = [xPos, yPos, width * 50, height * 50]
    block = [random.randint(0, 15) * 50, random.randint(0, 15) * 50, 50, 50]
    direction = 'R'
    gameExit = False
    gameDisplay.fill(Colors.white)
    draw(Colors.red, snake)
    draw(Colors.red, block)

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.K_RIGHT:
                if direction == 'L':
                    pass
                else:

            if event.type == pygame.K_LEFT:
                if direction == 'R':
                    pass
            if event.type == pygame.K_UP:
                if direction == 'D':
                    pass
            if event.type == pygame.K_DOWN:
                if direction == 'U':
                    pass

            if event.type == pygame.QUIT:
                gameExit = True
        pygame.display.update()
        clock.tick(10)


if __name__ == '__main__':
    main()
