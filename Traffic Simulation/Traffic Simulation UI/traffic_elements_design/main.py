import pygame
import sys
from ButtonDesign import *
from TrafficLightDesign import *
from RoadDesign import *

class Game:
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.button_rect = Button_Design(self.screen, "Button", 'comicsans', 25, 350, 250, 100, 40, 20, 'white',  'black', 'black', 'white')  
        # ^--- Button_Design(surface, text, text_style, text_size, x, y, width, height, border_radius, text_color, text_color_mouse_pos, bg, bg_color_mouse_pos)
        self.traffic_light_N = Traffic_Light_Design(self.screen, 500, 300, 30, 65)
        # ^--- Traffic_Light_Design(surface, x, y, width, height, light_signal)
        self.road_Y = Road_Design(self.screen, 50, 50, 3, 'Y')
        # ^--- Road_Design(surface, x, y, road_length)
        self.road_X = Road_Design(self.screen, 73, 50, 3, 'X')
        # ^--- Road_Design(surface, x, y, road_length)
        

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.button_rect.rect.collidepoint(mouse_pos):
                        print("Clicked!!")

            self.screen.fill('#303030')
            self.button_rect.update()
            self.traffic_light_N.update()
            self.road_Y.update()
            self.road_X.update()
        
            #self.traffic_light_N.update_signal_light(0)
            #self.traffic_light_N.update_signal_light(1)
            #self.traffic_light_N.update_signal_light(2)
            self.traffic_light_N.update_signal_light(3)         
            #self.traffic_light_N.update_signal_light(4)

            

            pygame.display.update()

            clock.tick(60)
    
            

if __name__ == '__main__':
    game = Game()
    game.run()
    
