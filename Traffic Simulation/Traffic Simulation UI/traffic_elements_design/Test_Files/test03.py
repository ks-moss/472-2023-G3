import pygame
import math

pygame.init()

# Set up the display
screen = pygame.display.set_mode((500, 500))

# Define the arch parameters
center_x = 250
center_y = 250
radius = 200

# Set up the object
obj_radius = 20
obj_color = (0, 0, 255)
obj_x = center_x + radius
obj_y = center_y

# Set up the speed control
speed = 0.05  # radians per frame
speed_increment = 0.01

# Run the game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                speed += speed_increment
            elif event.key == pygame.K_DOWN:
                speed -= speed_increment

    # Calculate the new object position
    angle = speed * pygame.time.get_ticks() / 1000  # calculate the angle based on time
    obj_x = center_x + radius * math.cos(angle)
    obj_y = center_y + radius * math.sin(angle)

    # Draw the objects
    screen.fill((255, 255, 255))  # clear the screen
    pygame.draw.circle(screen, obj_color, (int(obj_x), int(obj_y)), obj_radius)  # draw the object

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
