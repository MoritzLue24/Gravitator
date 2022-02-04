from os import stat
from VectorUtils.Vector import *
import pygame


def renderText(text: str, position: Vector2, font: pygame.font.Font, color: pygame.Color=(255, 255, 255)):
    text = font.render(text, 1, color)
    pygame.display.get_surface().blit(text, position.toTuple())


class Widget:
    instances = []
    color_active = pygame.Color(128, 128, 128)
    color_passive = pygame.Color(89, 89, 89)
    def __init__(self, position: Vector2, size: Vector2, description: str=''):
        self.position = position
        self.size = size
        self.description = description
        self.active = False
        self.padding = Vector2(4, 4)
        self.instances.append(self)

    @staticmethod
    def render(font: pygame.font.Font, font_color=(255, 255, 255)):
        for instance in Widget.instances:
            instance.render(font, font_color)

    @staticmethod
    def events(event: pygame.event.Event):
        for instance in Widget.instances:
            if (instance.events(event)):
                return True


class InputField(Widget):
    def __init__(self, position: Vector2, size: Vector2, description: str='', text: str=''):
        super().__init__(position, size, description)
        self.text = text

    def render(self, font, font_color=(255, 255, 255)):
        pygame.draw.rect(
            pygame.display.get_surface(), 
            self.color_active if self.active else self.color_passive, 
            (self.position.x, self.position.y, self.size.x, self.size.y), 
            border_radius=3)

        renderText(self.text, self.position + self.padding, font, font_color)
        renderText(self.description, Vector2(self.position.x, self.position.y - 20), font, font_color)

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

class Checkbox(Widget):
    def __init__(self, position: Vector2, size: Vector2, description: str=''):
        super().__init__(position, size, description)

    def render(self, font: pygame.font.Font, font_color=(255, 255, 255)):
        pygame.draw.rect(
            pygame.display.get_surface(), 
            self.color_active if self.active else self.color_passive, 
            (self.position.x, self.position.y, self.size.x, self.size.y), 
            border_radius=3)

        if self.active:
            pygame.draw.line(
                pygame.display.get_surface(), 
                font_color, 
                (self.position + self.padding).toTuple(), 
                (self.position + self.size - self.padding).toTuple(),
                width=3)

            pygame.draw.line(
                pygame.display.get_surface(), 
                font_color, 
                (self.position + Vector2(self.size.x - self.padding.x, self.padding.y)).toTuple(), 
                (self.position + Vector2(self.padding.x, self.size.y - self.padding.y)).toTuple(),
                width=3)

        renderText(self.description, Vector2(self.position.x, self.position.y - 20), font, font_color)

    def events(self, event: pygame.event):
        rect = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(pygame.mouse.get_pos()):
                self.active = not self.active
                return True
