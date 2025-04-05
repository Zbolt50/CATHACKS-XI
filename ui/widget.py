import math
import pygame

class Button:
    DEBUG_DRAGGABLE = True

    text_font = None

    def __init__(self, x, y, width, height):
        if Button.text_font is None:
            Button.text_font = pygame.font.Font("./assets/fonts/Ac437_IBM_VGA_8x16.ttf", 32)

        self.rect = pygame.rect.Rect(x, y, width, height)
        self.surf = pygame.surface.Surface((width, height))
        self.color = pygame.color.Color((255, 255, 255, 255))

        self.display_tooltip = False
        self.tiptext = ""
        self.tiptextsurface = Button.text_font.render(self.tiptext, False, (232, 232, 232), (0, 0, 0))

        self.damp = 0
        self.callback = None
        self.timer = 0
    def update(self, dt):
        self.timer += dt
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.display_tooltip = True
            if pygame.mouse.get_pressed()[0]:
                self.damp = 2

                if Button.DEBUG_DRAGGABLE:
                    mouse_pos = list(pygame.mouse.get_pos())
                    mouse_pos[0] = math.floor(mouse_pos[0] / 16) * 16
                    mouse_pos[1] = math.floor(mouse_pos[1] / 16) * 16
                    self.rect = pygame.rect.Rect(mouse_pos[0] - self.rect.width / 2, mouse_pos[1] - self.rect.height / 2, self.rect.width, self.rect.height)
            else:
                self.damp = 1

            if pygame.mouse.get_just_released()[0]:
                if self.callback is not None and not Button.DEBUG_DRAGGABLE:
                    self.callback()
        else:
            self.damp = 0
            self.display_tooltip = False

        if Button.DEBUG_DRAGGABLE and self.timer > 1.0:
            print("DEBUG: rectangle: " + str(self.rect))
            self.timer = 0

    def render(self, display=pygame.display.get_surface()):
        # render text

        new_color = self.color.lerp("black", 0.3 * self.damp)
        self.surf.fill(new_color)
        display.blit(self.surf, self.rect)
        if len(self.tiptext) != 0 and self.display_tooltip:
            mouse_pos = list(pygame.mouse.get_pos())
            mouse_pos[0] = math.floor(mouse_pos[0] / 32) * 32
            mouse_pos[1] = math.floor(mouse_pos[1] / 32) * 32
            display.blit(self.tiptextsurface, (mouse_pos[0], mouse_pos[1]))
    '''Set hover text in this button.
    Make sure to use this; it re-bakes the surface so it displays an updated render
    '''
    def set_text(self, text):
        self.tiptext = text
        self.tiptextsurface = Button.text_font.render(self.tiptext, False, (232, 232, 232), (0, 0, 0))
