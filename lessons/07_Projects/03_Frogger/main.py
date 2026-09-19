import pygame
import random
from pathlib import Path
d = Path(__file__).parent
pygame.init()

class Settings:
    """A class to store all settings for the game."""
    SCREEN_WIDTH  = 600
    SCREEN_HEIGHT = 600
    FPS = 30
    laser_count = 0
    alien_move_speed = 2
    score = 0
    font = pygame.font.SysFont(None, 36)
    colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'blue': (0, 0, 255),
            'green': (0, 255, 0),
            'gray': (127, 127, 127)
        }
    obstacle_width= 100
    obstacle_height = 100
    obstacle_speed = 5
    game_over = False
    high_score = 0

screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("Frogger")

class car_left(pygame.sprite.Sprite):
    def __init__(self, settings, y):
        super().__init__()
        self.settings = settings
        car_image = pygame.image.load(d / "images/carLeft.png").convert_alpha()
        self.image = pygame.transform.scale(car_image, (self.settings.obstacle_width, self.settings.obstacle_height))
        self.rect = self.image.get_rect()
        self.rect.x = Settings.SCREEN_WIDTH
        Settings.obstacle_x = Settings.SCREEN_WIDTH
        self.rect.y = y
        self.scored = False
        self.alive = True
        self.collided = False

    def update(self, level):
        self.rect.x -= Settings.obstacle_speed * level
        Settings.obstacle_x -= Settings.obstacle_speed * level
        # Remove the obstacle if it goes off screen
        if self.rect.x < 0:
            self.kill()

