""" Version 1.2 Ultimate Brick
Anderson Ang Wei Jian and Qingyun Liu

Uses trivial graphical tiles to create a game environment -
the objective is to spawn an environment with tiles and sprites using non-trivial
code (without interaction elements)

Changelog: (Total hours: 32 hours minimum, 40 hours maximum)

- Version 1.0 (base game) (complete)
Includes:
    - Basic sprite formation (ball, player bar, blocks)
    - Level randomization (block position, color)
    - Ball spawn randomization (position)

- Version 1.1 (estimated 13 hours) (complete)
Includes:
    - Sound support (bgm, interactive)
    - Controller interaction (keyboard input)
    - Collision physics
        - Bar + Ball physics
        - Ball + Block physics
    - Screen edge detection
        - Ball + edge physics
    - Sprite motion (ball & bar)
    - Add game_over flash screen

- Version 1.2 (est. 6 hours) (complete)
    - Multi-face playablility
        - Bar + edge physics
    - Reform code grid into MVC format

- Version 2.0 (est. 4 hours)
    - In-game restart capability
    - Addition of flash screen for instructions

- Version 2.1 (est. 9 hours)
    - Support 2P generation (multiplayer) - done -
    - Develop competitive elements (inter-player sprite interaction) - done -

-------------- M.V.P (Minimum Viable) : Part III ---------

- Stretch goal: Version 3.0 (est. 4 + 4 hours) - cancelled -
    - Voice-based control
    - Multiple game modes (Time attack, Classic, Point Rush)

------------ Game complete! -------------------------

"""

# Libraries
import math
import pygame
import random

# Colors (for bar and ball only)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255,0,0)
blue = (0,0,255)


# Block sizes
block_width = 23
block_height = 15

# Number of players
playercount = 2


class Block(pygame.sprite.Sprite):
    """This class represents each block that will get knocked out by the ball
    It derives from the "Sprite" class in Pygame """

    def __init__(self, color, x, y):
        """ Constructor. Passes in the color of the block,
            and its x and y position. """

        # Call the parent class (Sprite) constructor
        super(Block,self).__init__()

        # Create the image of the block of appropriate size
        # The width and height are sent as a list for the first parameter.
        self.image = pygame.Surface([block_width, block_height])

        # Fill the image with the appropriate color
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Move the top left of the rectangle to x,y.
        # This is where our block will appear..
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    """ This class represents the ball
        It derives from the "Sprite" class in Pygame """

    # Speed in pixels per cycle
    speed = 10.0

    # Floating point representation of where the ball spawns
    # Alternates between spawning from left/right of screen
    x = float(random.randrange(0,801,799))
    # Varies between the top 1/3rd to the lower 1/3rd of the screen height
    y = float(random.randint(120, 280))

    # Initial direction of ball (in degrees)
    direction = 150

    width = 10
    height = 10

    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Ball, self).__init__()

        # Create the image of the ball
        self.image = pygame.Surface([self.width, self.height])

        # Color the ball
        self.image.fill(white)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    def bounce(self, diff):
        """ This function will bounce the ball
            off surfaces (Controller-model interface 2) """

        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self):
        """ Update the position of the ball. (Controller-Model interface) """
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y

        # Do we bounce off the top of the screen?
        if self.y <= 0:
            self.bounce(0)
            self.y = 1

        # Do we bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1

        # Do we bounce of the right side of the screen?
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1

        # Did we fall off the bottom edge of the screen?
        if self.y > 600:
            return True
        else:
            return False


class Player(pygame.sprite.Sprite):
    """ This class represents the bar(s) that the
    player(s) controls. """

    def __init__(self,color,x,y):
        """ View Constructor for player creation. Passes in color of bar, x and y location """
        # Call the parent's constructor
        super(Player, self).__init__()

        self.width = 75
        self.height = 15

        # Create and claims surface geometry and color
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((color))

        # Make the rect from the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.x = x
        self.rect.y = self.screenheight-y


    def update(self, xdiff):
        """ Acts as the controller-model interface for the player's bar """
        # Set the left side of the player bar according to player input
        self.rect.x += xdiff
        # Make sure we don't push the player paddle off the right side of the screen
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

