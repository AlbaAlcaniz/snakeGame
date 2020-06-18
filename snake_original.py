import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# import os, sys
# with open(os.devnull, 'w') as f:
#     # disable stdout
#     oldstdout = sys.stdout
#     sys.stdout = f

#     import pygame

#     # enable stdout
#     sys.stdout = oldstdout

class cube(object):
    rows = 20
    width = 500
    def __init__(self, start, dirnx = 1, dirny = 0, color = (255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes = False):
        dis = self.width // self.rows
        i = self.pos[0] #row
        j = self.pos[1] #column

        #So we draw inside the square
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis+dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        # Direction for x and y
        self. dirnx = 0
        self. dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                #Change the direction 
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0

                    #We need to remember where we turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0

                    #We need to remember where we turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1

                    #We need to remember where we turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1

                    #We need to remember where we turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        # look the positions of the bosy of the snake
        # get the index and cube object in the body
        for i, c in enumerate(self.body):
            #Makes a copy so we don't change the position of the snake
            #Grab the position of each object and see if it's in the turn list
            p = c.pos[:] #Position
            if p in self.turns:
                # The actual turns is the turn direction give by the keyboard
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                # If we're on the last cube
                if i == len(self.body)-1:
                    #Remove that cube
                    self.turns.pop(p)
            # If the position is not in the list
            else:
                # The snake hits the edges of the screen
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
                else: c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))
        
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                #Only to add this to draw the eyes of the snake
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid(width, rows, surface):
    # How big each square is gonna be
    size_between = width // rows
    x = 0
    y = 0
    for l in range(rows):
        x += size_between
        y += size_between

        color_lines = (255, 255, 255)
        # draw the lines
        pygame.draw.line(surface, color_lines, (x, 0), (x, width))
        pygame.draw.line(surface, color_lines, (0, y), (width, y))

    pass    

def redrawWindow(surface):
    global rows, width, s, snack
    color_surface = (0, 0, 0)
    surface.fill(color_surface)
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

    pass

def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        # Make sure we don't put a snack on top of the snake
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)

def message_box(subject, content):
    #Make sure that the window appears on top
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    width = 500
    # Rows needs to divide evenly by width
    rows = 20
    win = pygame.display.set_mode((width, width))
    position = (int(rows/2), int(rows/2))
    color = (255, 0, 0)
    s = snake(color, position)
    snack = cube(randomSnack(rows, s), color = (0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        # The two below commands play with the velocity of the snake
        pygame.time.delay(50)
        #Makes sure that the game runs at 10 frame per second
        clock.tick(10)
        #Snake moves
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color = (0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You lost!', 'Play again...')
                s.reset((10,10))
                break

        redrawWindow(win)

        


    pass


main()