class car_right(pygame.sprite.Sprite):
    def __init__(self, settings, y):
        super().__init__()
        self.settings = settings
        car_image = pygame.image.load(d / "images/carRight.png").convert_alpha()
        self.image = pygame.transform.scale(car_image, (self.settings.obstacle_width, self.settings.obstacle_height))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        Settings.obstacle_x = 0
        self.rect.y = y
        self.scored = False
        self.alive = True
        self.collided = False

    def update(self, level):
        self.rect.x += Settings.obstacle_speed * level
        Settings.obstacle_x += Settings.obstacle_speed * level
        # Remove the obstacle if it goes off screen
        if self.rect.x < 0:
            self.kill()

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        orig_image = pygame.image.load(d/'images/frogger_road_bg.png').convert()
        orig_image = pygame.transform.scale(orig_image, (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        self.image.blit(orig_image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -50

class Game_Over(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        gm_ovr_img = pygame.image.load(d/'images/gameover.png').convert_alpha()
        self.image = pygame.transform.scale(gm_ovr_img, (550, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

game_over_screen = Game_Over()
game_over_group = pygame.sprite.Group(game_over_screen)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_image = pygame.image.load(d/'images/frog.png').convert_alpha()
        self.image = pygame.transform.scale(player_image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 450

player = Player()
player_group = pygame.sprite.Group(player)

def add_car_left(obstacles, row):
    # random.random() returns a random float between 0 and 1, so a value
    # of 0.25 means that there is a 25% chance of adding an obstacle. Since
    # add_obstacle() is called every 100ms, this means that on average, an
    # obstacle will be added every 400ms.
    # The combination of the randomness and the time allows for random
    # obstacles, but not too close together. 
    if random.random() < 0.4:
        if row == "row_1":
            obstacle = car_left(Settings, 375)
            obstacles.add(obstacle)
            return 1
        if row == "row_3":
            obstacle = car_left(Settings, 225)
            obstacles.add(obstacle)
            return 1
        if row == "row_5":
            obstacle = car_left(Settings, 75)
            obstacles.add(obstacle)
            return 1
    return 0
def add_car_right(obstacles, row):
    # random.random() returns a random float between 0 and 1, so a value
    # of 0.25 means that there is a 25% chance of adding an obstacle. Since
    # add_obstacle() is called every 100ms, this means that on average, an
    # obstacle will be added every 400ms.
    # The combination of the randomness and the time allows for random
    # obstacles, but not too close together.
    if random.random() < 0.4:
        if row == "row_2":
            obstacle = car_right(Settings, 300)
            obstacles.add(obstacle)
            return 1
        if row == "row_4":
            obstacle = car_right(Settings, 150)
            obstacles.add(obstacle)
            return 1
    return 0
def main():
    """Run the main game loop."""
    running = True
    bg = Background()
    all_sprites = pygame.sprite.Group(bg)
    clock = pygame.time.Clock()
    last_car_time = pygame.time.get_ticks()
    row_1 = pygame.sprite.Group()
    row_2 = pygame.sprite.Group()
    row_3 = pygame.sprite.Group()
    row_4 = pygame.sprite.Group()
    row_5 = pygame.sprite.Group()
    car_count = 0
    score = 0
    level = 1
    lives = 3
    time_start = pygame.time.get_ticks()/1000
    while running:
        time_since_start = pygame.time.get_ticks()/1000 - time_start
        time = 30 - time_since_start
        time_int = int(time)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if keys[pygame.K_UP] and not player.rect.y == 0:
                player.rect.y -= 75
            if keys[pygame.K_DOWN] and not player.rect.y == 450:
                player.rect.y += 75
            if keys[pygame.K_LEFT] and not player.rect.x == 0:
                player.rect.x -= 75
            if keys[pygame.K_RIGHT] and not player.rect.x == 525:
                player.rect.x += 75
            if keys[pygame.K_SPACE] and Settings.game_over:
                    score = 0
                    Settings.game_over = False
                    main()
        if pygame.time.get_ticks() - last_car_time > 300:
            last_car_time = pygame.time.get_ticks()
            which_row = random.randint(0,5)
            if which_row == 1:
                car_count += add_car_left(row_1, "row_1")
            elif which_row == 2:
                car_count += add_car_right(row_2, "row_2")
            elif which_row == 3:
                car_count += add_car_left(row_3, "row_3")
            elif which_row == 4:
                car_count += add_car_right(row_4, "row_4")
            elif which_row == 5:
                car_count += add_car_left(row_5, "row_5")
        if pygame.sprite.groupcollide(row_1, player_group, False, False) and player.rect.y == 375:
            lives -= 1
            player.rect.y = 450
        if pygame.sprite.groupcollide(row_2, player_group, False, False) and player.rect.y == 300:
            lives -= 1
            player.rect.y = 450
        if pygame.sprite.groupcollide(row_3, player_group, False, False) and player.rect.y == 225:
            lives -= 1
            player.rect.y = 450
        if pygame.sprite.groupcollide(row_4, player_group, False, False) and player.rect.y == 150:
            lives -= 1
            player.rect.y = 450
        if pygame.sprite.groupcollide(row_5, player_group, False, False) and player.rect.y == 75:
            lives -= 1   
            player.rect.y = 450                                         
        if player.rect.y == 0:
            score += 1
            player.rect.y = 450
            time_start = pygame.time.get_ticks()/1000 + 1
        if time_int <= 0:
            Settings.game_over = True
        if score % 4 == 0 and not score == 0:
            level = int(score/4 + 1)
            lives = 3
        if lives == 0:
            Settings.game_over = True
            if score > Settings.high_score:
                Settings.high_score = score
        if Settings.game_over == True:
            screen.fill(Settings.colors['white'])
            game_over_group.draw(screen)
            score_text = Settings.font.render(f"Score: {int(score)}", True, Settings.colors['black'])
            high_score_text = Settings.font.render(f"High Score: {int(Settings.high_score)}", True, Settings.colors['black'])
            screen.blit(score_text, (200, 220))
            screen.blit(high_score_text, (200, 250))
        else:
            row_1.update(level)
            row_2.update(level)
            row_3.update(level)
            row_4.update(level)
            row_5.update(level)
            all_sprites.update()
            all_sprites.draw(screen)
            player_group.draw(screen)
            row_1.draw(screen)
            row_2.draw(screen)
            row_3.draw(screen)
            row_4.draw(screen)
            row_5.draw(screen)       
            time_text = Settings.font.render(f"Time left: {int(time)}", True, Settings.colors['black'])
            screen.blit(time_text, (10, 10))
            score_text = Settings.font.render(f"Score: {score}", True, Settings.colors['black'])
            screen.blit(score_text, (175, 10))
            level_text = Settings.font.render(f"Level {level}", True, Settings.colors['black'])
            screen.blit(level_text, (300, 10))
            lives_text = Settings.font.render(f"Lives: {lives}", True, Settings.colors['black'])
            screen.blit(lives_text, (400, 10))
            clock.tick(Settings.FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()