import pygame

class Button_Design(pygame.sprite.Sprite):
    def __init__(self, surface, text, text_style, text_size, x, y, width, height, border_radius, text_color, text_color_mouse_pos, bg, bg_color_mouse_pos):
        self.surface = surface
        self.text = text
        self.text_style = text_style
        self.text_size = text_size
        self.rect = pygame.Rect(x, y, width, height)
        self.border_radius = border_radius

        self.main_text_color = text_color
        self.text_color = text_color
        self.text_color_mouse_pos = text_color_mouse_pos

        self.main_bg_color = bg
        self.bg_color = bg
        self.bg_color_mouse_pos = bg_color_mouse_pos

    def draw_button(self):
        pygame.draw.rect(self.surface, self.main_bg_color, self.rect, border_radius=self.border_radius)
        font = pygame.font.SysFont(self.text_style, self.text_size)
        text = font.render(self.text, 1, self.main_text_color)
        text_pos = text.get_rect(center=self.rect.center)
        self.surface.blit(text, text_pos)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                self.main_text_color = self.text_color_mouse_pos
                self.main_bg_color = self.bg_color_mouse_pos
            else:
                self.main_text_color = self.text_color
                self.main_bg_color = self.bg_color
        else:
            self.main_text_color = self.text_color
            self.main_bg_color = self.bg_color
        self.draw_button()

