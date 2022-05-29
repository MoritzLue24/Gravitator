import pygame
from VectorUtils import Vector2
from .font import Font


class Widget:
    instances = []
    MARGIN = 5
    ACTIVE_COLOR = (150, 150, 150)
    PASSIVE_COLOR = (45, 75, 123)
    DEFAULT_X = 10
    DEFAULT_Y_SPACING = 10

    def __init__(self, surface, topleft: Vector2 | None):
        '''
        The widget class is the base class for all widgets.

        Args:
            * surface (Surface) - The parent surface.
            * topleft (Vector2, optional=None) - If None, topleft is calculated using the DEFAULT_X and DEFAULT_Y_SPACING properties.
        '''

        self.surface = surface
        self.active = False

        # Get the topleft position
        if topleft != None:
            self.topleft = topleft
        else:
            self.topleft = Vector2(Widget.DEFAULT_X, Widget.DEFAULT_Y_SPACING + len(surface.widgets) * (Widget.DEFAULT_Y_SPACING + Font.getRenderSize('a').y + Widget.MARGIN * 2))

        self.surface.widgets.append(self)
        Widget.instances.append(self)
    

    @staticmethod
    def oneActive() -> bool:
        '''
        Return True if there is atleast one widget active.
        '''
        return any(widget.active for widget in Widget.instances)


    def handleEvents(self, event: pygame.event.Event) -> bool:
        '''
        Handle the events of a widget.
        This function returns True if the event was handled, False otherwise.
        '''
        return False


    def draw(self):
        '''
        Draws the widget. The offset is the topleft position of parent surface.
        '''
        pass
