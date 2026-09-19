import pygame
import math
from pathlib import Path

assets = Path(__file__).parent / "images"

class Settings:
    """Class to store game configuration."""

    width = 800
    height = 600
    fps = 60
    triangle_size = 20
    projectile_speed = 5
    projectile_size = 11
    shoot_delay = 250  # 250 milliseconds between shots, or 4 shots per second
    colors = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0)}


# Notice that this Spaceship class is a bit different: it is a subclass of
# Sprite. Rather than a plain class, like in the previous examples, this class
# inherits from the Sprite class. The main additional function of a Sprite is
# that it can be added and removed from groups. This is useful for handling
# multiple objects of the same type, like projectiles.
class Spaceship(pygame.sprite.Sprite):
    """Class representing the spaceship."""

    def __init__(self, settings, position):
        super().__init__()

        self.game = None # will be set in Game.add()
        self.settings = settings

        self.angle = 0
        self.original_image = self.create_spaceship_image()

        self.velocity = pygame.Vector2(0, 0)

        self.acceleration = 1
        # For Sprites, the image and rect attributes are part of the Sprite class
        # and are important. The image is the surface that will be drawn on the screen

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
            

    def fire_projectile(self):
        """Creates and fires a projectile."""

        new_projectile = Projectile(
            self.settings,
            position=self.rect.center,
            angle=self.angle,
            velocity=self.settings.projectile_speed,
        )

        # Important! The game will update all of the sprites in the group, so we
        # need to add the projectile to the group to make sure it is updated.
        self.game.add(new_projectile)

    


    # The Sprite class defines an update method that is called every frame. We
    # can override this method to add our own functionality. In this case, we
    # are going to handle input and update the image of the spaceship. However,
    # we also need to call the update method of the parent class, so we use
    # super().update()
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.angle -= 5

        if keys[pygame.K_RIGHT]:
            self.angle += 5

        if keys[pygame.K_SPACE] and self.ready_to_shoot():
            self.fire_projectile()
        if keys[pygame.K_UP]:
  
            self.velocity = (pygame.Vector2(0, -1).rotate(self.angle))*self.acceleration
            self.acceleration = self.acceleration * 1.01
        elif not keys[pygame.K_UP]:
            self.velocity = pygame.Vector2(0, 0)
            self.acceleration = 1

        self.image = pygame.transform.rotate(self.original_image, -self.angle)

        # Reassigning the rect because the image has changed.
        self.rect = self.image.get_rect(center=self.rect.center)
        
        self.rect.center += self.velocity

        # Dont forget this part! If you don't call the Sprite update method, the
        # sprite will not be drawn
        super().update()

    # WAIT! Where is the draw method? We don't need to define it because the
    # Sprite class already has a draw method that will draw the image on the
    # screen. We only need to add the sprite to a group and the group will take
    # care of drawing the sprite.
class AlienSpaceship(Spaceship):
    
    def create_spaceship_image(self):
        """Creates the spaceship shape as a surface."""
        
        return pygame.image.load(assets/'alien1.gif')
        

class Projectile(pygame.sprite.Sprite):
    """Class to handle projectile movement and drawing."""

    def __init__(self, settings, position, velocity, angle):
        super().__init__()

        self.game = None  # will be set in Game.add()
        self.settings = settings

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


class Game:
    """Class to manage the game loop and objects."""

    def __init__(self, settings):
        pygame.init()
        pygame.key.set_repeat(1250, 1250)
        
        self.settings = settings
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        

        pygame.display.set_caption("Really Boring Asteroids")

        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()

    def add(self, sprite):
        """Adds a sprite to the game. Really important! This group is used to
        update and draw all of the sprites."""

        sprite.game = self

        self.all_sprites.add(sprite)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):

        # We only need to call the update method of the group, and it will call
        # the update method of all sprites But, we have to make sure to add all
        # of the sprites to the group, so they are updated.
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(self.settings.colors["black"])

        # The sprite group has a draw method that will draw all of the sprites in
        # the group.
        self.all_sprites.draw(self.screen)

        pygame.display.flip()

    def run(self):
        """Main Loop for the game."""
        
       
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.settings.fps)

        pygame.quit()


if __name__ == "__main__":

    settings = Settings()

    game = Game(settings)

    spaceship = AlienSpaceship(
        settings, position=(settings.width // 2, settings.height // 2)
    )
    game.add(spaceship)

    game.run()
