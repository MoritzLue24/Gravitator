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

    
    def render(self):
        '''
        Render the text using the static ui.Font.render method.
        '''

        #rect = (self.topleft + Vector2(self.surface.x, self.surface.y)).combineToList(Font.getRenderSize(self.text) + Widget.TEXT_MARGIN * 2)
        #renderer.draw_rect(rect, Widget.ACTIVE_COLOR if self.active else Widget.PASSIVE_COLOR)

        # Render the text
        Font.myRender(self.surface, self.text, self.topleft + Widget.TEXT_MARGIN)

        # Render underline if widget.underlined
        if self.underlined:
            height = Font.getRenderSize(self.text).y + Widget.TEXT_MARGIN * 2
            a = Vector2(self.topleft.x, self.topleft.y + height)
            b = self.topleft + Vector2(self.surface.size.x - self.topleft.x * 2, height)
            pygame.draw.line(self.surface, (255, 255, 255), a.toTuple(), b.toTuple())