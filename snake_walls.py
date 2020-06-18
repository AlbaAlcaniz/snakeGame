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
        # Variable which tells us whether the snake has hit the walls (1) or not (0). 
        self. walls_hit = 0

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

        # look the positions of the body of the snake
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
        
        # If the user has decided to play with the walls active
        if walls == 1:
            # You lose if the snake hits the edges of the screen
            if c.dirnx == -1 and self.head.pos[0] == c.rows-1: s.walls_hit = 1
            if c.dirnx == 1 and self.head.pos[0] == 0: s.walls_hit = 1        
            if c.dirny == 1 and self.head.pos[1] == 0: s.walls_hit = 1
            if c.dirny == -1 and self.head.pos[1] == c.rows-1: s.walls_hit = 1

    def reset(self, pos):
        """FUnction for resetting the snake after the player has lost

        Args:
            pos (array (x,y)): original position of the snake

        Returns:
            walls: function which tells you whether the player has decided to turn on the walls or not
        """
        walls = message_box_levels('Welcome to the snake!') #The player chooses the walls active or not
        # The next commands initialize the snake performing almost the same as the __init__ function
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        self.walls_hit = 0
        return walls

    def addCube(self):
        """When the snake eats a snack, it grows by adding a cube to its body
        """
        # Need to know the position ad movement of the tail so that the next cube is added consistently
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
    color_lines = (255, 255, 255) #White
    for l in range(rows):
        x += size_between # Every iteration add the size of the square in order to plot the next line
        y += size_between

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
        # Make sure we don't put a snack on top of the snake. Otherwise, just look for a new position
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)

def lost_game(score):
    """Function that appears once you've lost

    Args:
        score (int): length of the snake, which represents your score

    Returns:
        walls (boolean): only if the player has decided to play again, returns the walls variable, which
        represents the user choice of the walls or not 
    """
    # Print the score you have achieved
    print('Score: ', score)

    # Create a new window in which the player can choose to play again
    root = tk.Tk()
    # Make sure that the window appears on top
    root.attributes('-topmost', True)
    root.withdraw()
    # Appear the message box which asks a question
    MsgBox = messagebox.askquestion ('You lost...','Play again?')
    if MsgBox == 'yes':
        # If you want to play again, destroy the window which tells you you've lost, and reset
        # the game.
        root.destroy()
        walls = s.reset((10,10))
        return walls
    else:
        # If you don't want to play again (coward), exit python
        exit()

def message_box_levels(subject):
    """Function for the beginning of the game which lets you choose the levels of the game.
    For now, you can only choose whether you want walls or not on the game.

    Args:
        subject (string): message seen by the player

    Returns:
        walls (boolean): returns the walls variable, which represents the user choice of the 
        walls active or not
    """

    # Create a window in which the player can choose the game options
    root = tk.Tk()
    #Make sure that the window appears on top
    root.attributes('-topmost', True)

    def callback():
        """Function which activates when the player clicks the "let's play" button
        It destroys the window of the levels so that the pygame window can appear
        """
        root.destroy()

    # Display a message for the player
    w = tk.Message(root, text=subject)
    w.pack()

    walls = tk.IntVar() #Initiallize the integer variable "walls"
    # The choose of the checkbutton by the player decides the value of the variable walls:
    # walls = 0 if the box is unchecked, while walls = 1 if the box is checked.
    c = tk.Checkbutton(root, text="Walls limit", variable = walls)
    c.pack()

    # Button for the starting of the game. Once clicked it destroys the window of the levels
    b = tk.Button(root, text="Let's play", command=callback)
    b.pack()

    # Start the window so that everything is displayed
    root.mainloop()
    
    return walls.get()

def main():
    """Main function which relates the rest of functions and classes
    """
    # Make global all the following self-explanatory variables (s = snake)
    global width, rows, s, snack, walls

    # Display the window which lets the user choose the walls 
    walls = message_box_levels('Welcome to the snake!')

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
                #Display the message for resetting the game
                walls = lost_game(len(s.body))
                break

        # If the walls are active, you can also lose by hitting them (something not very intelligent either)
        if s.walls_hit == 1:
            walls = lost_game(len(s.body))
        
        # every frame (or however you call it) redraw the window
        redrawWindow(win)

    pass

# Run the main function
main()