# Set the title of the window
pygame.display.set_caption('Ultimate Brick')

# Enable this to make the mouse disappear when over our window
pygame.mouse.set_visible(0)

# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Create sprite lists
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
players = pygame.sprite.Group()
allsprites = pygame.sprite.Group()

# Create the player paddle objects
if playercount == 2:
    player = Player(red, 0, 15)
    player2 = Player(blue, (800-75), 600)
    players.add(player)
    players.add(player2)
    allsprites.add(player)
    allsprites.add(player2)
else:
    player = Player(white,0,15)
    players.add(player)
    allsprites.add(player)

# Positional start points for Player bars
x_position=0
xx_position=780

y_position=580
yy_position=600

x_move = 0
x2_move = 0
x2_position=650

y2_position=0
xx2_position=0
yy2_position=-150

# Create the ball
ball = Ball()
allsprites.add(ball)
balls.add(ball)

# The top of the block (y position)
top = 160

# Number of blocks to create
blockcount = 28
# Number of rows to create
rowcount = random.randint(2,8)

## Create blocks

# Range controls the number of rows
for row in range(rowcount):
    # 28 columns with a max diff of 28-8-4 = 16
    for column in range(random.randint(2,8), blockcount - random.randint(0,4)):
        # Create a block (color,x,y)
        # randint starts at 80 to create brighter hues
        rainbow = (random.randint(100,255), random.randint(90,255), random.randint(90,250))
        block = Block(rainbow, column * (block_width + 2 ) + 1, top)
        blocks.add(block)
        allsprites.add(block)
    # Starts at the next row
    top += block_height + 2

# Clock to limit speed
clock = pygame.time.Clock()

# Is the game over?
game_over = False

# Exit the program?
exit_program = False

# Plays the BGM on launch
pygame.mixer.music.load("BGM2.mp3")
pygame.mixer.music.play(-1)

# Main program loop
while not exit_program:

    # Limit to 30 fps
    clock.tick(30)

    # Clear the screen
    screen.fill(black)

    # Process the events in the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_move = -10
            if event.key == pygame.K_RIGHT:
                x_move = 10
            if event.key == pygame.K_q:
                x2_move = -10
            if event.key == pygame.K_e:
                x2_move = 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                x_move = 0
            if event.key == pygame.K_RIGHT:
                x_move = 0
            if event.key == pygame.K_q:
                x2_move = 0
            if event.key == pygame.K_e:
                x2_move = 0
        x_position += x_move
        x2_position += x2_move

    # Controller portion: update positions as it goes
    if not game_over:
        # Update the player and ball positions
        player.update(x_move)
        player2.update(x2_move)
        game_over = ball.update()

    # Print game over if the ball hits any corner
    if game_over:
        text = font.render("Game Over", True, white)
        textpos = text.get_rect(centerx=background.get_width()/2)
        textpos.top = 300
        screen.blit(text, textpos)


    # See if the ball hits the player 1's paddle
    if pygame.sprite.spritecollide(player, balls, False):
        # The 'diff' lets you try to bounce the ball left or right
        # depending where on the paddle you hit it
        diff = (player.rect.x + player.width/2) - (ball.rect.x+ball.width/2)

        # Set the ball's y position in case
        # we hit the ball on the edge of the paddle
        ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
        ball.bounce(diff)

    if pygame.sprite.spritecollide(player2, balls, False):
        # The 'diff' lets you try to bounce the ball left or right
        # depending where on the paddle you hit it
        diff2 = (player2.rect.x + player2.width/2) - (ball.rect.x+ball.width/2)

        # Set the ball's y position in case
        # we hit the ball on the edge of the paddle
        ball.rect.y = screen.get_height() - player2.rect.height - ball.rect.height - 1
        ball.bounce(diff2)

    # Check for collisions between the ball and the blocks
    deadblocks = pygame.sprite.spritecollide(ball, blocks, True)

    # If we actually hit a block, bounce the ball
    if len(deadblocks) > 0:
        ball.bounce(0)

        # Game ends if all the blocks are gone
        if len(blocks) == 0:
            game_over = True

    # Draw Everything
    allsprites.draw(screen)

    # Flip the screen and show what we've drawn
    pygame.display.flip()

pygame.quit()
