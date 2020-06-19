# Import packages
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    """This class creates and manages the cubes. 
    They represent the snack and the snake, since aesthetically this game is not so nice (yet)
    """
    rows = 20
    width = 500
    def __init__(self, start, dirnx = 1, dirny = 0, color = (255,0,0)):
        """Initialize the cube objects by setting the arguments:

        Args:
            start (array (x,y)): initial position of the cube
            dirnx (int): movement on x direction. Defaults to 1.
            dirny (int): movement on y direction. Defaults to 0.
            color (tuple): Color of the cube. Defaults to red, for the apple.
        """
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        """Function that defines the movement of the cube, according to the x and y directions.
        By looking at how the position is changed, I think it's self-explanatory

        Args:
            dirnx (int): movement on x direction
            dirny (int): movement on y direction
        """
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes = False):
        """Function that draws the cube itself.

        Args:
            surface (window?): window in which the cube will be displayed
            eyes (bool, optional): Whether the eyes of the snake are drawn or not. 
            Defaults to False because the snake only has eyes on the head (xD)
        """
        dis = self.width // self.rows #width of each square of the grid
        i = self.pos[0] #row
        j = self.pos[1] #column

        # We draw the square in which the cube is
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        
        # We don't want the snake blind, so we better draw some eyes on the head cube
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis+dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    """Create a class for the snake
    """
    # Initialize the body and the turns, which represent the directions given by the player
    # This commands are useful when resetting the game
    body = []
    turns = {}
    def __init__(self, color, pos):
        """Initialize the head of the snake 

        Args:
            color (tuple): color of the snake.
            pos (array (x,y)): initial position of the head of the snake
        """
        self.color = color
        self.head = cube(pos) #Initialize the head of the snake by initializing its cube
        self.body.append(self.head) #The body contains the head as well as the rest of cubes of the snake
        # Direction for x and y
        self. dirnx = 0
        self. dirny = 1

    def move(self):
        """This function defines the movement of the snake following the instructions given by the 
        player and the previous turns performed by the snake.
        """
        # An event is an interaction of the player
        for event in pygame.event.get():
            # If the player wants to quit, he/she should have the right, right?
            if event.type == pygame.QUIT:
                pygame.quit()

            # If a key is pressed, we need to know which one is
            keys = pygame.key.get_pressed()

            for key in keys:
                # In this for loop, we change the direction of the snake according to the key
                # pressed by the player 
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
        """Function for resetting the snake after the player has lost

        Args:
            pos (array (x,y)): original position of the snake
        """
        # The next commands initialize the snake performing almost the same as the __init__ function
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        """When the snake eats a snack, it grows by adding a cube to its body
        """
        # Need to know the position and movement of the tail so that the next cube is added consistently
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # Depending on the movement of the tail, the new cube is added on one direction or the other
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))
        
        # Set the direction for the added cube
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        """Draw the snake so that the player knows what is going on

        Args:
            surface (window?): window in which the snake will be displayed
        """
        # Draw all the cubes which represent the snake
        for i, c in enumerate(self.body):
            if i ==0:
                #Only to add this to draw the eyes of the snake
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid(width, rows, surface):
    """This function draws the white lines on top of the black background which represents the 
    grid, where the snake and the snack will be displayed and interact with the user.

    Args:
        width (int): width of the window created
        rows (int): number of rows by which the grid will be divided
        surface (window?): window in which the grid will be displayed
    """
    # How big each square is gonna be
    size_between = width // rows

    # Plot all the horizontal and vertical white lines
    x = 0
    y = 0
    for l in range(rows):
        x += size_between
        y += size_between

        color_lines = (255, 255, 255) #White
        # Draw the white lines which divide the grid
        pygame.draw.line(surface, color_lines, (x, 0), (x, width))
        pygame.draw.line(surface, color_lines, (0, y), (width, y))

    pass    

def redrawWindow(surface):
    """For every frame, you need to redraw the grid, the snake and the snack.
    Otherwise it would be quite caothic.
    Maybe it could be optimized by not redrawing everything, but only what changes, but it's not
    straightforward for me yet.

    Args:
        surface (window?): window in which the grid will be displayed
    """
    # s is the snake, the rest of variables I find them self-explanatory
    global rows, width, s, snack
    color_surface = (0, 0, 0) #Black
    surface.fill(color_surface) #Black background
    s.draw(surface) #Plot the snake
    snack.draw(surface) #Plot the snack
    drawGrid(width, rows, surface) #Plot the white lines of the grid
    pygame.display.update() #Update the changes done on the window

    pass

def randomSnack(rows, item):
    """After the snake has eaten the snack, a new snack has to appear in a random position.
    This function gives you the new position of the snack

    Args:
        rows (int): rows in which the grid is divided. Useful so that the new snack position is inside
        the grid
        item (object): It's the snake. Calling it an item is objectifying it!! It has feelings!! ;p

    Returns:
        position x, y: new random position for the snack
    """
    # Get the positions of the body of the snake
    positions = item.body

    while True:
        # Find a new random position for the snack
        x = random.randrange(rows)
        y = random.randrange(rows)
        # Make sure we don't put a snack on top of the snake
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)

def message_box(subject, content):
    """Message box that appears at the beginning and end of the game

    Args:
        subject (string): message that appears on the top of the window
        content (string): message seen by the player
    """
    # Create a new window in which the player can choose to play again
    root = tk.Tk()
    # Make sure that the window appears on top
    root.attributes('-topmost', True)
    root.withdraw()
    # Display a simple message box
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    """Main function which relates the rest of functions and classes
    """
    # Make global all the following self-explanatory variables (s = snake)
    global width, rows, s, snack

    # Width of the pygame window
    width = 500
    # Rows needs to divide evenly by width
    rows = 20
    # Create the square pygame window of size width
    win = pygame.display.set_mode((width, width))
    # Determine the initial position of the snake in the middle of the window
    position = (int(rows/2), int(rows/2))
    color = (255, 0, 0) # color of the snake
    s = snake(color, position) #Initialize the snake
    snack = cube(randomSnack(rows, s), color = (0, 255, 0)) #Initialize the snack
    flag = True #auxiliar variable which is true until you lost

    clock = pygame.time.Clock() # activate the game clock

    while flag: #As long as you don't lose...

        # The two below commands play with the velocity of the snake
        pygame.time.delay(50)
        #Makes sure that the game runs at 10 frame per second
        clock.tick(10)

        #Snake moves
        s.move()
        # If the snake moves to the position of the snack, add a new cube to it and choose a new
        # random position for the snack
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color = (0, 255, 0))

        # If the snake eats itself (not something very intelligent to do), you lose
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                # Print the score, that is the length of the snake, achieved by the player
                print('Score: ', len(s.body))
                # Display a message for playing again
                message_box('You lost!', 'Play again...')
                # Reset the game
                s.reset((10,10))
                break
        
        # every frame (or however you call it) redraw the window
        redrawWindow(win)

    pass

# Run the main function
main()