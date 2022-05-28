import pygame
import ui
from VectorUtils import Vector2
from body import Body


class Application:
    def __init__(self, title: str, width: int, height: int):
        '''
        The application class is the main class of the program.

        Args:
            * title (str) - The title of the window.
            * width (int) - The width of the window.
            * height (int) - The height of the window.
        '''

        # Initialize pygame
        pygame.init()

        # Create a window
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(title)

        # Running and pause variables (if paused, the physics will not be calculated)
        self.running = True
        self.paused = False
        self.g = 400

        # Deltatime
        self.delta_time = 0.0

        # Every body in the simulation is inside this list
        self.bodies = []

        # If the user wants to add a body, this is the variable that will be used
        self.current_body = None

        # UI
        ui.Font('assets/Fonts/Roboto-Regular.ttf', 16, (225, 225, 225))
        self.config_surf = ui.Surface(Vector2(0, 0), Vector2(270, height), 170)
        self.fps_text = self.config_surf.addWidget(ui.Text(text='FPS: 0.0'))
        self.mass_input = self.config_surf.addWidget(ui.InputField(description='Mass:', text='2.0', min_width=90))
        self.radius_input = self.config_surf.addWidget(ui.InputField(description='Radius:', text='4', min_width=90))
        self.g_input = self.config_surf.addWidget(ui.InputField(description='G:', text='400.0', min_width=90))
        self.path_length_input = self.config_surf.addWidget(ui.InputField(description='Path length:', text='200', min_width=90))
        self.path_color_multiplier_input = self.config_surf.addWidget(ui.InputField(description='Path color multiplier:', text='0.5', min_width=90))


    def createBody(self):
        '''
        Application.createBody() is called when the user releases the mouse.
        '''

        # Create a body
        try:
            mass = float(self.mass_input.text)
            radius = float(self.radius_input.text)
        except ValueError:
            return None

        return Body(Vector2.fromTuple(pygame.mouse.get_pos()), Vector2(0, 0), mass, radius)


    def handleBodies(self):
        '''
        This function is called every frame.
        It handles the bodies and their interactions.
        '''

        # Render & update bodies
        for body in self.bodies:
            body.render()

            if self.paused:
                continue

            for other in self.bodies:
                if body != other:
                    body.attract(other, self.g)
            body.update(self.delta_time)

        # Update the initial velocity of the body based on the mouse position if the user is creating a body
        if self.current_body:
            mouse_pos = Vector2.fromTuple(pygame.mouse.get_pos())

            self.current_body.velocity = self.current_body.position - mouse_pos

            # Draw a line from the current mouse position to the position of the body
            pygame.draw.line(self.screen, (0, 0, 255), mouse_pos.toTuple(), self.current_body.position.toTuple())
            self.current_body.render()

    
    def run(self):
        '''
        Run this function to start the main loop.
        '''

        # Mainloop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Handle ui events
                if ui.Surface.handleEvents(event) or ui.Widget.oneActive():
                    continue
                
                # If the user presses the escape key, the physics will be paused
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_BACKSPACE:
                        self.bodies.pop()
                    elif event.key == pygame.K_c:
                        self.bodies = []

                # Handle body events
                elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
                    self.current_body = self.createBody()
                elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1) and self.current_body:
                    self.bodies.append(self.current_body)
                    self.current_body = None


            # Update g & path length & path color
            try:
                self.g = float(self.g_input.text)
                Body.path_length = int(self.path_length_input.text)
                Body.path_color_multiplier = float(self.path_color_multiplier_input.text)
            except ValueError:
                pass


            # Clear the screen
            self.screen.fill((0, 0, 0))

            # Render & update the bodies
            self.handleBodies()

            # Display the ui
            self.config_surf.render()

            # Render the pause / unpause image on the bottom left
            img = pygame.transform.scale(pygame.image.load(f'assets/{"paused" if self.paused else "running"}_icon.png'), (32, 32))
            self.screen.blit(img, (5, self.screen.get_height() - 37))

            # Render & delta time
            pygame.display.flip()
            self.delta_time = self.clock.tick(60) / 1000.0
            self.fps_text.text = 'FPS: ' + str(round(1 / self.delta_time, 1))
            

        # Cleanup
        pygame.quit()
