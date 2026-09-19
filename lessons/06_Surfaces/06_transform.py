import pygame
from jtlgames.spritesheet import SpriteSheet
from pathlib import Path
import random 

images = Path(__file__).parent / 'images'




# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((640, 480))

grid = []
for y in range(0, screen.get_height(), 48):
    for x in range(0, screen.get_width(), 48):
        grid.append((x, y))
    print(len(grid))
 
print(grid[51], grid[100])


pygame.display.set_caption("")

# Load the sprite sheet
filename = images / 'spritesheet.png'  # Replace with your actual file path
cellsize = (16, 16)  # Replace with the size of your sprites
ss = SpriteSheet(filename, cellsize)
 
# Get a bunch of images from the sprite sheet
log = ss.compose_horiz([24, 25, 26])
alig = ss.compose_horiz([32, 33, 15])
frog_g = ss.image_at(4)
frog_p = ss.image_at(76)
fly = ss.image_at(57)


screen.blit(alig, grid[14])
# Scale in X and Y, bigger or smaller. 
alig3x = pygame.transform.scale(alig, (alig.get_width() * 3, alig.get_height() * 3))
screen.blit(alig3x, grid[15])

# Flip top to bottom
alig3x_hflip = pygame.transform.flip(alig3x, True, False)
screen.blit(alig3x_hflip, grid[19])

# Flip left to right. 
alig3x_vflip = pygame.transform.flip(alig3x, False, True)
screen.blit(alig3x_vflip, grid[23])

# 2x increase, without jagged edges. 
frog2x = pygame.transform.scale2x(frog_g)
screen.blit(frog2x, grid[42])

# Just scale normally by a factor
frog4x =  pygame.transform.scale_by(frog2x, 3)
screen.blit(frog4x, grid[43])

# Different scale in X and Y
frog_w = pygame.transform.scale(frog_g, (frog_g.get_width() * 6, frog_g.get_height() * 2))
screen.blit(frog_w, grid[45])

# Rotations. Notice that the frog seems to be moving down, this is 
# because we are rotating a rotated image, so any errors compound.
frog_p2x = pygame.transform.scale2x(frog_p)
for  i in range(5):
    frog_p2x = pygame.transform.rotate(frog_p2x, 30)
    screen.blit(frog_p2x, grid[70+(i*2)])
    

# Rotations. Here we always rotate the original image, to whatever angle, 
# so the image doesn't seem to stray. 
frog_p2x = pygame.transform.scale2x(frog_p)
for  i in range(5):
    frog_rot = pygame.transform.rotate(frog_p2x, 30*i)
    screen.blit(frog_rot, grid[112+(i*2)])



pygame.display.flip()


while True:
    e = pygame.event.wait()
    if e.type == pygame.QUIT:
            break
    pygame.time.Clock().tick(60)
pygame.quit()


