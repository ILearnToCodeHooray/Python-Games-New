import pygame
import math
from pathlib import Path
import random
#import numpy
pygame.init()
assets = Path(__file__).parent / "images"

class Settings:
    """Class to store game configuration.""" 
    font = pygame.font.SysFont(None, 36)
    width = 600
    height = 600
    fps = 60
    triangle_size = 20
    projectile_speed = 5 
    projectile_size = 11
    shoot_delay = 250  # 250 milliseconds between shots, or 4 shots per second
    colors = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0), "blue": (0, 0, 255)}
    score = 0
    lives = 3
    tank1health = 100
    tank2health = 100

class Tank(pygame.sprite.Sprite):
    """Class representing the spaceship."""

    def __init__(self, settings, position, team):
        super().__init__()

        self.game = None  # will be set in Game.add()
        self.settings = settings

        if team == 1:
            self.angle = -90
        else:
            self.angle = 90
        self.original_image = self.create_spaceship_image()

        self.move = pygame.Vector2(0, -10)

        self.velocity = pygame.Vector2(0, 0)
        self.team = team
        self.acceleration = 1
        # For Sprites, the image and rect attributes are part of the Sprite class
        # and are important. The image is the surface that will be drawn on the screen
        spaceship_position = position
        self.image = self.original_image.copy() 
        self.rect = self.image.get_rect(center=position)
        # These values help us limit the rate of fire
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = self.settings.shoot_delay  

    def create_spaceship_image(self):
        """Creates the spaceship shape as a surface."""
        image = pygame.Surface( (self.settings.triangle_size * 2, self.settings.triangle_size * 2),pygame.SRCALPHA)
        points = [
            (self.settings.triangle_size, 0),  # top point
            (0, self.settings.triangle_size * 2),  # left side point
            (self.settings.triangle_size * 2,self.settings.triangle_size * 2, ),  # right side point
        ]
        pygame.draw.polygon(image, self.settings.colors["white"], points)
        return image

    def ready_to_shoot(self):
        """Checks if the spaceship is ready to shoot again."""
        if pygame.time.get_ticks() - self.last_shot > self.shoot_delay:
            self.last_shot = pygame.time.get_ticks()
            return True
        return False
            
    def fire_projectile(self, team):
        """Creates and fires a projectile."""

        new_projectile = Projectile(
            self.settings,
            position=self.rect.center,
            angle=self.angle,
            velocity=self.settings.projectile_speed,
            team=team
        )

        self.game.add(new_projectile)

    def update(self):
        keys = pygame.key.get_pressed()
        if self.team == 1:
            if keys[pygame.K_UP]:
                self.velocity = (pygame.Vector2(0, -5).rotate(self.angle))
            elif not keys[pygame.K_DOWN]:
                self.velocity = (pygame.Vector2(0, 0).rotate(self.angle))

            if keys[pygame.K_LEFT]:
                self.angle -= 5
                self.move.rotate_ip(self.angle)

            if keys[pygame.K_RIGHT]:
                self.angle += 5
                self.move.rotate_ip(self.angle)

            if keys[pygame.K_DOWN]:
                self.velocity = (pygame.Vector2(0, 2.5).rotate(self.angle))
            elif not keys[pygame.K_UP]:
                self.velocity = (pygame.Vector2(0, 0).rotate(self.angle))

            if keys[pygame.K_RETURN] and self.ready_to_shoot():
                self.fire_projectile(1)
        else:
            if keys[pygame.K_w]:
                self.velocity = (pygame.Vector2(0, -5).rotate(self.angle))
            elif not keys[pygame.K_DOWN]:
                self.velocity = (pygame.Vector2(0, 0).rotate(self.angle))

            if keys[pygame.K_a]:
                self.angle -= 5
                self.move.rotate_ip(self.angle)

            if keys[pygame.K_d]:
                self.angle += 5
                self.move.rotate_ip(self.angle)

            if keys[pygame.K_s]:
                self.velocity = (pygame.Vector2(0, 2.5).rotate(self.angle))
            elif not keys[pygame.K_w]:
                self.velocity = (pygame.Vector2(0, 0).rotate(self.angle))

            if keys[pygame.K_SPACE] and self.ready_to_shoot():
                self.fire_projectile(2)
        # Reassigning the rect because the image has changed.
        self.rect = self.image.get_rect(center=self.rect.center)

        screen_width = self.settings.width
        screen_height = self.settings.height

        if self.rect.right < 0:
            self.rect.x = screen_width
            
        if self.rect.left > screen_width:
            self.rect.x = 0

        if self.rect.top > screen_height:
            self.rect.y = 0

        if self.rect.bottom < 0:
            self.rect.y = screen_height
        # Dont forget this part! If you don't call the Sprite update method, the
        # sprite will not be drawn
        self.rect.center += self.velocity
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        super().update()



