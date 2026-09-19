import pygame

pygame.init()

# ------------------------
# Setup
# ------------------------
SCREEN_W, SCREEN_H = 600, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Scrolling Background - Class Version")

# ------------------------
# Background class
# ------------------------
class Background(pygame.sprite.Sprite):
    def __init__(self, colors, tile_width=100, scroll_speed=120):
        super().__init__()
        self.tile_width = tile_width
        self.scroll_speed = scroll_speed  # pixels per second
        self.image = self.make_repeating_pattern(colors)
        self.rect = self.image.get_rect(topleft=(0, 0))  # where pattern starts
        self.pattern_width = self.image.get_width()

    def make_color_tile(self, color):
        """Return a 100px-wide Surface as tall as the screen, filled with color."""
        surf = pygame.Surface((self.tile_width, SCREEN_H))
        surf.fill(color)
        return surf

    def make_repeating_pattern(self, colors):
        """Create one long repeating strip of colored tiles."""
        pattern_w = self.tile_width * len(colors)
        pattern = pygame.Surface((pattern_w, SCREEN_H)).convert()
        x = 0
        for color in colors:
            pattern.blit(self.make_color_tile(color), (x, 0))
            x += self.tile_width
        return pattern

    def update(self, dt):
        """Move the background leftward by scroll_speed * dt."""
        self.rect.x -= self.scroll_speed * dt

        # Once it has fully scrolled left past one pattern width, reset it.
        if self.rect.x <= -self.pattern_width:
            self.rect.x = 0

    def draw(self, surface):
        """Draw the pattern twice to fill the whole screen."""
        surface.blit(self.image, (self.rect.x, 0))
        surface.blit(self.image, (self.rect.x + self.pattern_width, 0))

# ------------------------
# Create background object
# ------------------------
stripe_colors = [
    (231, 76, 60),   # red
    (46, 204, 113),  # green
    (52, 152, 219),  # blue
    (241, 196, 15),  # yellow
    (155, 89, 182),  # purple
    (26, 188, 156),  # teal
]

background = Background(stripe_colors, tile_width=100, scroll_speed=120)

# ------------------------
# Main loop
# ------------------------
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0  # seconds since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update and draw
    background.update(dt)
    background.draw(screen)

    pygame.display.flip()

pygame.quit()
