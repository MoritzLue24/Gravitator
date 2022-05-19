import pygame
from VectorUtils import Vector2
from .widget import Widget
import config as cfg


class Text(Widget):
    def __init__(self, topleft: Vector2, text: str):
        '''
        This class is used to display text on the screen.
        It is recommended to create an instance of this class only inside the ui class
        '''
        super().__init__(topleft)

        self.text = text
        self.font = pygame.font.Font(cfg.FONT_PATH, cfg.FONT_SIZE)

        # Calculate the size of the text surface and store it in self.size
        self.size = Vector2.fromTuple(self.font.size(self.text)) + cfg.TEXT_MARGIN * 2


    def draw(self):
        '''
        This method is called once per frame.
        It loops through all instances and calls the draw method.
        '''
        surface = pygame.display.get_surface()

        # Update the size
        self.size = Vector2.fromTuple(self.font.size(self.text)) + cfg.TEXT_MARGIN * 2

        # Draw the text
        pygame.draw.rect(surface, cfg.PASSIVE_COLOR, self.topleft.combineToList(self.size), 2)
        surface.blit(self.font.render(self.text, True, cfg.FONT_COLOR), (self.topleft + cfg.TEXT_MARGIN).toTuple())
        