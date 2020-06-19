# Import packages
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

class cube(object):
    """This class creates and manages the cubes. 
    They represent the snack and the snake, since aesthetically this game is not so nice (yet)
    """
    rows = 20
    width = 500
    def __init__(self, start, dirnx = 1, dirny = 0, color = (120,153,0)):
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

    def draw_snake(self, surface, eyes = False, tail = False):
        """Function that draws the snake as octahedra, except for the tail, which is a triangle.

        Args:
            surface (window?): window in which the cube will be displayed
            eyes (bool, optional): Whether the eyes of the snake are drawn or not. 
            Defaults to False because the snake only has eyes on the head (xD)
            tail (bool, optional): The tail of the snake is a triangle instead of an octahedra
        """
        dis = self.width // self.rows
        i = self.pos[0] #row
        j = self.pos[1] #column

        # Define the distances needed for drawing the octahedra
        x_m = i*dis; y_m = j*dis; x_M = x_m + dis-2; y_M = y_m + dis-2
        x_med = int((x_m+x_M)/2); y_med = int((y_m+y_M)/2)
        mar = 5

        if tail:
            # Draw the triangle of the tail depending on the direction in which it moves
            if self.dirnx == -1 and self.dirny == 0:
                pygame.draw.polygon(surface, self.color, [(x_m, y_m+mar), (x_M, y_med), (x_m, y_M-mar)])
            elif self.dirnx == 1 and self.dirny == 0:
                pygame.draw.polygon(surface, self.color, [(x_M, y_m+mar), (x_m, y_med), (x_M, y_M-mar)])
            elif self.dirnx == 0 and self.dirny == -1:
                pygame.draw.polygon(surface, self.color, [(x_m+mar, y_m), (x_med, y_M), (x_M-mar, y_m)])
            elif self.dirnx == 0 and self.dirny == 1:
                pygame.draw.polygon(surface, self.color, [(x_m+mar, y_M), (x_med, y_m), (x_M-mar, y_M)])
        else:
            # If you're not drawing the tail, draw the octahedra that represents the snake's body
            pygame.draw.polygon(surface, self.color, [(x_m+mar, y_m), (x_M-mar, y_m), (x_M, y_m+mar), \
                (x_M, y_M-mar), (x_M-mar, y_M), (x_m+mar, y_M), (x_m, y_M-mar), (x_m, y_m+mar)])

        # We don't want the snake blind, so we better draw some eyes on the head cube
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis+dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

    def draw_apple(self, surface, rotten = False, poisoned = False):
        """Function that draws the apple and its root

        Args:
            surface (window?): window in which the cube will be displayed
            rotten (bool, optional): Rotten apples have a grey color. Defaults to False.
            poisoned (bool, optional): poisoned apples have a purple color. Defaults to False.
        """
        dis = self.width // self.rows #width of each square of the grid
        i = self.pos[0] #row
        j = self.pos[1] #column
        
        # Set the color of the apple depending on whether it's rotten, poisoned or tasty
        if rotten:
            color = (100,100,100)
        elif poisoned:
            color = (204,0,204)
        else:
            color = (255,0,0)

        # Define useful distances for the drawing
        x_m = i*dis; y_m = j*dis; x_M = x_m + dis; y_M = y_m + dis; x_med = int((x_M+x_m)/2)
        a = 5; b = 3; c = 4; d = 5
        # Draw the apple
        pygame.draw.polygon(surface, color, [(x_M-a, y_M), (x_med,y_M-b), (x_m+a, y_M), \
            (x_m,y_m+c), (x_m+c,y_m), (x_med,y_m+d), (x_M-c,y_m), (x_M,y_m+c)])

        # Draw the root of the apple
        e = 2; f = c
        pygame.draw.polygon(surface, (0,255,0), [(x_med-e,y_m-d), (x_med+e,y_m+d), (x_med,y_m+f)])

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
        """Function for resetting the snake after the player has lost

        Args:
            pos (array (x,y)): original position of the snake

        Returns:
            walls: variable which tells you whether the player has decided to turn on the walls or not
            rot_apple_on: variable which tells you whether the player wants to play with rotten apples
            pois_apple_on: variable which tells you whether the player wants to play with poisoned apples
        """
        walls, rot_apple_on, pois_apple_on = message_box_levels('Welcome to the snake!')
        # The next commands initialize the snake performing almost the same as the __init__ function
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        self.walls_hit = 0
        return walls, rot_apple_on, pois_apple_on

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

    def removeCube(self):
        """When the snake eats a rotten apple, its length is reduced by one,
        removing the last cube of its body
        """
        tail = self.body[-1]
        self.body.remove(tail)

    def draw_snake(self, surface):
        """Draw the snake so that the player knows what is going on

        Args:
            surface (window?): window in which the snake will be displayed
        """
        # Draw all the octahedra which represent the snake
        for i, c in enumerate(self.body):
            if i ==0:
                #Only to add this to draw the eyes of the snake
                c.draw_snake(surface, True)
            elif i == len(self.body)-1 and len(self.body) > 1:
                # Draw the tail of the snake if it's not only the head
                c.draw_snake(surface, tail = True)
            else:
                c.draw_snake(surface)
        
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
    x = 0; y = 0
    color_lines = (255, 255, 255) # White
    for l in range(rows):
        x += size_between # Every iteration add the size of the square in order to plot the next line
        y += size_between

        # Draw the white lines which divide the grid
        pygame.draw.line(surface, color_lines, (x, 0), (x, width))
        pygame.draw.line(surface, color_lines, (0, y), (width, y))
    
    # If the walls are active, surround the grid by brown lines so that the player is aware of them
    if walls == 1:
        color_walls = (204,102,0); width_walls = 7
        pygame.draw.line(surface, color_walls, (0, 0), (0, width),width_walls)
        pygame.draw.line(surface, color_walls, (x, 0), (x, width),width_walls)
        pygame.draw.line(surface, color_walls, (0, 0), (width, 0),width_walls)
        pygame.draw.line(surface, color_walls, (0, y), (width, y),width_walls)

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
    global rows, width, s, snack, rot_apple
    color_surface = (0, 0, 0) #Black
    surface.fill(color_surface) #Black background
    s.draw_snake(surface) #Plot the snake
    snack.draw_apple(surface) #Plot the apple
    # If the player has decided to play with rotten apples, they appear if the 
    # snake is more than only the head
    if len(s.body) > 1 and rot_apple_on == 1:
        rot_apple.draw_apple(surface,True)
    # If the player has decided to play with poisoned apples
    if pois_apple_on == 1:
        pois_apple.draw_apple(surface,poisoned = True)
    drawGrid(width, rows, surface) #Plot the white lines of the grid and the walls if apply
    pygame.display.update() #Update the changes done on the window

    pass

