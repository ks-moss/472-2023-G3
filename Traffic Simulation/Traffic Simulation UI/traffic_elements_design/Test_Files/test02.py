import pygame

# initialize Pygame
pygame.init()

# define screen dimensions
screen_width = 800
screen_height = 600

# create screen
screen = pygame.display.set_mode((screen_width, screen_height))

# define rectangle dimensions and colors
rect_width = 100
rect_height = 50
rect_color = (255, 255, 255)
road_color = (128, 128, 128)

# define initial position of the first rectangle
x = 100
y = 100

# create multiple rectangles using for loop
for i in range(5):
    # draw rectangle
    pygame.draw.rect(screen, rect_color, pygame.Rect(x, y, rect_width, rect_height))
    # draw road
    pygame.draw.rect(screen, road_color, pygame.Rect(x, y + rect_height, rect_width, 10))
    # update position for the next rectangle
    x += rect_width
    y += 10

# update screen
pygame.display.flip()

# main loop
running = True
while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# quit Pygame
pygame.quit()
