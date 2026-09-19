import pygame
import math

# Initialize Pygame
pygame.init()

# Settings class
class Settings:
    """A class to store all settings for the game."""
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    PLAYER_SIZE = 20
    LINE_COLOR = (0, 255, 0)
    PLAYER_COLOR = (0, 0, 255)
    BACKGROUND_COLOR = (255, 255, 255)
    TEXT_COLOR = (0, 0, 0)
    FPS = 30
    ANGLE_CHANGE = 3
    LENGTH_CHANGE = 5
    INITIAL_LENGTH = 100
    FONT_SIZE = 24

# Initialize screen
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("Player with Direction Vector")

# Clock to control frame rate
clock = pygame.time.Clock()

# Font for displaying vector information
font = pygame.font.Font(None, Settings.FONT_SIZE)

# Player class
class Player:
    def __init__(self, x, y):
        """Initializes the Player with a position and direction vector.

        Args:
            x (int): The initial x-coordinate of the player.
            y (int): The initial y-coordinate of the player.
        """
        self.position = pygame.math.Vector2(x, y)
        self.direction_vector = pygame.math.Vector2(Settings.INITIAL_LENGTH, 0)  # Initial direction vector

    def draw(self, show_line=True):
        """Draws the player and the direction vector on the screen."""
        pygame.draw.rect(screen, Settings.PLAYER_COLOR, (self.position.x - Settings.PLAYER_SIZE // 2, self.position.y - Settings.PLAYER_SIZE // 2, Settings.PLAYER_SIZE, Settings.PLAYER_SIZE))
        
        # The end position of the direction vector is the player's position plus the direction vector
        end_position = self.position + self.direction_vector
        
        if show_line:
            pygame.draw.line(screen, Settings.LINE_COLOR, self.position, end_position, 2)

    def move(self):
        """Moves the player in the direction of the current angle."""
        
        
        init_position = self.position # Save the initial position for the animation
        
        # Calculate the final position after moving. Its just addition!
        final_position = self.position + self.direction_vector
        
        # The rest is just for animation
        length = self.direction_vector.length()
        N = int(length // 3)
        step = (final_position - self.position) / N
       
        for i in range(N):
            self.position += step
            screen.fill(Settings.BACKGROUND_COLOR)
            self.draw(show_line=False)
            pygame.draw.line(screen, Settings.LINE_COLOR, init_position, final_position, 2)
            pygame.display.flip()
            clock.tick(Settings.FPS)

def draw_vector_info(player):
    """Draws the vector information at the bottom of the screen."""
    direction_x, direction_y = player.direction_vector.x, player.direction_vector.y
    magnitude = player.direction_vector.length()
    angle = player.direction_vector.angle_to(pygame.math.Vector2(1, 0))  # Angle with respect to the x-axis

    # Prepare the text to display
    vector_text = f"Vector: ({direction_x:.2f}, {direction_y:.2f})"
    magnitude_text = f"Magnitude: {magnitude:.2f}"
    angle_text = f"Angle: {angle:.2f}°"

    # Render the text
    vector_surface = font.render(vector_text, True, Settings.TEXT_COLOR)
    magnitude_surface = font.render(magnitude_text, True, Settings.TEXT_COLOR)
    angle_surface = font.render(angle_text, True, Settings.TEXT_COLOR)

    # Display the text at the bottom of the screen
    screen.blit(vector_surface, (10, Settings.SCREEN_HEIGHT - 70))
    screen.blit(magnitude_surface, (10, Settings.SCREEN_HEIGHT - 45))
    screen.blit(angle_surface, (10, Settings.SCREEN_HEIGHT - 20))

def main():
    player = Player(Settings.SCREEN_WIDTH // 2, Settings.SCREEN_HEIGHT // 2)
    running = True
    
    pygame.key.set_repeat(50, 50)
    
    key_limit = 0
    while running: 
        key_limit += 1
        
        screen.fill(Settings.BACKGROUND_COLOR)
        
        keys = pygame.key.get_pressed()
        
        if key_limit%3 == 0: # Limit frequency of key presses so the user can set exact angles
            if keys[pygame.K_LEFT]:
                player.direction_vector = player.direction_vector.rotate(-Settings.ANGLE_CHANGE)
            elif keys[pygame.K_RIGHT]:
                player.direction_vector = player.direction_vector.rotate(Settings.ANGLE_CHANGE)
                
        if keys[pygame.K_UP]:
            player.direction_vector.scale_to_length(player.direction_vector.length() + Settings.LENGTH_CHANGE)
        elif keys[pygame.K_DOWN]:
            player.direction_vector.scale_to_length(player.direction_vector.length() - Settings.LENGTH_CHANGE)
        elif keys[pygame.K_SPACE]:
            player.move()
                

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Draw the player and the direction vector
        player.draw()

        # Draw the vector information at the bottom of the screen
        draw_vector_info(player)

        pygame.display.flip()
        clock.tick(Settings.FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
