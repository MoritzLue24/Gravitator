import pygame
from VectorUtils import Vector2
from .widget import Widget
from .font import Font
from .text import Text


class Surface(pygame.Surface):
    BG_COLOR = (20, 20, 20)
    instances = []
    def __init__(self, topleft: Vector2, size: Vector2, vertical_seperator: int, bg_color: pygame.Color=BG_COLOR):
        '''
        The surface is used as a parent for widgets, that can be added via the addWidget() method.

        Args:
            * topleft (Vector2) - The topleft position of the surface.
            * size (Vector2) - The size of the surface.
            * vertical_seperator (int) - The x position of the vertical seperator, where the description and the widgets are seperated.
            * bg_color (pygame.Color, optional=Surface.BG_COLOR) - The background color of the surface.
        '''

        # Initialize the superclass (sdl2.SDL_Rect)
        super().__init__((size.x, size.y))
        self.topleft = topleft
        self.size = size
        self.vertical_seperator = vertical_seperator
        self.bg_color = bg_color

        # The widgets inside this surface
        self.widgets = []

        Surface.instances.append(self)

    
    def addWidget(self, widget: Widget) -> Widget:
        '''
        Add a widget to the surface. Returns the widget
        '''
        widget.surface = self
        self.widgets.append(widget)
        return widget

    
    @staticmethod
    def handleEvents(event: pygame.event.Event) -> bool:
        '''
        Handle events for all widgets on all surfaces. Returns True if the event was handled.
        '''

        event_handled = False

        # Handle events for all widgets
        for surface in Surface.instances:
            for widget in surface.widgets:
                if widget.handleEvents(event):
                    event_handled = True
            if pygame.Rect(surface.topleft.combineToList(surface.size)).collidepoint(pygame.mouse.get_pos()):
                event_handled = True
        
        return event_handled


    def render(self):
        '''
        Render all widgets and the surface
        '''

        # Render the background rect
        self.fill(self.bg_color)

        # Render all widgets
        for widget in self.widgets:
            widget.render()

        pygame.display.get_surface().blit(self, self.topleft.toTuple())