import pygame
import random
import math
from pathlib import Path
d = Path(__file__).parent/ 'images'
pygame.init()

class Colors:
    """Constants for Colors"""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    PLAYER_COLOR = (0, 0, 255)
    BACKGROUND_COLOR = (255, 255, 255)

class Settings:
    """Settings for the game"""
    font = pygame.font.SysFont(None, 36)
    colors = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0), "blue": (0, 0, 255)}
    width: int = 600
    height: int = 400
    gravity: float = 0.3
    player_start_x: int = 100
    player_start_y: int = 100
    player_v_y: float = 0  # Initial y velocity
    player_v_x: float = 0  # Initial x velocity
    player_width: int = 10
    player_height: int = 10
    player_jump_velocity: float = 15
    frame_rate: int = 15
    lives = 3
    move = pygame.Vector2(0, 1)
    fuel = 100
    score = 0
    lines = []

class Game:
    """Main object for the top level of the game. Holds the main loop and other
    update, drawing and collision methods that operate on multiple other
    objects, like the player and obstacles."""
    
    def __init__(self, settings: Settings):
        pygame.init()

        self.settings = settings
        self.running = True

        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        self.clock = pygame.time.Clock()

        # Turn Gravity into a vector
        self.gravity = pygame.Vector2(0, self.settings.gravity)
        self.v1_tup = (0,270)
        self.v2_tup = (10, 350)
        self.v3_tup = (50, 340)
        self.v4_tup = (150, 280)
        self.v5_tup = (200, 330)
        self.v6_tup = (230, 330)
        self.v7_tup = (280, 380)
        self.v8_tup = (330, 380)
        self.v9_tup = (400, 300)
        self.v10_tup = (420, 320)
        self.v11_tup = (470, 320)
        self.v12_tup = (530, 270)
        self.v13_tup = (600, 270)
        v1 = pygame.math.Vector2(self.v1_tup)
        v2 = pygame.math.Vector2(self.v2_tup)
        v3 = pygame.math.Vector2(self.v3_tup)
        v4 = pygame.math.Vector2(self.v4_tup)
        v5 = pygame.math.Vector2(self.v5_tup)
        v6 = pygame.math.Vector2(self.v6_tup)
        v7 = pygame.math.Vector2(self.v7_tup)
        v8 = pygame.math.Vector2(self.v8_tup)
        v9 = pygame.math.Vector2(self.v9_tup)
        v10 = pygame.math.Vector2(self.v10_tup)
        v11 = pygame.math.Vector2(self.v11_tup)
        v12 = pygame.math.Vector2(self.v12_tup)
        v13 = pygame.math.Vector2(self.v13_tup)
        Settings.lines.append(v1)
        Settings.lines.append(v2)
        Settings.lines.append(v3)
        Settings.lines.append(v4)
        Settings.lines.append(v5)
        Settings.lines.append(v6)
        Settings.lines.append(v7)
        Settings.lines.append(v8)
        Settings.lines.append(v9)
        Settings.lines.append(v10)
        Settings.lines.append(v11)
        Settings.lines.append(v12)
        Settings.lines.append(v13)

    def run(self):
        """Main game loop"""
        player = Player(self)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False

            if Settings.fuel == 0:
                pygame.quit()
            player.update()

            self.screen.fill(Colors.BACKGROUND_COLOR)
            player.draw(self.screen)
            fuel_text = Settings.font.render(f"Fuel: {(Settings.fuel)}", True, Settings.colors['black'])
            self.screen.blit(fuel_text, (10, 10))
            score_text = Settings.font.render(f"Score: {(Settings.score)}", True, Settings.colors['black'])
            self.screen.blit(score_text, (150, 10))
            lives_text = Settings.font.render(f"Lives: {(Settings.lives)}", True, Settings.colors['black'])
            self.screen.blit(lives_text, (300, 10))

            for i, line in enumerate(Settings.lines[0:-1]):
                pygame.draw.line(self.screen, (0,0, i), line, Settings.lines[i+1], 2)

            if Settings.lives == 0:
                pygame.quit()            
            pygame.display.flip()
            self.clock.tick(self.settings.frame_rate)
        pygame.quit()

