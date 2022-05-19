import pygame
from VectorUtils import Vector2
from ui.widget import Widget
from ui.config import *


class Checkbox(Widget):
    def __init__(self, topleft: Vector2, size: Vector2, checked: bool=False):
        '''
        This class is used to take boolean type input from the user.
        It is recommended to create an instance of this class only inside the ui class
        '''
        super().__init__(topleft)
        self.size = size
        self.checked = checked


    def event_handler(self, event: pygame.event.Event) -> bool:
        '''
        The event handler has to be called once inside the event loop.
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(self.topleft.x, self.topleft.y, self.size.x, self.size.y).collidepoint(pygame.mouse.get_pos()):
                self.checked = not self.checked
                return True
        return False

    
    def draw(self):
        '''
        The draw method has to be called once per frame.
        '''

        # Draw the checkbox
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.topleft.x, self.topleft.y, self.size.x, self.size.y))