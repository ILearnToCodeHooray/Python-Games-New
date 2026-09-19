import pygame
from jtlgames.spritesheet import SpriteSheet
from pathlib import Path
from pygame import Vector2


images = Path(__file__).parent / 'images'
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, frog_images):
        super().__init__()
        self.image = frog_images[0]
        self.images = frog_images
        self.steps_left = 0
        self.direction_vector = pygame.math.Vector2(100, 0)
        self.screen = pygame.display.set_mode((640, 480))
        self.init_position = (0, 0)
        self.filename = images / 'spritesheet.png'
        self.cellsize = (16, 16)
        self.spritesheet = SpriteSheet(self.filename, self.cellsize)
        self.rect = self.image.get_rect(center=(x,y))
        self.frog_sprites = scale_sprites(self.spritesheet.load_strip(0, 4, colorkey=-1) , 4)
    def move(self, position):
        if self.steps_left <= 0:
            self.steps_left = self.direction_vector.length() / 3
            self.init_position = position
            self.final_position = position + self.direction_vector
            length = self.direction_vector.length()
            N = int(length // 3)
            self.step = (self.final_position - position) / N
    def draw_frog(self, index):
        index = index % (len(self.images))
        width = self.images[0].get_width()
        height = self.images[0].get_height()
        self.composed_image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.composed_image.blit(self.images[index], (0, 0))
        return self.composed_image
        
    def update(self):
        if self.steps_left > 0:
            self.rect.x += self.step[0]
            self.rect.y += self.step[1]
            self.steps_left -= 1
        
    def draw_line(self):
        end_position = pygame.math.Vector2(self.rect[0:2]) + self.direction_vector
        pygame.draw.line((self.screen), (255, 0, 0), pygame.math.Vector2(self.rect.center), end_position, 2)

class Alligator(pygame.sprite.Sprite):
    def __init__(self, start_pos, images):
        super().__init__()
        self.other_images = Path(__file__).parent / 'images'
        self.image = images[0]
        self.images = images
        self.rect = self.image.get_rect(center=(start_pos))
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]
        self.screen = pygame.display.set_mode((640, 480))
        self.index = 0
        self.filename = self.other_images / 'spritesheet.png'
        self.cellsize = (16, 16)
        self.spritesheet = SpriteSheet(self.filename, self.cellsize)
        self.frog_sprites = scale_sprites(self.spritesheet.load_strip(0, 4, colorkey=-1) , 4)
        self.sprite_rect = self.frog_sprites[0].get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.sprite_rect_vector = pygame.math.Vector2(self.screen.get_width() // 2, self.screen.get_height() // 2)
    def draw_alligator(self, index):
        """Creates a composed image of the alligator sprites.

        Args:
            alligator (list): List of alligator sprites.
            index (int): Index value to determine the right side sprite.

        Returns:
            pygame.Surface: Composed image of the alligator.
        """

        index = index % (4)
        
        width = self.images[0].get_width()
        height = self.images[0].get_height()
        composed_image = pygame.Surface((width * 3, height), pygame.SRCALPHA)

        composed_image.blit(self.image, (0, 0))
        composed_image.blit(self.images[1], (width, 1))
        composed_image.blit(self.images[(index + 3) % len(self.images)], (width * 2, 0))
        return composed_image

    def allig_update(self, player_pos):
        composed_alligator = self.draw_alligator(self.index)
        self.screen.blit(composed_alligator, self.rect)
        self.position = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.player_position = pygame.math.Vector2(player_pos)
        self.new_pos = self.position.move_towards(self.player_position, 1)
        self.rect.x = self.new_pos[0]
        self.rect.y = self.new_pos[1]

        return composed_alligator
def scale_sprites(sprites, scale):
    """Scale a list of sprites by a given factor.

    Args:
        sprites (list): List of pygame.Surface objects.
        scale (int): Scale factor.

    Returns:
        list: List of scaled pygame.Surface objects.
    """
    return [pygame.transform.scale(sprite, (sprite.get_width() * scale, sprite.get_height() * scale)) for sprite in sprites]

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Sprite Animation Test")
    filename = images / 'spritesheet.png'  # Replace with your actual file path
    cellsize = (16, 16)  # Replace with the size of your sprites
    spritesheet = SpriteSheet(filename, cellsize)

    # Load a strip sprites
    frog_sprites = scale_sprites(spritesheet.load_strip(0, 4, colorkey=-1) , 4)
    allig_sprites = scale_sprites(spritesheet.load_strip( (0,4), 9, colorkey=-1), 4)
    # Set up the display
    player = Player(300, 300, frog_sprites)
    allig = Alligator((100, 100), allig_sprites)
    # Load the sprite sheet
    frog_group = pygame.sprite.Group()
    alligator_group = pygame.sprite.Group()

    frog_group.add(player)
    alligator_group.add(allig)




    # Compose an image
    '''log = spritesheet.compose_horiz([24, 25, 26], colorkey=-1)
    log = pygame.transform.scale(log, (log.get_width() * 4, log.get_height() * 4))'''

    # Variables for animation
    frog_index = 0
    frames_per_image = 6
    frame_count = 0
    frog_frame_count = 0

    # Main game loop
    running = True
    sprite_rect = frog_sprites[0].get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    key_limit = 0
    pygame.math.Vector2(1, 0)

    while running:
        key_limit += 1
        keys = pygame.key.get_pressed()
        # Update animation every few frames
        frame_count += 1
        if player.steps_left <= 0:
            frog_frame_count += 1
        if frog_frame_count % frames_per_image == 0:
            frog_index = (frog_index + 1) % len(frog_sprites)
        if frame_count % frames_per_image == 0: 
            allig.index = (allig.index + 1) % len(allig_sprites)
        
        # Get the current sprite and display it in the middle of the screen
        
        #composed_allig = allig.draw_alligator(allig.index)
        #screen.blit(composed_allig, sprite_rect.move(allig.position))
        #screen.blit(log,  sprite_rect.move(0, -100))
        if key_limit%3 == 0:
            if keys[pygame.K_LEFT]:
                player.direction_vector = player.direction_vector.rotate(-5)
            elif keys[pygame.K_RIGHT]:
                player.direction_vector = player.direction_vector.rotate(5)

        if keys[pygame.K_UP]:
            player.direction_vector.scale_to_length(player.direction_vector.length() + 5)
        elif keys[pygame.K_DOWN]:
            player.direction_vector.scale_to_length(player.direction_vector.length() - 5)
        elif keys[pygame.K_SPACE]:
            player.move(player.rect.center)
            
        # Update the display


        player.update()
        frog_group.draw(screen)
        player.draw_line()
        
        pygame.draw.rect(screen, (255,0,0), allig.rect)
        allig.allig_update(player.rect.center)
        pygame.display.flip()
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 139))  # Clear screen with deep blue
        # Cap the frame rate

        pygame.time.Clock().tick(60)
        collider = pygame.sprite.groupcollide( 
            frog_group, alligator_group,
            True, True
            )
        if not len(collider) == 0:
            break
    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
