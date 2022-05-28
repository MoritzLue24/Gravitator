import pygame
from VectorUtils import Vector2
from .widget import Widget
from .font import Font


class InputField(Widget):
    def __init__(self, **kwargs):
        '''
        Used to display an interactive text input field.

        Kw Args:
            * topleft (Vector2, optional=None) - If None, topleft is calculated using the DEFAULT_X and DEFAULT_Y_SPACING properties.
            * description (str, optional=None) - The description.
            * text (str) - The default text that can be edited.
            * min_width (int, optional=0) - The minimum width of the input (not description) field.
        '''

        super().__init__(kwargs.get('topleft', None))
        self.description = kwargs.get('description', None)
        self.text = kwargs.get('text')
        self.min_width = kwargs.get('min_width', 0)

        # A flag that indicates if the user has deselected the text field
        self.changed = False

        # Calculate the size of the boxes of both the description and the input text
        self.desc_size = Font.getRenderSize(self.description) + Widget.TEXT_MARGIN * 2
        text_size = Font.getRenderSize(self.text) + Widget.TEXT_MARGIN * 2
        self.text_size = text_size if text_size.x >= self.min_width else Vector2(self.min_width, text_size.y)


    def handleEvents(self, event: pygame.event.Event) -> bool:
        '''
        Handle the events of the input field.
        This function returns True if the event was handled, False otherwise.
        '''
        
        text_rect = pygame.Rect(
            self.surface.vertical_seperator + self.surface.topleft.x if self.description else self.topleft.x, 
            self.topleft.y + self.surface.topleft.y, 
            self.text_size.x, 
            self.text_size.y
        )

        # Reset the changed flag
        self.changed = False

        # Set instance.active to True if the user has clicked on the text field and False otherwise
        if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            if text_rect.collidepoint(pygame.mouse.get_pos()):
                # Set the changed flag to True if the user has deselected the text field
                self.changed = True
                self.active = not self.active
                return True

            else:
                self.changed = True
                if self.active:
                    self.active = False
                    return True

        # Handle the keyboard events
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.changed = True

            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            
            # Update the text size
            text_size = Font.getRenderSize(self.text) + Widget.TEXT_MARGIN * 2
            self.text_size = text_size if text_size.x >= self.min_width else Vector2(self.min_width, text_size.y)
            return True

        return False


    def render(self, surface: pygame.Surface=None):
        '''
        Render the text input field.
        '''
        
        # Calculate the description rect and the text rect
        text_rect = pygame.Rect(
            self.surface.vertical_seperator if self.description else self.topleft.x, 
            self.topleft.y, 
            self.text_size.x, 
            self.text_size.y
        )

        # Render the background
        # renderer.fill(desc_rect, sdl2.ext.Color(255, 20, 20))
        # renderer.fill(text_rect, sdl2.ext.Color(20, 20, 255))

        surf = self.surface if self.surface else surface

        pygame.draw.rect(surf, Widget.ACTIVE_COLOR if self.active else Widget.PASSIVE_COLOR, text_rect, 2)


        # Render the description
        Font.myRender(surf, self.description, self.topleft + Widget.TEXT_MARGIN)

        # Render the default text
        Font.myRender(surf, self.text, Vector2(text_rect[0], text_rect[1]) + Widget.TEXT_MARGIN)