"""

Moving Square

All this game does is move a square around the screen using the arrow keys.
The square is constrained to the screen, so it can't go off the edges. 

"""
import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
SQUARE_SIZE = 50
SQUARE_COLOR = (0, 128, 255) # Red-Green-Blue color in the range 0-255
BACKGROUND_COLOR = (255, 255, 255) # White
SQUARE_SPEED = 5
FPS = 60

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Move the Square")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Main function
def main():
    # Initial position of the square
    square_x = SCREEN_WIDTH // 2 - SQUARE_SIZE // 2
    square_y = SCREEN_HEIGHT // 2 - SQUARE_SIZE // 2
    
    running = True
    
    while running:
        

        # Event handling
        for event in pygame.event.get():
            
            # Check for clicking the close button
            if event.type == pygame.QUIT:
                running = False
        
        # Get the keys pressed. Gtes an array of all the keys
        # with a boolean value of whether they are pressed or not
        keys = pygame.key.get_pressed()

        # Move the square based on arrow keys
        if keys[pygame.K_a]:
            square_x -= SQUARE_SPEED
        if keys[pygame.K_d]:
            square_x += SQUARE_SPEED
        if keys[pygame.K_w]:
            square_y -= SQUARE_SPEED
        if keys[pygame.K_s]:
            square_y += SQUARE_SPEED

        # Prevent the square from going off the screen
        square_x = max(0, min(SCREEN_WIDTH - SQUARE_SIZE, square_x))
        square_y = max(0, min(SCREEN_HEIGHT - SQUARE_SIZE, square_y))

        # This will clear the screen by filling it 
        # with the background color. If we didn't do this, 
        # the square would leave a trail behind it.
        screen.fill(BACKGROUND_COLOR)

        # Draw the square
        pygame.draw.rect(screen, SQUARE_COLOR, (square_x, square_y, SQUARE_SIZE, SQUARE_SIZE))

        # Update the display. Imagine that the screen is two different whiteboards. One
        # whiteboard is currently visible to the player, and the other whiteboard is being
        # drawn on. When you call pygame.display.flip(), it's like taking the whiteboard
        # that was being drawn on and showing it to the player, while taking the whiteboard
        # that was visible to the player and giving it to the artist to draw on. This makes
        # it so that the player never sees the drawing process, only the final result.
        pygame.display.flip()

        # Cap the frame rate. This makes the game run at a consistent speed on all computers.
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