class Projectile(pygame.sprite.Sprite):
    """Class to handle projectile movement and drawing."""

    def __init__(self, settings, position, velocity, angle, team):
        super().__init__()

        self.game = None  # will be set in Game.add()
        self.settings = settings
        self.team = team
        # The (0,-1) part makes the vector point up, and the rotate method
        # rotates the vector by the given angle. Finally, we multiply the vector
        # by the velocity (scalar) to get the final velocity vector.
        self.velocity = pygame.Vector2(0, -1).rotate(angle) * velocity

        # Dont forget to create the image and rect attributes for the sprite
        self.image = pygame.Surface(
            (self.settings.projectile_size, self.settings.projectile_size),
            pygame.SRCALPHA,
        )

        half_size = self.settings.projectile_size // 2

        pygame.draw.circle(
            self.image,
            self.settings.colors["red"],
            center=(half_size + 1, half_size + 1),
            radius=half_size,
        )

        # Notice that we are using the rect attribute to store the position of the projectile
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.center += self.velocity


tanks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

class Game:
    """Class to manage the game loop and objects."""

    def __init__(self, settings):
        pygame.init()
        self.side = random.randint(1,4)
        self.settings = settings
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))

        pygame.display.set_caption("Really Boring Asteroids")

        self.clock = pygame.time.Clock()
        self.running = True

    def add(self, sprite):
        """Adds a sprite to the game. Really important! This group is used to
        update and draw all of the sprites."""

        sprite.game = self

        all_sprites.add(sprite)
        
        if isinstance(sprite, Tank):
            tanks.add(sprite)
        elif isinstance(sprite, Projectile):
            projectiles.add(sprite)

    def update(self):
        collision = pygame.sprite.groupcollide(
            tanks, projectiles,
            False, False,
            collided = pygame.sprite.collide_mask
        )
        for tank in collision:
            for projectile in collision[tank]:
                if not tank.team == projectile.team:
                    if tank.team == 1:
                        Settings.tank1health -= 10
                        print(Settings.tank1health)
                        projectile.kill()
                    elif tank.team == 2:
                        Settings.tank2health -= 10
                        print(Settings.tank2health)
                        projectile.kill()

        projectiles.update()

    def draw(self):
        self.screen.fill(self.settings.colors["black"])
        tank1health_text = self.settings.font.render(f"Tank 1 Health: {self.settings.tank1health}", True, self.settings.colors["white"])
        self.screen.blit(tank1health_text, (10, 10))
        tank2health_text = self.settings.font.render(f"Tank 2 Health: {self.settings.tank2health}", True, self.settings.colors["white"])
        self.screen.blit(tank2health_text, (350, 10))
        # The sprite group has a draw method that will draw all of the sprites in
        # the group.
        all_sprites.draw(self.screen)
        pygame.display.flip()


    def run(self):
        """Main Loop for the game."""
       
        while True:
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                self.clock.tick(self.settings.fps)
                tanks.update()
                self.update()
                self.draw()
                self.clock.tick(1500)
            pygame.quit()

if __name__ == "__main__":

    settings = Settings()

    game = Game(settings)

    tank_1 = Tank(
        settings, position=(500, settings.height // 2), team=1
    )
    tank_2 = Tank(
        settings, position=(100, settings.height // 2), team=2
    )
    game.add(tank_1)
    game.add(tank_2)

    game.run()