import pygame
from .widget import Widget
from .font import Font


class Checkbox(Widget):
    def __init__(self, **kwargs):
        '''
        A input widget with a checked value of true or false

        Kw Args:
            * surface (Surface) - The parent surface.
            * topleft (Vector2, optional=None) - If None, topleft is calculated using the DEFAULT_X and DEFAULT_Y_SPACING properties.
            * description (str) - The description.
            * checked (bool, optional=False) - If True, the checkbox is checked.
        '''

        super().__init__(kwargs.get('surface'), kwargs.get('topleft', None))
        self.description = kwargs.get('description')
        self.checked = kwargs.get('checked', False)
    

    def handleEvents(self, event: pygame.event.Event) -> bool:
        '''
        Handle the events of the checkbox.
        This function returns True if the event was handled, False otherwise.
        '''
        box_size = Font.getRenderSize('a').y + Widget.MARGIN * 2
        rect = pygame.Rect(self.surface.topleft.x + self.surface.vertical_seperator, self.surface.topleft.y + self.topleft.y, box_size, box_size)

        if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            if rect.collidepoint(pygame.mouse.get_pos()):
                self.checked = not self.checked
                return True
        return False

    
    def draw(self):
        '''
        Draw the checkbox.
        '''
        
        # Draw the description
        self.surface.blit(Font.get().render(self.description, True, Font.get().color), (self.topleft + Widget.MARGIN).toTuple())

        box_size = Font.getRenderSize('a').y + Widget.MARGIN * 2

        # Draw a cross if the checkbox is checked
        if self.checked:
            pygame.draw.line(self.surface, Widget.ACTIVE_COLOR, 
                (self.surface.vertical_seperator + 2, self.topleft.y + 2),
                (self.surface.vertical_seperator + box_size - 2, self.topleft.y + box_size - 2), 2)
            pygame.draw.line(self.surface, Widget.ACTIVE_COLOR, 
                (self.surface.vertical_seperator + box_size - 2, self.topleft.y + 2),
                (self.surface.vertical_seperator + 2, self.topleft.y + box_size - 2), 2)
        
        # Draw the checkbox
        pygame.draw.rect(self.surface, Widget.PASSIVE_COLOR, pygame.Rect(self.surface.vertical_seperator, self.topleft.y, box_size, box_size), 2)
