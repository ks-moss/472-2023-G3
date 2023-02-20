import pygame

class Traffic_Light_Design(pygame.sprite.Sprite):
    def __init__(self, surface, x, y, width, height): 
        # light_signal = (0 | 1 | 2 | 3 | 4) Note that: 0 = red, 1 = yellow, 2 = green, 3 = default, 4 = gray
        self.surface = surface
        self.rect = pygame.Rect(x, y, width, height)

        self.default_light_color = "#303030"
        self.default_top_light = 'red'
        self.default_center_light = 'yellow'
        self.default_bottom_light = 'green'

        self.top_light = 'red'
        self.center_light = 'yellow'
        self.bottom_light = 'green'
        

    def draw_traffic_light(self):
        rec = pygame.draw.rect(self.surface, 'black', self.rect, border_radius=20)

        # Calculate the center points of the three circles
        circle_x1, circle_y1 = rec.left + 15, rec.top + 13
        circle_x2, circle_y2 = rec.centerx, rec.centery
        circle_x3, circle_y3 = rec.right - 15, rec.bottom - 13

        # Draw the three circles
        pygame.draw.circle(self.surface, self.top_light, (circle_x1, circle_y1), 8)
        pygame.draw.circle(self.surface, self.center_light, (circle_x2, circle_y2), 8)
        pygame.draw.circle(self.surface, self.bottom_light, (circle_x3, circle_y3), 8)


    def update_signal_light(self, signal_light):
  
        if signal_light == 0: # RED
            self.center_light = self.default_light_color
            self.bottom_light = self.default_light_color
            # Crisis part: assign red color
            self.top_light = self.default_top_light
            

        if signal_light == 1: # YELLOW
            self.top_light = self.default_light_color
            self.bottom_light = self.default_light_color
            # Crisis part: assign yellow color
            self.center_light = self.default_center_light
        

        if signal_light == 2: # GREEN
            self.top_light = self.default_light_color
            self.center_light = self.default_light_color
            # Crisis part: assign green color
            self.bottom_light = self.default_bottom_light
        
        if signal_light == 3: # DEFAULT
            self.top_light = self.default_top_light
            self.center_light = self.default_center_light
            self.bottom_light = self.default_bottom_light

        if signal_light == 4: # GRAY
            self.top_light = self.default_light_color
            self.center_light = self.default_light_color
            self.bottom_light = self.default_light_color

        


    def update(self):
        self.draw_traffic_light()



            
       