def randomSnack(rows, item, item_list):
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

        # Make sure we don't put apples on top of another apple
        for it in range(len(item_list)):
            print(item_list[it].pos)
            if x == item_list[it].pos[0] and y == item_list[it].pos[0]:
                break

    return (x,y)

def lost_game(score):
    """Function that appears once you've lost

    Args:
        score (int): length of the snake, which represents your score

    Returns:
        walls (boolean): if the player has decided to play again, returns the walls variable, which
        represents the user choice of the walls or not 
        rot_apple_on (boolean): if the player has decided to play again, returns its choice regading
        the appearance of rotten apples
        pois_apple_on (boolean): if the player has decided to play again, returns its choice regading
        the appearance of poisoned apples 
    """
    # Print the score you have achieved
    print('Score: ', score)

    # Create a new window in which the player can choose to play again
    root = tk.Tk()
    # Make sure that the window appears on top
    root.attributes('-topmost', True)
    root.withdraw()
    # Appear the message box which asks a question and displays the score
    content = 'You lost. Your score was ' + str(score)
    MsgBox = messagebox.askquestion (content,'Play again?')
    if MsgBox == 'yes':
        # If you want to play again, destroy the window which tells you you've lost, and reset
        # the game.
        root.destroy()
        walls, rot_apple_on, pois_apple_on = s.reset((10,10))
        return walls, rot_apple_on, pois_apple_on
    else:
        # If you don't want to play again (coward), exit python
        exit()

