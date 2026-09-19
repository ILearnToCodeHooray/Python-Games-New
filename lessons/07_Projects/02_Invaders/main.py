import pygame
from pathlib import Path
d = Path(__file__).parent
pygame.init()

class Settings:
    """A class to store all settings for the game."""
    SCREEN_WIDTH  = 600
    SCREEN_HEIGHT = 750
    FPS = 30
    laser_count = 0
    alien_move_speed = 2
    score = 0
    font = pygame.font.SysFont(None, 36)
    colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'blue': (0, 0, 255)
        }
    game_over = False
    
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        orig_image= pygame.image.load(d/'images/space.png').convert()
        orig_image = pygame.transform.scale(orig_image, (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        self.image.blit(orig_image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -200
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        alien_image = pygame.image.load(d/'images/alien.png').convert_alpha()
        self.image = pygame.transform.scale(alien_image, (25, 25))
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_image = pygame.image.load(d/'images/rocket.png').convert_alpha()
        self.image = pygame.transform.scale(player_image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = Settings.SCREEN_HEIGHT - 250
        
player = Player()
player_group = pygame.sprite.Group(player)


class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        laser_image = pygame.image.load(d/'images/projectile.png').convert_alpha()
        self.image = pygame.transform.scale(laser_image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.y = player.rect.y
        self.rect.x = player.rect.x
        self.alive = True
        self.collided = False
    def update(self):
        self.rect.y -= 10
        if self.rect.y < 0:
            Settings.laser_count -= 1
            self.kill()

def shoot_laser(Lasers):
    if Settings.laser_count < 4:
        laser = Laser()
        laser.rect.x = player.rect.x
        Lasers.add(laser)
        Settings.laser_count += 1
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
def main():
    """Run the main game loop."""
    running = True
    game_begun = False
    bg = Background()
    all_sprites = pygame.sprite.Group(bg)
    lasers = pygame.sprite.Group()
    alien_group = pygame.sprite.Group()
    alienlist = []
    while game_begun == False:
        main_menu = Settings.font.render("Press space to begin", True, Settings.colors['black'])
        screen.fill(Settings.colors['white'])
        screen.blit(main_menu, (200, 200))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_begun = True
    if game_begun == True:
        x = 20
        y = 0
        for i in range(4):
            for i in range(10):
                alien = Alien(x, y)
                alien_group.add(alien)
                alienlist.append(alien)
                x += 40
            x = 20
            y -= 30
        for i in range(10):
            alien = Alien(x, -30)
            alien_group.add(alien)
            alienlist.append(alien)
            x += 40
        clock = pygame.time.Clock()
        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        shoot_laser(lasers)
            if keys[pygame.K_LEFT]:
                player.rect.x -= 5
            if keys[pygame.K_RIGHT]:
                player.rect.x += 5
            for alien in alienlist:
                alien.rect.x += Settings.alien_move_speed
            for alien in alienlist:
                if alien.rect.x > 600:
                    Settings.alien_move_speed = -2
                    for alien in alienlist:
                        alien.rect.y += 20
                    break
                if alien.rect.x < 0:
                    Settings.alien_move_speed = 2
                    for alien in alienlist:
                        alien.rect.y += 20
                    break
            if pygame.sprite.groupcollide(alien_group, lasers, True, True):
                Settings.laser_count -= 1
                Settings.score += 1
            if pygame.sprite.groupcollide(alien_group, player_group, False, False):
                Settings.game_over = True
            if Settings.game_over == True:
                screen.fill(Settings.colors['white'])
                game_over_group.draw(screen)
                score_text = Settings.font.render(f"Score: {int(Settings.score)}", True, Settings.colors['black'])
                screen.blit(score_text, (200, 220))
            else:
                score_text = Settings.font.render(f"Score: {int(Settings.score)}", True, Settings.colors['white'])

                all_sprites.update()
                all_sprites.draw(screen)
                player_group.draw(screen)
                alien_group.draw(screen)
                lasers.draw(screen)
                lasers.update()
                screen.blit(score_text, (0, 0))
            pygame.display.flip()
            
            clock.tick(Settings.FPS)
    pygame.quit()



if __name__ == "__main__":
    main()