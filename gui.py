from VectorUtils.Vector import *
import pygame


def renderText(text: str, position: Vector2, font: pygame.font.Font, color: pygame.Color=(255, 255, 255)):
    text = font.render(text, 1, color)
    pygame.display.get_surface().blit(text, position.toTuple())


class InputField:
    color_active = pygame.Color(128, 128, 128)
    color_passive = pygame.Color(89, 89, 89)
    def __init__(self, position: Vector2, size: Vector2, text: str=""):
        self.position = position
        self.size = size

        self.text = text
        self.active = False
        self.padding = Vector2(4, 4)

    def draw(self, font, font_color=(255, 255, 255)):
        rect = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
        pygame.draw.rect(
            pygame.display.get_surface(), 
            self.color_active if self.active else self.color_passive, 
            rect, 
            border_radius=3)

        text_surf = font.render(self.text, True, font_color)
        pygame.display.get_surface().blit(
            text_surf, 
            (rect.x + self.padding.x, 
            rect.y + self.padding.y))

    def events(self, event: pygame.event):
        rect = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(pygame.mouse.get_pos()):
                self.active = not self.active
                return True
            else:
                self.active = False

        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                return True
        return False
