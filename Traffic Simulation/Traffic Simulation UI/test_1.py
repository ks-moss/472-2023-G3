import pygame
import sys
import math

pygame.init()

# Set up the game window
width = 640
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Object")

# Set up the object's starting position and velocity along the straight line
object_x = 0
object_y = height // 2
object_speed = 5

# Set up the object's starting position and velocity along the arc line
arc_rect = pygame.Rect(100, 100, 200, 200)
arc_center = (arc_rect.centerx, arc_rect.centery)
arc_radius = arc_rect.width // 2
arc_angle = math.pi / 2
arc_speed = 0.05

# Set up the game clock and frame rate
clock = pygame.time.Clock()
FPS = 60

# Create the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    # Move the object along the straight line
    if object_x < arc_rect.left:
        object_x += object_speed
    else:
        # Move the object along the arc line
        arc_angle -= arc_speed
        object_x = arc_center[0] + arc_radius * math.cos(arc_angle)
        object_y = arc_center[1] + arc_radius * math.sin(arc_angle)
    
    # Clear the screen
    screen.fill((255, 255, 255))
    
    # Draw the arc
    pygame.draw.arc(screen, (255, 0, 0), arc_rect, math.pi / 2, 0, 5)
    
    # Draw the object
    pygame.draw.circle(screen, (0, 0, 255), (int(object_x), int(object_y)), 10)
    
    # Update the display
    pygame.display.update()
    
    # Delay to control the frame rate
    clock.tick(FPS)
