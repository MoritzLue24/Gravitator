import pygame
import sys
from VectorUtils import Vector2
from config import *
import ui
from body import Body


class Window(pygame.Surface):
    def __init__(self):
        '''
        The Window class is responsible for creating the window,
        initializing the pygame module and executing the main loop. 

        Run the main loop by calling Window.run()
        '''

        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.delta_time = 0.0

        # Pause flag (used to pause the simulation)
        self.paused = False
        self.g = 400

        # Initialize the user interface
        slider_x = 100
        self.fps_text = ui.Text(Vector2(10, 10), 'FPS: 0.00')
        self.mass_input = ui.Slider(Vector2(10, 50), slider_x, 8, Vector2(100, 20), 0.0, 10.0, 2.0, 'Mass  ')
        self.radius_input = ui.Slider(Vector2(10, 90), slider_x, 8, Vector2(100, 20), 0.0, 10.0, 2.0, 'Radius')
        self.g_input = ui.Slider(Vector2(10, 130), slider_x, 8, Vector2(100, 20), 0.0, 1000, 400, 'G ')
        self.path_col_input = ui.Slider(Vector2(10, 170), slider_x, 8, Vector2(100, 20), 0.0, 1.0, 0.2, 'Path Color ')
        self.path_length_input = ui.Slider(Vector2(10, 210), slider_x, 8, Vector2(100, 20), 0, 1000, 100, 'Path Length ')

        # List to store all bodies
        self.bodies = []

        # Flag that indicates if the user is creating a body
        # (Its used to allow the user to customize the initial velocity of the body)
        self.current_body = None


    def createBody(self):
        '''
        Window.createBody() is called when the user releases the mouse.
        '''

        # Get the current mouse position
        mouse_pos = Vector2.fromTuple(pygame.mouse.get_pos())

        # Create a body
        mass = self.mass_input.value
        radius = self.radius_input.value

        return Body(mouse_pos, Vector2(0, 0), mass, radius)


    def updateBodies(self):
        '''
        Has to be called once per frame
        '''
        for body in self.bodies:
            # Draw the body
            body.drawPath(self.screen, self.path_col_input.value)
            pygame.draw.circle(self.screen, BODY_COLOR, body.position.toTuple(), body.radius)
            
            # Skip to the next body if the simulation is paused
            if self.paused:
                continue

            # Make the bodies attract each other
            for other in self.bodies:
                if body != other:
                    body.attract(other, self.g)

            # Update the body
            body.update(self.delta_time, self.path_length_input.value)

        # Update the initial velocity of the body based on the mouse position if the user is creating a body
        if self.current_body:
            self.current_body.velocity = self.current_body.position - Vector2.fromTuple(pygame.mouse.get_pos())

            # Draw a line from the current mouse position to the position of the body
            pygame.draw.line(self.screen, INITIAL_VEL_COLOR, pygame.mouse.get_pos(), self.current_body.position.toTuple(), 1)

        # Draw the current body
        if self.current_body:
            pygame.draw.circle(self.screen, BODY_COLOR, self.current_body.position.toTuple(), self.current_body.radius)


    def run(self):
        '''
        Window.run() is the main loop of the window. 

        It is responsible for updating the display and handling events.
        '''

        while True:
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                
                # Continue the event loop if the user presses ontop of one widget so that the user cant click through the widget
                if ui.Widget.events_all(event):
                    continue
                
                # Continue the event loop if a widget is active
                one_active = ui.Widget.oneActive()
                if one_active:
                    continue
                
                if event.type == pygame.KEYDOWN:
                    # Press escape to pause the simulation
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                    # Press [c] to delete all bodies
                    elif event.key == pygame.K_c:
                        self.bodies = []
                    # Press backspace to delete the last body
                    elif event.key == pygame.K_BACKSPACE:
                        if len(self.bodies) > 0:
                            self.bodies.pop()

                # Create a body if the left mouse button is pressed
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.current_body = self.createBody()
                
                # Stop creating a body if the left mouse button is released
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.current_body is not None:
                    self.bodies.append(self.current_body)
                    self.current_body = None

            # Gray background
            self.screen.fill(MAIN_BG_COLOR)

            # Bodies
            self.updateBodies()

            # Update G
            self.g = self.g_input.value

            # Draw the user interface
            # Get the highest y value of all input fields widgets
            max_x = max([widget.topleft.x + widget.size.x for widget in ui.Widget.instances if isinstance(widget, ui.InputField)])

            # Draw the background for the user interface
            # The x size of the background is the highest x value of all input fields + offset
            pygame.draw.rect(self.screen, pygame.Color(ui.BG), pygame.Rect(0, 0, max_x + 10, HEIGHT))
            ui.Widget.draw_all()

            # Draw the paused / running icon
            img = pygame.transform.scale(pygame.image.load('assets/paused_icon.png' if self.paused else 'assets/running_icon.png').convert_alpha(), (32, 32))
            self.screen.blit(img, (10, HEIGHT - img.get_width() - 10))

            # Update dt & display
            self.delta_time = 1/self.clock.get_fps() if self.clock.get_fps() != 0 else 0.0
            pygame.display.flip()
            self.fps_text.text = 'FPS: ' + str(round(self.clock.get_fps(), 2))
            self.clock.tick(60)


if __name__ == '__main__':
    # Create the window
    window = Window()
    
    # Run the main loop
    window.run()

    # Exit
    pygame.quit()
    sys.exit()