def message_box_levels(subject):
    """Function for the beginning of the game which lets you choose the game options.

    Args:
        subject (string): message seen by the player

    Returns:
        walls (boolean): represents the player choice of the walls active or not
        rot_apple_on (boolean): represents the player choice of the appearance of rotten apples
        pois_apple_on (boolean): represents the player choice of the appearance of poisoned apples
    """

    # Create a window in which the player can choose the game options
    root = tk.Tk()
    #Make sure that the window appears on top
    root.attributes('-topmost', True)

    # Export and display snake image for the making the game more aestheticall
    im = Image.open("0_snake.png")
    im=im.resize((200,200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image = im)
    panel = tk.Label(root, image = img)
    panel.pack(side = "left")

    def callback():
        """Function which activates when the player clicks the "let's play" button
        It destroys the window of the levels so that the pygame window can appear
        """
        root.destroy()

    # Display a message for the player
    w = tk.Message(root, text=subject)
    w.pack()

    walls = tk.IntVar() #Initiallize the boolean variable "walls"
    # The choice of the checkbutton by the player decides the value of the variable walls:
    # walls = 0 if the box is unchecked, while walls = 1 if the box is checked.
    c = tk.Checkbutton(root, text="Walls limit", variable = walls)
    c.pack()

    # Same checkbutton as before for activating the rotten apples
    rot_apple_on = tk.IntVar()
    d = tk.Checkbutton(root, text="Rotten apples", variable = rot_apple_on)
    d.pack()

    # Same checkbutton as before for activating the poisoned apples
    pois_apple_on = tk.IntVar()
    d = tk.Checkbutton(root, text="Poisoned apples", variable = pois_apple_on)
    d.pack()

    # Button for the starting of the game. Once clicked it destroys the window of the levels
    b = tk.Button(root, text="Let's play!", command=callback)
    b.pack()

    # Start the window so that everything is displayed
    root.mainloop()
    
    return walls.get(), rot_apple_on.get(), pois_apple_on.get()

def main():
    """Main function which relates the rest of functions and classes
    """
    # Make global all the following self-explanatory variables (s = snake)
    global width, rows, s, snack, rot_apple, walls, rot_apple_on, pois_apple, pois_apple_on

    # Display the window which lets the user choose the game options 
    walls, rot_apple_on, pois_apple_on = message_box_levels('Welcome to the snake!')

    # Width of the pygame window
    width = 500
    # Rows needs to divide evenly by width
    rows = 20
    # Create the square pygame window of size width
    win = pygame.display.set_mode((width, width))
    # Determine the initial position of the snake in the middle of the window
    position = (int(rows/2), int(rows/2))
    color = (120,153,0) # color of the snake
    s = snake(color, position) #Initialize the snake
    snack = cube(randomSnack(rows, s, []), color = (255,0, 0)) #Initialize the snack
    rot_apple = cube(randomSnack(rows, s, [snack]), color = (100,100,100)) #Initialize the rotten apple
    pois_apple = cube(randomSnack(rows, s, [snack, rot_apple]), color = (204,0,204)) #Initialize the poisoned apple
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
            snack = cube(randomSnack(rows, s, [rot_apple, pois_apple]), color = (255, 0, 0))
        
        # If the snake eats a rotten apple, and the player has decided to play with rotten apples
        # the length of the snake is reduced by one
        if s.body[0].pos == rot_apple.pos and rot_apple_on == 1:
            s.removeCube()
            rot_apple = cube(randomSnack(rows, s, [snack, pois_apple]), color = (100,100,100))
        
        # If the snake eats a poisoned apple, and the player has decided to play with poisoned apples
        # you lost the game
        if s.body[0].pos == pois_apple.pos and pois_apple_on == 1:
            walls, rot_apple_on, pois_apple_on = lost_game(len(s.body))
        
        # If the snake eats itself (not something very intelligent to do), you lose
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                #Display the message for resetting the game
                walls, rot_apple_on, pois_apple_on = lost_game(len(s.body))
                break

        # If the walls are active, you can also lose by hitting them (something not very intelligent either)
        if s.walls_hit == 1:
            walls, rot_apple_on, pois_apple_on = lost_game(len(s.body))
        
        # every frame (or however you call it) redraw the window
        redrawWindow(win)

    pass

# Run the main function
main()