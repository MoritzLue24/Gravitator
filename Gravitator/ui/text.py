import pygame
from VectorUtils import Vector2
from .widget import Widget
from .font import Font


class Text(Widget):
    def __init__(self, **kwargs):
        '''
        Used to display simple text on a surface.

        Kw Args:
            * topleft (Vector2, optional=None) - If None, topleft is calculated using the DEFAULT_X and DEFAULT_Y_SPACING properties.
            * text (str) - The text to be displayed.
            * underlined (bool, optional=True) - If True, underlines the text.
        '''

        super().__init__(kwargs.get('topleft', None))
        self.text = kwargs.get('text')
        self.underlined = kwargs.get('underlined', True)

    
    def draw(self):
        '''
        Draws the text using the static ui.Font.draw method.
        '''

        # Draw the text
        Font.draw(self.surface, self.text, self.topleft + Widget.TEXT_MARGIN)

        # Draw underline if widget.underlined
        if self.underlined:
            height = Font.getRenderSize(self.text).y + Widget.TEXT_MARGIN * 2
            a = Vector2(self.topleft.x, self.topleft.y + height)
            b = self.topleft + Vector2(self.surface.size.x - self.topleft.x * 2, height)
            pygame.draw.line(self.surface, (255, 255, 255), a.toTuple(), b.toTuple())