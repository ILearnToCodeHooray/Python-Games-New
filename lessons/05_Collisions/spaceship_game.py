"""
Dino Jump

Use the arrow keys to move the blue square up and down to avoid the black
obstacles. The game should end when the player collides with an obstacle ...
but it does not. It's a work in progress, and you'll have to finish it. 

"""
import pygame
import random
from pathlib import Path

# Initialize Pygame
pygame.init()

images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"

# Screen dimensions
class Settings:
        width = 600
        height = 300
        screen = pygame.display.set_mode((width, 600))
        pygame.display.set_caption("Dino Jump")

        # Colors
        colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'blue': (0, 0, 255),
            'red': (255, 0, 0)
        }

        # FPS
        fps = 60

        # Player attributes
        size = 50

        speed = 5

        # Obstacle attributes
        obstacle_width= 20
        obstacle_height = 20
        obstacle_speed = 5
        obstacle_x = 0

        # Font
        font = pygame.font.SysFont(None, 36)
        score = 0


# Define an obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        cactus_image = pygame.image.load(images_dir / "asteroid1.png").convert_alpha()
        self.image = pygame.transform.scale(cactus_image, (self.settings.obstacle_width, self.settings.obstacle_height))
        self.original_image = pygame.transform.scale(cactus_image, (self.settings.obstacle_width, self.settings.obstacle_height))
        self.rect = self.image.get_rect()
        self.rect.x = Settings.width
        Settings.obstacle_x = Settings.width
        self.rect.y = Settings.height - random.randint(40, 400)
        self.scored = False
        self.explosion = pygame.image.load(images_dir / "explosion1.gif")
        self.alive = True
        self.collided = False
        self.angle = 0.0
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self):
        self.x = self.x + random.randint(-10, 5)
        Settings.obstacle_x = Settings.obstacle_x +random.randint(-10, 5)
        self.y = self.y + random.randint(-5, 5)
        # Remove the obstacle if it goes off screen
        self.angle += 5
        if self.angle >= 360:
            self.angle = 0

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.original_image.get_rect(center = (self.x+10, self.y+10)) 
        if self.x < 0:
            self.kill()

    def explode(self):
        """Replace the image with an explosition image."""
        
        # Load the explosion image
        self.image = self.explosion
        self.image = pygame.transform.scale(self.image, (Settings.obstacle_width, Settings.obstacle_height))
        self.rect = self.image.get_rect(center=self.rect.center)

class Player(pygame.sprite.Sprite):
    def __init__(self, Settings):
        super().__init__()
        dino_image = pygame.image.load(images_dir / "alien2.gif").convert_alpha()
        self.image = pygame.transform.scale(dino_image, (Settings.size, Settings.size))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = Settings.height - Settings.size - 10

        # Jump variables
        self.velocity = 0
        self.gravity = 1
        self.jump_strength = -15
        self.is_jumping = False

    def update(self):
        # Apply gravity
        self.velocity += self.gravity
        self.rect.y += self.velocity

        # Prevent falling below ground
        if self.rect.bottom >= Settings.height:
            self.rect.bottom = Settings.height
            self.velocity = 0
            self.is_jumping = False



# Create a player object
player = Player(Settings)
player_group = pygame.sprite.Group(player)

# Add obstacles periodically
def add_obstacle(obstacles):
    # random.random() returns a random float between 0 and 1, so a value
    # of 0.25 means that there is a 25% chance of adding an obstacle. Since
    # add_obstacle() is called every 100ms, this means that on average, an
    # obstacle will be added every 400ms.
    # The combination of the randomness and the time allows for random
    # obstacles, but not too close together. 
    
    if random.random() < 0.4:
        obstacle = Obstacle(Settings)
        obstacles.add(obstacle)
        return 1
    return 0