class Player(pygame.sprite.Sprite):
    """Player class, just a bouncing rectangle"""

    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        settings = self.game.settings
        self.original_image = pygame.image.load(d/'lander.png')
        self.original_image_scaled = pygame.transform.scale(self.original_image, (self.original_image.get_width() / 3, self.original_image.get_height() / 3))
        self.image = self.original_image_scaled.copy()
        self.width = Settings.player_width
        self.height = Settings.player_height
        self.angle = 0
        self.rect = self.original_image_scaled.get_rect()
        # Vector for our jump velocity, which is just up
        self.v_jump = pygame.Vector2(0, -settings.player_jump_velocity)

        # Player position
        self.pos = pygame.Vector2(settings.player_start_x, settings.player_start_y if settings.player_start_y is not None else settings.height - self.height)
        
        # Player's velocity
        self.vel = pygame.Vector2(settings.player_v_x, settings.player_v_y)  # Velocity vector
        #self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def going_up(self):
        """Check if the player is going up"""
        return self.vel.y < 0
    
    def going_down(self):
        """Check if the player is going down"""
        return self.vel.y > 0
    
    def going_left(self):
        """Check if the player is going left"""
        return self.vel.x < 0
    
    def going_right(self):
        """Check if the player is going right"""
        return self.vel.x > 0

    def at_top(self):
        """Check if the player is at the top of the screen"""
        return self.pos.y <= 0
    
    def at_bottom(self):
        """Check if the player is at the bottom of the screen"""
        return self.pos.y >= self.game.settings.height - self.height

    def at_left(self):
        """Check if the player is at the left of the screen"""
        return self.pos.x <= 0
    
    def at_right(self):
        """Check if the player is at the right of the screen"""
        return self.pos.x >= self.game.settings.width - self.width

    def update(self):
        """Update player position, continuously jumping"""
        self.update_v()
        self.update_pos()

    def update_v(self):
        """Update the player's velocity based on gravity and bounce on edges"""
        self.vel += self.game.gravity  # Add gravity to the velocity
        self.rect.y = self.pos.y
        self.rect.x = self.pos.x

        if self.rect.clipline(game.v5_tup, game.v6_tup):
            if self.angle > -21 and self.angle < 21 and self.vel.y != 0 and self.vel.y < 6:
                self.pos.x = Settings.player_start_x
                self.pos.y = Settings.player_start_y
                self.vel.y = 0
                self.vel.x = 0
                Settings.score += 5
            else:
                self.vel.y = 0
                self.vel.x = 0
                self.pos.x = Settings.player_start_x
                self.pos.y = Settings.player_start_y
                Settings.lives -= 1

        elif self.rect.clipline(game.v7_tup, game.v8_tup):
            if self.angle > -21 and self.angle < 21 and self.vel.y != 0 and self.vel.y < 6:
                self.pos.x = Settings.player_start_x
                self.pos.y = Settings.player_start_y
                self.vel.y = 0
                self.vel.x = 0
                Settings.score += 5
            else:
                self.vel.y = 0
                self.vel.x = 0
                self.pos.x = Settings.player_start_x
                self.pos.y = Settings.player_start_y
                Settings.lives -= 1

        elif self.rect.clipline(game.v10_tup, game.v11_tup):
            if self.angle > -21 and self.angle < 21 and self.vel.y != 0 and self.vel.y < 6:
                self.pos.x = Settings.player_start_x
                self.pos.y = Settings.player_start_y
                self.vel.y = 0
                self.vel.x = 0
                Settings.score += 5
            else:
                self.vel.y = 0
                self.vel.x = 0
                self.pos.x = Settings.player_start_x
                self.pos.y = Settings.player_start_y
                Settings.lives -= 1

        elif self.rect.clipline(game.v12_tup, game.v13_tup):
            if self.angle > -21 and self.angle < 21 and self.vel.y != 0 and self.vel.y < 6:
                self.pos.x = Settings.player_start_x
                self.pos.y = Settings.player_start_y
                self.vel.y = 0
                self.vel.x = 0
                Settings.score += 5
            else:
                self.vel.y = 0
                self.vel.x = 0
                self.pos.x = Settings.player_start_x
                self.pos.y = Settings.player_start_y
                Settings.lives -= 1

        elif self.rect.clipline(game.v1_tup, game.v2_tup):
            self.pos.x = Settings.player_start_x
            self.pos.y = Settings.player_start_y
            self.vel.y = 0
            self.vel.x = 0
            Settings.lives -= 1
        elif self.rect.clipline(game.v2_tup, game.v3_tup):
            self.pos.x = Settings.player_start_x
            self.pos.y = Settings.player_start_y
            self.vel.y = 0
            self.vel.x = 0
            Settings.lives -= 1
        elif self.rect.clipline(game.v3_tup, game.v4_tup):
            self.pos.x = Settings.player_start_x
            self.pos.y = Settings.player_start_y
            self.vel.y = 0
            self.vel.x = 0
            Settings.lives -= 1
        elif self.rect.clipline(game.v4_tup, game.v5_tup):
            self.pos.x = Settings.player_start_x
            self.pos.y = Settings.player_start_y
            self.vel.y = 0
            self.vel.x = 0
            Settings.lives -= 1
        elif self.rect.clipline(game.v6_tup, game.v7_tup):
            self.pos.x = Settings.player_start_x
            self.pos.y = Settings.player_start_y
            self.vel.y = 0
            self.vel.x = 0
            Settings.lives -= 1
        elif self.rect.clipline(game.v8_tup, game.v9_tup):
            self.pos.x = Settings.player_start_x
            self.pos.y = Settings.player_start_y
            self.vel.y = 0
            self.vel.x = 0
            Settings.lives -= 1
        elif self.rect.clipline(game.v9_tup, game.v10_tup):
            self.pos.x = Settings.player_start_x
            self.pos.y = Settings.player_start_y
            self.vel.y = 0
            self.vel.x = 0
            Settings.lives -= 1
        elif self.rect.clipline(game.v11_tup, game.v12_tup):
            self.pos.x = Settings.player_start_x
            self.pos.y = Settings.player_start_y
            self.vel.y = 0
            self.vel.x = 0
            Settings.lives -= 1
        elif self.at_top() and self.going_up():
            self.vel.y = 0

            # If the player hits one side of the screen or the other, bounce the
            # player. we are also checking if the player has a velocity going farther
            # off the screeen, because we don't want to bounce the player if it's
            # already going away from the edge
        if self.at_bottom:
            drag = (0, 0)
        else:
            drag = -self.vel * 0.1
            self.vel += drag

    def update_pos(self):
        """Update the player's position based on velocity"""
        self.pos += self.vel  # Update the player's position based on the current velocity

        # If the player is at the bottom, stop the player from falling and
        # stop the jump
        
        if self.at_bottom():
            self.pos.y = self.game.settings.height - self.height

        if self.at_top():
            self.pos.y = 0

        # Don't let the player go off the left side of the screen
        if self.at_left():
            self.pos.x = self.game.settings.width - self.width
  
        # Don't let the player go off the right side of the screen
        elif self.at_right():
            self.pos.x = 0

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.angle += 5
            Settings.move = pygame.Vector2(0,1)
            Settings.move.rotate_ip(-self.angle)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.angle -= 5
            Settings.move = pygame.Vector2(0,1)
            Settings.move.rotate_ip(-self.angle)
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.vel -= Settings.move
            Settings.fuel -= 1
        if self.rect.clipline((200, 330), (230, 330)):
            pygame.quit()
    def draw(self, screen):
        self.image_rotated = pygame.transform.rotate(self.image, self.angle)
        screen.blit(self.image_rotated, (self.pos.x, self.pos.y))
settings = Settings()
game = Game(settings)
game.run()