import pygame
from VectorUtils import Vector2


class Font(pygame.font.Font):
    _instance = None
    def __init__(self, filename: str, size: int, color: pygame.Color):
        '''
        Initialize the font. This function must be called before any other render function of a ui surface.

        Args:
            * filename (str) - The path to the font file.
            * size (int) - The size of the font.
            * color (sdl2.ext.Color) - The color of the font.
        '''

        super().__init__(filename, size)
        self.color = color
        Font._instance = self


    @staticmethod
    def get():
        '''
        Get the instance of the font.
        '''

        return Font._instance


    @staticmethod
    def getRenderSize(text: str) -> Vector2:
        '''
        Get the size of the text surface.
        '''

        surface = Font.get().render(text, False, Font.get().color)

        # Return the result
        return Vector2(surface.get_width(), surface.get_height())


    @staticmethod
    def myRender(surface: pygame.Surface, text: str, topleft: Vector2):
        '''
        Render the text on the surface.
        '''
        
        # Get the text surface
        text_surf = Font.get().render(text, True, Font.get().color)
        
        # Render the text
        surface.blit(text_surf, topleft.toTuple())

