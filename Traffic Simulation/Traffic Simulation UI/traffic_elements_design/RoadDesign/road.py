import pygame

class Road_Design(pygame.sprite.Sprite):
    def __init__(self, surface, x, y, road_length, road_XY): 
        
        self.surface = surface
        self.road_length = road_length

        self.road_color = 'gray'
        self.yellow_line_color = 'yellow'
        self.white_line_color = 'white'
        
        self.x = x
        self.y = y
        self.road_XY = road_XY

    
        

    def draw_road_X(self):
        if self.road_XY == 'X':
            move_X = self.x

            for i in range(self.road_length):
                
                rect = pygame.draw.rect(self.surface, self.road_color, pygame.Rect(move_X, self.y, 100, 50))
                pygame.draw.rect(self.surface, self.yellow_line_color, pygame.Rect(move_X, (rect.centery-2), 100, 3))

                move_X += 100


    def draw_road_Y(self):
        if self.road_XY == 'Y':
            move_Y = self.y

            for i in range(self.road_length):
                
                rect = pygame.draw.rect(self.surface, self.road_color, pygame.Rect(self.x, move_Y, 50, 100))
                pygame.draw.rect(self.surface, self.yellow_line_color, pygame.Rect((rect.centerx-2), move_Y, 3, 100))

                move_Y += 100
         


    def update(self):
        self.draw_road_X()
        self.draw_road_Y()



            
       