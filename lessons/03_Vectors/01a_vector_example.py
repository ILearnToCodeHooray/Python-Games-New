
import pygame
import math

from jtlgames.vector20 import Vector20Factory

# Initialize pygame
pygame.init()

# Screen setup
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Vector with Arrow")

# Create a new Vector20 class with customized screen size and scale
Vector20, draw_v20, draw_grid = Vector20Factory(screen_width, screen_height, 20)
draw_grid(screen)

# Create some vectors
v0 = Vector20(5,5)
v1 = Vector20(0, 1)  

v1scaled = v1 * 10

v1rotated = v1scaled.rotate(90)

start = draw_v20(screen, v0, v1rotated)
v2 = v1rotated.rotate(90)
v3 = v2.rotate(90)
v4 = v3.rotate(90)
start = draw_v20(screen, start, v2)
start = draw_v20(screen, start, v3)
start = draw_v20(screen, start, v4)
# Update display
pygame.display.flip()

# Game loop, just pausing so you can see the screen. 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit pygame
pygame.quit()
