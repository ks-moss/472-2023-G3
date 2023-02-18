import pygame
import pygame_gui
import sys
import os



#  Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Display Constants
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
MANAGER = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Traffic Simulation')



# ---------- Shortcut Create Text Label ----------
# Function for creating text labels
def Create_Text(text, front, size, fg, X, Y):
    font = pygame.font.SysFont(front, size)
    img = font.render(text, True, fg)
    SCREEN.blit(img, (X, Y))


# ---------- Shortcut Create Button ----------
# Function for creating buttons
def Create_Button(text, position, size, manager, object_id):
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(position, size),
        text=text,
        manager=manager,
        object_id=object_id
    )
    return button



# ---------- Assign Header Image ----------
# load the image
image_path = os.path.join('image', '/Users/krisadasinamkam/Desktop/CS 472/Traffic Simulation UI/Images/traffic-header-image.png')
image = pygame.image.load(image_path).convert_alpha()
# scale the image down to 20.5% of its original size
HEADER_IMAGE_SCALE_FACTOR = 0.205
scaled_image = pygame.transform.scale(image, (int(image.get_width()*HEADER_IMAGE_SCALE_FACTOR), int(image.get_height()*HEADER_IMAGE_SCALE_FACTOR)))

# ---------- Assign Backgrounds ----------
# Backgroung Right Frame
background_right = pygame.Surface((250, SCREEN_HEIGHT-int(image.get_height()*HEADER_IMAGE_SCALE_FACTOR)))
background_right.fill(pygame.Color('#d4d4d4'))


# ---------- Create Buttons ----------
exit_button = Create_Button('Exit', (1135, 770), (60, 25), MANAGER, object_id='exit_button')   # (X,Y), (weiwidth, height)
start_button = Create_Button('Start', (970, 600), (70, 25), MANAGER, object_id='start_button')   # (X,Y), (weiwidth, height)
reset_button = Create_Button('Reset', (1100, 600), (70, 25), MANAGER, object_id='reset_button')   # (X,Y), (weiwidth, height)



# Car 1 start spot and speed
rect_car1_x = 20
rect_car1_vel = 10

# Car 1 start spot and speed
rect_car2_x = 900
rect_car2_vel = 5



# ---------- Loop to keep the main window staying active ----------
clock = pygame.time.Clock()
FPS = 60
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        # If user click on [X], then terminate the window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == exit_button:
                    is_running = False
                if event.ui_element == start_button:
                    print("Start!")
                if event.ui_element == reset_button:
                    print("Reset Requested!")
                

        MANAGER.process_events(event)
    MANAGER.update(time_delta)


    # ---------- Everything after this line will be displayed on the screen ----------
    # Default Background
    SCREEN.fill(pygame.Color('#303030'))
    # Header Image
    SCREEN.blit(scaled_image, (0, 0))
    # Center Right Frame
    SCREEN.blit(background_right, (950, int(image.get_height()*HEADER_IMAGE_SCALE_FACTOR)))
    # Texts
    Create_Text('BZ Traffic', 'didot.ttc', 30, 'white', 20, 20)
    Create_Text('Traffic Output', 'didot.ttc', 25, 'black', 960, 65)

    # Drawing Rectangle
    center_right_textbox = pygame.draw.rect(SCREEN, 'white', pygame.Rect(960, (int(image.get_height() * HEADER_IMAGE_SCALE_FACTOR) + 35), 230, 500), border_radius=10)  # pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)
    Create_Text('Time 0', 'arial.ttc', 20, 'black', 970, 110)
    Create_Text('Vehicle 1', 'arial.ttc', 20, 'black', 970, 125)
    Create_Text('   -> road: Rochelle', 'arial.ttc', 20, 'black', 970, 140)
    Create_Text('   -> position: 20', 'arial.ttc', 20, 'black', 970, 155)
    Create_Text('   -> speed: 16.6', 'arial.ttc', 20, 'black', 970, 170)

    Create_Text('Vehicle 2', 'arial.ttc', 20, 'black', 970, 200)
    Create_Text('   -> road: Rochelle', 'arial.ttc', 20, 'black', 970, 215)
    Create_Text('   -> position: 0', 'arial.ttc', 20, 'black', 970, 230)
    Create_Text('   -> speed: 16.6', 'arial.ttc', 20, 'black', 970, 245)

    simulator_background = pygame.draw.rect(SCREEN, '#d4fc9f', pygame.Rect(5, 62, 940, 735), border_radius=10)  # pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)
    road_X = pygame.draw.rect(SCREEN, '#6b6b6a', pygame.Rect(20, 380, 900, 100), border_radius=10)  # pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)
    road_Y = pygame.draw.rect(SCREEN, '#6b6b6a', pygame.Rect(420, 70, 100, 720), border_radius=10)  # pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)

    yellow_line_N = pygame.draw.rect(SCREEN, '#ffd000', pygame.Rect(467, 70, 5, 300), border_radius=10)  # pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)
    yellow_line_S = pygame.draw.rect(SCREEN, '#ffd000', pygame.Rect(467, 490, 5, 300), border_radius=10)  # pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)
    yellow_line_E = pygame.draw.rect(SCREEN, '#ffd000', pygame.Rect(525, 427, 395, 5), border_radius=10)  # pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)
    yellow_line_W = pygame.draw.rect(SCREEN, '#ffd000', pygame.Rect(20, 427, 395, 5), border_radius=10)  # pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)

    white_line_N = pygame.draw.rect(SCREEN, 'white', pygame.Rect(420, 367, 50, 5), border_radius=10)  # pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)
    white_line_S = pygame.draw.rect(SCREEN, 'white', pygame.Rect(470, 490, 50, 5), border_radius=10)  # pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)
    white_line_E = pygame.draw.rect(SCREEN, 'white', pygame.Rect(525, 380, 5, 50), border_radius=10)  # pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)
    white_line_W = pygame.draw.rect(SCREEN, 'white', pygame.Rect(410, 430, 5, 50), border_radius=10)  # pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)

    light_N = pygame.draw.rect(SCREEN, 'red', pygame.Rect(400, 350, 15, 15), border_radius=10)  # pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)
    light_E = pygame.draw.rect(SCREEN, 'red', pygame.Rect(525, 490, 15, 15), border_radius=10)  # pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)
    light_E = pygame.draw.rect(SCREEN, 'red', pygame.Rect(530, 360, 15, 15), border_radius=10)  # pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)
    light_W = pygame.draw.rect(SCREEN, 'green', pygame.Rect(400, 485, 15, 15), border_radius=10)  # pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)
    
   # Update the rectangle's position
    rect_car1_x += rect_car1_vel
   # rect_car2_x -= rect_car2_vel

    if(rect_car1_x >= 899):
        rect_car1_x = 20


    # if(rect_car2_x == 20):
       # rect_car2_x = 900


    car_1 = pygame.draw.rect(SCREEN, 'blue', (rect_car1_x, 445, 30, 15), border_radius=10) # draw the rectangle
    car_2 = pygame.draw.rect(SCREEN, 'blue', (530, 400, 30, 15), border_radius=10) # draw the rectangle


    # ---------- Update to the screen ----------
    MANAGER.draw_ui(SCREEN)
    pygame.display.update()

    # Delay to control the frame rate
    clock.tick(FPS)



pygame.quit()
sys.exit()
