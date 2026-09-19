"""
Implementing Gravity

This program will demonstrate a simple implementation of gravity in a game, 
the the player constantly jumping. Notice that using gravity makes the player
jump more realistic. The player goes up quickly, but falls slowly. 

"""
import pygame
from dataclasses import dataclass

# Initialize Pygame
pygame.init()


# This is a data class, one way of storing settings and constants for a game.
# We will create an instance of the data class, but since there is only one of
# them, we could also use the class directly, like GameSettings.screen_width.
# You can check that the instance has the same values as the class:
#    settings = GameSettings()
#    assert GameSettings.screen_width == settings.screen_width
@dataclass
class GameSettings:
    """Class for keeping track of game settings."""
    screen_width: int = 500
    screen_height: int = 500
    player_size: int = 10
    player_x: int = 100 # Initial x position of the player
    gravity: float = 0.3 # acelleration, the change in velocity per frame
    jump_velocity: int = 15
    white: tuple = (255, 255, 255)
    black: tuple = (0, 0, 0)
    tick_rate: int = 30 # Frames per second

# Initialize game settings
settings = GameSettings()



# Initialize screen
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))

# Define player
player = pygame.Rect(settings.player_x, 
                     settings.screen_height - settings.player_size, 
                     settings.player_size, settings.player_size)

player_y_velocity = 0
is_jumping = False

# Main game loop
running = True
clock = pygame.time.Clock()

while running:

    # Handle events, such as quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    # Continuously jump. If the player is not jumping, initialize a new jump
    if keys[pygame.K_SPACE] and player.bottom >= settings.screen_height:
        # Jumping means that the player is going up. The top of the 
        # screen is y=0, and the bottom is y=SCREEN_HEIGHT. So, to go up,
        # we need to have a negative y velocity
        player_y_velocity = -settings.jump_velocity
        is_jumping = True

    # Update player position. Gravity is always pulling the player down,
    # which is the positive y direction, so we add GRAVITY to the y velocity
    # to make the player go up more slowly. Eventually, the player will have
    # a positive y velocity, and gravity will pull the player down.
    player_y_velocity += settings.gravity
    player.y += player_y_velocity

    # If the player hits the ground, stop the player from falling.
    # The player's position is measured from the top left corner, so the
    # bottom of the player is player.y + PLAYER_SIZE. If the bottom of the
    # player is greater than the height of the screen, the player is on the
    # ground. So, set the player's y position to the bottom of the screen
    # and stop the player from falling
    if player.bottom >= settings.screen_height:
        player.bottom = settings.screen_height 
        player_y_velocity = 0
        is_jumping = False

    # Draw everything
    screen.fill(settings.white)
    pygame.draw.rect(screen, settings.black, player)

    pygame.display.flip()
    clock.tick(settings.tick_rate)

pygame.quit()
