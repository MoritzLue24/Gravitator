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
            * surface (Surface) - The parent surface.
            * topleft (Vector2, optional=None) - If None, topleft is calculated using the DEFAULT_X and DEFAULT_Y_SPACING properties.
            * size (Vector2, optional=None) - If None, size is calculated using the Widget.MARGIN and text size.
            * description (str) - The description.
            * on_click (function) - The function to call when the button is clicked.
        '''

        super().__init__(kwargs.get('surface'), kwargs.get('topleft', None))
        self.size = kwargs.get('size', None)
        self.description = kwargs.get('description')
        self.on_click = kwargs.get('on_click')
        self._clicked_time = None


    def handleEvents(self, event: pygame.event.Event) -> bool:
        '''
        Handle the events of the button.
        This function returns True if the event was handled, False otherwise.
        '''
        rect = pygame.Rect((self.surface.topleft + self.topleft).toTuple(), self.size.toTuple())
        
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

        # Draw the description so it is always in the middle of the button
        font_surface = Font.get().render(self.description, True, Font.get().color)
        font_size = Vector2(font_surface.get_width(), font_surface.get_height())
        self.surface.blit(font_surface, (self.topleft + (self.size - font_size) / 2).toTuple())

        # Draw the button
        pygame.draw.rect(self.surface, Widget.ACTIVE_COLOR if self.active else Widget.PASSIVE_COLOR, self.topleft.combineToList(self.size), 2)
