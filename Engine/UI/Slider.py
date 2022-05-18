import pygame
from VectorUtils import *
from config import *
from Engine.UI.Widget import Widget
from Engine.UI.InputField import InputField
from Engine.UI.config import *


class Slider(Widget):
    HITBOX_SIZE = 10
    LINE_WIDTH = 2
    def __init__(self, topleft: Vector2, slider_dist: int, input_dist: int, size: Vector2, min_val: float | int, max_val: float | int, start_val: float | int=0, description: str='', type: str='square'):
        '''
        This class is used to take input from the user in the form of a slider. \n
        slider_dist = Distance between topleft and the slider \n
        input_dist = Distance between the slider and the input field \n
        '''
        super().__init__(topleft)
        
        self.size = size
        self.slider_dist = slider_dist
        self.min = min_val
        self.max = max_val
        self.value = start_val
        self.description = description
        self.type = type
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

        # Calculate the percentage of the slider that is filled by the current value and store it in self.t 
        self.t = (self.value - self.min) / (self.max - self.min)

        # Calculate the hitbox rect of the slider and store it in self.rect 
        self.slider_rect = pygame.Rect(self.topleft.x + slider_dist + self.size.x * self.t - self.HITBOX_SIZE / 2, self.topleft.y + self.size.y / 2 - self.HITBOX_SIZE / 2, self.HITBOX_SIZE, self.HITBOX_SIZE)

        # Create the input field for the value of the slider and store it in self.input_field
        self.input_field = InputField(Vector2(self.topleft.x + self.size.x + slider_dist + input_dist, topleft.y), str(start_val))


    def event_handler(self, event: pygame.event.Event=None) -> bool:
        '''
        The event handler has to be called once inside the event loop. \n
        The event parameter does not have to be passed to the event handler. Its just there so the Window class can call it.
        '''
        # Set active to true, if the user has clicked on the slider
        if (self.slider_rect.collidepoint(pygame.mouse.get_pos()) or pygame.Rect(self.topleft.x + self.slider_dist, self.topleft.y, self.size.x, self.size.y).collidepoint(pygame.mouse.get_pos())) and pygame.mouse.get_pressed()[0]:
            self.active = True
            return True

        # Set active to false, if the user has released the mouse button
        if not pygame.mouse.get_pressed()[0]:
            self.active = False
        
        return False


    def setValue(self, value: float | int):
        '''
        Set the value of the slider and adjust its position.
        '''
        self.value = value
        self.input_field.text = str(round(self.value, 1))

        # Update the position of the slider rectangle
        self.t = (constrain(self.value, self.min, self.max) - self.min) / (self.max - self.min)
        self.slider_rect = pygame.Rect(self.topleft.x + self.slider_dist + self.size.x * self.t - self.HITBOX_SIZE / 2, self.topleft.y + self.size.y / 2 - self.HITBOX_SIZE / 2, self.HITBOX_SIZE, self.HITBOX_SIZE)


    def draw(self):
        '''
        The draw method has to be called once per frame.
        '''
        # Draw the description if there is one
        if self.description != '':
            font_render = self.font.render(self.description, True, FONT_COLOR)
            pygame.display.get_surface().blit(font_render, self.topleft.toTuple())

        # Draw the slider line
        middle_y = self.topleft.y + self.size.y / 2
        pygame.draw.line(pygame.display.get_surface(), (255, 255, 255), (self.topleft.x + self.slider_dist, middle_y - self.LINE_WIDTH / 2), (self.topleft.x + self.slider_dist + self.size.x, middle_y - self.LINE_WIDTH / 2), self.LINE_WIDTH)

        # Get the color for the slider
        slider_color = ACTIVE_COLOR if self.active else PASSIVE_COLOR

        # Draw the slider itself
        if self.type == 'square':
            pygame.draw.rect(pygame.display.get_surface(), slider_color, self.slider_rect)
        elif self.type == 'circle':
            pygame.draw.circle(pygame.display.get_surface(), slider_color, self.slider_rect.center, self.HITBOX_SIZE / 2)
        else:
            print('Invalid slider type')


        # Update the position of the slider
        # (Inside draw() because it is called once per frame)
        if self.active:
            self.slider_rect.centerx = constrain(pygame.mouse.get_pos()[0], self.topleft.x + self.slider_dist, self.topleft.x + self.slider_dist + self.size.x)
            
            self.t = (self.slider_rect.centerx - (self.topleft.x + self.slider_dist)) / self.size.x
            self.value = self.min + (self.max - self.min) * self.t
            self.input_field.text = str(round(self.value, 1))

        # Apply changes of the input field
        if self.input_field.changed:
            try:
                self.setValue(float(self.input_field.text))
            except ValueError:
                print('Invalid slider value.')
                self.input_field.text = str(round(self.value, 1))

        # Round the number inside the input field
        if not self.input_field.active:
            try:
                self.input_field.text = str(round(float(self.input_field.text), 1))
            except ValueError:
                print('Invalid slider value.')
        