class Game_Over(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        gm_ovr_img = pygame.image.load(images_dir / "game_over_screen.png").convert_alpha()
        self.image = pygame.transform.scale(gm_ovr_img, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

game_over_screen = Game_Over()
game_over_group = pygame.sprite.Group(game_over_screen)
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.laser_x = x
        self.laser_y = y
        self.width = 20
        self.height = 10
        self.speed = 10
        self.color = Settings.colors['red']
        self.rect = pygame.Rect(self.laser_x, self.laser_y, self.width, self.height)

    def update(self):
        self.laser_x += self.speed
        self.rect.x = self.laser_x
        if self.laser_x > Settings.width:
            self.kill()  # Remove from group when off screen

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# Main game
# loop
class Loop():
    def __init__(self):
        self.game_over = False
        self.high_score = 0
        self.shooting = False
        self.game_loop(Settings)
        
    def game_loop(self, Settings):
        clock = pygame.time.Clock()
        last_obstacle_time = pygame.time.get_ticks()
        
        self.lasers = pygame.sprite.Group()
        # Group for obstacles
        obstacles = pygame.sprite.Group()

        obstacle_count = 0

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.velocity = player.jump_strength
                        player.is_jumping = True
                    if event.key == pygame.K_l:
                        laser = Laser(player.rect.right, player.rect.y + Settings.size // 2)
                        self.lasers.add(laser)
                        self.shooting = True

                        


            # Update player
            player.update()
            

            # Add obstacles and update
            if pygame.time.get_ticks() - last_obstacle_time > 500:
                last_obstacle_time = pygame.time.get_ticks()
                obstacle_count += add_obstacle(obstacles)
            obstacles.update()
            self.lasers.update()
            # Check for collisions
            
            for obstacle in obstacles:
                if not obstacle.scored and not obstacle.collided and obstacle.rect.right < player.rect.left:
                    Settings.score += 1
                    obstacle.scored = True
                   

            
            collider = pygame.sprite.spritecollide(player, obstacles, dokill=False)
            for obstacle in collider:
                if not obstacle.collided:
                    obstacle.collided = True
                    obstacle.explode()
                    self.game_over = True
                    if Settings.score > self.high_score:
                        self.high_score = Settings.score
            laser_collider = pygame.sprite.groupcollide(obstacles, self.lasers, dokilla=True, dokillb=True)
            for obstacle in laser_collider:
                if laser_collider:
                    Settings.score = Settings.score + 1
                    
                    
            # Draw everything
            Settings.screen.fill(Settings.colors['white'])
            player_group.draw(Settings.screen)
            obstacles.draw(Settings.screen)
            pygame.draw.rect(Settings.screen, Settings.colors['blue'], (0, 300, 1000, 500))
            
            for laser in self.lasers:
                pygame.draw.rect(Settings.screen, Settings.colors['red'], (laser.laser_x, laser.laser_y, 20, 10))


            # Display obstacle count
            obstacle_text = Settings.font.render(f"Obstacles: {obstacle_count}", True, Settings.colors['black'])
            Settings.screen.blit(obstacle_text, (10, 10))

            score_text = Settings.font.render(f"Score: {Settings.score}", True, Settings.colors['black'])
            Settings.screen.blit(score_text, (300, 10))
            pygame.display.update()
            clock.tick(Settings.fps)

        else:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        # Reset game state
                        Settings.score = 0
                        player.rect.y = Settings.height - Settings.size - 10
                        player.velocity = 0
                        player.is_jumping = False
                        self.game_over = False
                        self.game_loop(Settings)
                        return  # Exit this restart loop when game restarts

                Settings.screen.fill(Settings.colors['white'])
                game_over_group.draw(Settings.screen)

                # Draw the final score and high score here
                score_text = Settings.font.render(f"Score: {Settings.score}", True, Settings.colors['black'])
                high_score_text = Settings.font.render(f"High Score: {self.high_score}", True, Settings.colors['black'])
                press_space_text = Settings.font.render("Press space to restart", True, Settings.colors['black'])
                Settings.screen.blit(score_text, (200, 220))
                Settings.screen.blit(high_score_text, (200, 250))
                Settings.screen.blit(press_space_text, (200, 190))

                pygame.display.update()
                clock.tick(Settings.fps)


            
        # Game over screen
game_loop = Loop()