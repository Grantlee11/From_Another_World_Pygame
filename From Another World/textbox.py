import pygame.font

class TextBox():

    def __init__(self, screen, msg, y):
        """INTIALIZE TEXTBOX ATTRIBUTES"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # SET THE DIMENSIONS AND PROPERTIES OF THE TEXTBOX
        self.width, self.height = 1200, 80
        self.button_color = (0, 255, 100)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        # BUILD THE TEXTBOX RECT OBJECT AND CENTER IT
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = y

        self.prep_msg(msg)


    def prep_msg(self, msg):
        """CREATE AND CENTER RENDERED IMAGE IN TEXTBOX"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # DRAW BLANK TEXTBOX AND THEN DRAW THE IMAGE
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)