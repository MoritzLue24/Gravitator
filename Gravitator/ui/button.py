import pygame
from VectorUtils import Vector2
from .widget import Widget
from .font import Font


class Button(Widget):
    ANIMATION_DURATION = 100  # In milliseconds
    def __init__(self, **kwargs):
        '''
        A button widget.

        Kw Args:
            * topleft (Vector2, optional=None) - If None, topleft is calculated using the DEFAULT_X and DEFAULT_Y_SPACING properties.
            * description (str) - The description.
            * on_click (function) - The function to call when the button is clicked.
            * margin (Vector2, optional=Widget.TEXT_MARGIN) - The margin between the button and the description.
        '''

        super().__init__(kwargs.get('topleft', None))
        self.description = kwargs.get('description')
        self.on_click = kwargs.get('on_click')
        self.margin = kwargs.get('margin', Vector2(Widget.TEXT_MARGIN, Widget.TEXT_MARGIN))
        self._clicked_time = None


    def handleEvents(self, event: pygame.event.Event) -> bool:
        '''
        Handle the events of the button.
        This function returns True if the event was handled, False otherwise.
        '''
        rect = pygame.Rect(self.topleft.toTuple(), (Font.getRenderSize(self.description) + self.margin * 2).toTuple())

        if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            if rect.collidepoint(pygame.mouse.get_pos()):
                self._clicked_time = pygame.time.get_ticks()
                self.active = True
                self.on_click()
                return True
        return False


    def draw(self):
        '''
        Draw the button.
        '''

        # Update the animation
        if self._clicked_time is not None:
            if pygame.time.get_ticks() - self._clicked_time >= Button.ANIMATION_DURATION:
                self._clicked_time = None
                self.active = False

        # Draw the description
        Font.draw(self.surface, self.description, self.topleft + self.margin)

        # Draw the button
        pygame.draw.rect(self.surface, Widget.ACTIVE_COLOR if self.active else Widget.PASSIVE_COLOR, 
            pygame.Rect(self.topleft.toTuple(), (Font.getRenderSize(self.description) + self.margin * 2).toTuple()), 2)