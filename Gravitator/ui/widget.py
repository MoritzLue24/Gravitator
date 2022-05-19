import pygame
from VectorUtils import Vector2


class Widget:
    instances = []
    def __init__(self, topleft: Vector2):
        '''
        This is a base class for all widgets.
        Do not use this class directly but the static methods can be called.
        '''
        self.topleft = topleft
        self.active = False
        Widget.instances.append(self)

    def event_handler(self, event: pygame.event.Event) -> bool:
        return False

    @staticmethod
    def oneActive() -> bool:
        '''
        Returns True if there is at least one widget active.
        '''
        for instance in Widget.instances:
            if instance.active:
                return True
        return False


    @staticmethod
    def events_all(event: pygame.event.Event) -> bool:
        '''
        The event handler has to be called once inside the event loop.
        '''
        # Events for the InputFields
        smth_clicked = False

        for instance in Widget.instances:
            if instance.event_handler(event):
                smth_clicked = True

        return smth_clicked


    @staticmethod
    def draw_all():
        '''
        Draws every widget.
        '''
        for instance in Widget.instances:
            instance.draw()