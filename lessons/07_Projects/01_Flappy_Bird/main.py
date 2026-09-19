import pygame
import random
from pathlib import Path
assets = Path(__file__).parent

pygame.init()
class Settings:
    """A class to store all settings for the game."""
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 450
    BACKGROUND_SCROLL_SPEED = 2
    FPS = 30
    gravity: int = 1
    jump_y_velocity: int = 30
    jump_x_velocity: int = 10
    speed = 5
    size = 25
    fps = 60
    colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'blue': (0, 0, 255)
        }
    game_over = False
    obstacle_width= 100
    obstacle_height = 300
    obstacle_speed = 5
    obstacle_x = 0
    score = 0
    font = pygame.font.SysFont(None, 36)
    high_score = 0
    obstacles_passed = 0
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        cactus_image = pygame.image.load(assets/'images/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(cactus_image, (self.settings.obstacle_width, self.settings.obstacle_height))
        self.rect = self.image.get_rect()
        self.rect.x = Settings.SCREEN_WIDTH
        Settings.obstacle_x = Settings.SCREEN_WIDTH
        self.rect.y = Settings.SCREEN_WIDTH - Settings.obstacle_height
        self.scored = False
        self.alive = True
        self.collided = False

    def update(self):
        self.rect.x -= Settings.obstacle_speed
        Settings.obstacle_x -= Settings.obstacle_speed
        # Remove the obstacle if it goes off screen
        if self.rect.x < -100:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, Settings):
        super().__init__()
        dino_image = pygame.image.load(assets/'images/bluebird-midflap.png').convert_alpha()
        self.image = pygame.transform.scale(dino_image, (Settings.size, Settings.size))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = Settings.SCREEN_HEIGHT - Settings.size - 10

        # Jump variables
        self.velocity = 0
        self.gravity = 1
        self.jump_strength = -10

    def update(self):
        # Apply gravity
        self.velocity += self.gravity
        self.rect.y += self.velocity

        # Prevent falling below ground
        if self.rect.bottom >= Settings.SCREEN_HEIGHT:
            self.rect.bottom = Settings.SCREEN_HEIGHT
            self.velocity = 0

player = Player(Settings)
player_group = pygame.sprite.Group(player)

class Background(pygame.sprite.Sprite):
    """Represents the scrolling background in the game."""
    def __init__(self):
        super().__init__()
        
        # The Sprite image is 2x as wide as the screen
        self.image = pygame.Surface((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        
        # Load the background image and scale it to the screen size. Note the convert() call. 
        # This converts the form of the image to be more efficient. 
        orig_image= pygame.image.load(assets/'images/background.png').convert()
        orig_image = pygame.transform.scale(orig_image, (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        
        # Then, copy it into the self.image surface twice
        self.image.blit(orig_image, (0, 0))
        self.image.blit(orig_image, (Settings.SCREEN_WIDTH, 0))
        
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
class Game_Over(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        gm_ovr_img = pygame.image.load(assets/'images/gameover.png').convert_alpha()
        self.image = pygame.transform.scale(gm_ovr_img, (550, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

game_over_screen = Game_Over()
game_over_group = pygame.sprite.Group(game_over_screen)
def add_obstacle(obstacles):
    # random.random() returns a random float between 0 and 1, so a value
    # of 0.25 means that there is a 25% chance of adding an obstacle. Since
    # add_obstacle() is called every 100ms, this means that on average, an
    # obstacle will be added every 400ms.
    # The combination of the randomness and the time allows for random
    # obstacles, but not too close together. 
    
    obstacle = Obstacle(Settings)
    obstacle.rect.y = random.randint(200, 400)
    y = obstacle.rect.y
    obstacles.add(obstacle)
    obstacle = Obstacle(Settings)
    obstacle.rect.y = y - 400
    obstacle.image = pygame.transform.rotate(obstacle.image, 180)
    obstacles.add(obstacle)
    return 1

def main():
    """Run the main game loop."""
    running = True
    obstacles = pygame.sprite.Group()
    obstacle_count = 0
    bg = Background()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bg)

    clock = pygame.time.Clock()
    last_obstacle_time = pygame.time.get_ticks()
    obstacles = pygame.sprite.Group()
    screen.fill(Settings.colors['white'])
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.velocity = player.jump_strength
                if event.key == pygame.K_SPACE and Settings.game_over:
                    Settings.score = 0
                    Settings.game_over = False
                    main()
        player.update()
        all_sprites.update()
        if pygame.time.get_ticks() - last_obstacle_time > 1500:
            last_obstacle_time = pygame.time.get_ticks()
            obstacle_count += add_obstacle(obstacles)
        obstacles.update()

        for obstacle in obstacles:
            if not obstacle.scored and not obstacle.collided and obstacle.rect.right < player.rect.left and not Settings.game_over:
                Settings.score += 1
                obstacle.scored = True
        
        collider = pygame.sprite.spritecollide(player, obstacles, dokill=False)
        for obstacle in collider:
            if not obstacle.collided:
                obstacle.collided = True
                Settings.game_over = True
                if Settings.score > Settings.high_score:
                    Settings.high_score = Settings.score
        if Settings.game_over == True:
            screen.fill(Settings.colors['white'])
            game_over_group.draw(screen)
            score_text = Settings.font.render(f"Score: {int(Settings.score/2)}", True, Settings.colors['black'])
            high_score_text = Settings.font.render(f"High Score: {int(Settings.high_score/2)}", True, Settings.colors['black'])
            press_space_text = Settings.font.render("Press space to restart", True, Settings.colors['black'])
            screen.blit(score_text, (200, 220))
            screen.blit(high_score_text, (200, 250))
            screen.blit(press_space_text, (200, 190))
            
        else:
            all_sprites.draw(screen)
            player_group.draw(screen)
            obstacles.draw(screen)
            score_text = Settings.font.render(f"Score: {int(Settings.score/2)}", True, Settings.colors['black'])
            screen.blit(score_text, (10, 10))
            pygame.display.update()
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()