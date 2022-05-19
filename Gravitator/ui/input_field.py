import pygame
from VectorUtils import Vector2
from config import *
from .widget import Widget
from .config import *


class InputField(Widget):
    def __init__(self, topleft: Vector2, text: str, description: str=''):
        '''
        This class is used to take input from the user.
        It is recommended to create an instance of this class only inside the ui class
        '''
        super().__init__(topleft)

        self.description = description
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

        # The text the user has entered
        self.text = text
        
        # A flag that indicates if the user has deselected the text field
        self.changed = False

        # Calculate the size of the text surface and store it in self.size
        self.size = Vector2.fromTuple(self.font.size(self.description + ' ' + self.text)) + TEXT_MARGIN

    def event_handler(self, event: pygame.event.Event) -> bool:
        '''
        The event handler has to be called once inside the event loop.
        '''
        rect = pygame.Rect(self.topleft.combineToList(self.size))

        # Reset the changed flag
        self.changed = False

        # Set instance.highlighted to True if the user has clicked on the text field and False otherwise
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(pygame.mouse.get_pos()):
                # Set the changed flag to True if the user has deselected the text field
                if self.active:
                    self.changed = True

                self.active = not self.active
                return True

            else:
                self.changed = True
                if self.active:
                    self.active = False
                    return True

        # Set the input field to inactive if the user has clicked enter
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if not self.active: pass
            
            self.active = False
            self.changed = True
            return True

        # If the user has highlighted the text field, add the typed character to the text field
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            return True

        return False

    
    def draw(self):
        '''
        The draw method has to be called once per frame.
        '''
        surface = pygame.display.get_surface()

        # Update the size
        self.size.x = self.font.size(self.description + ' ' + self.text)[0] + TEXT_MARGIN.x * 2
        rect = self.topleft.combineToList(self.size)

        # Draw background
        pygame.draw.rect(surface, PASSIVE_COLOR, rect, 2)
        if self.active:
            pygame.draw.rect(surface, ACTIVE_COLOR, rect, 2)

        # Draw text
        text = self.font.render(self.description + ' ' + self.text, True, FONT_COLOR)
        surface.blit(text, (self.topleft + TEXT_MARGIN / 2).toTuple())