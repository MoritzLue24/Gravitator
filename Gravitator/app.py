import pygame
import tkinter as tk
import ui
from tkinter import filedialog, messagebox
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

        # If the user wants to add & move a body, these is the variable that will be used
        self.current_body = None
        self.dragged_body = None

        # UI
        ui.Font('assets/Fonts/Roboto-Regular.ttf', 16, (225, 225, 225))
        self.config_surf = ui.Surface(Vector2(0, 0), Vector2(270, height), 170)
        self.fps_text = self.config_surf.addWidget(ui.Text(text='FPS: 0.0'))
        self.run_button = self.config_surf.addWidget(ui.Button(
            topleft=Vector2(self.config_surf.topleft.x + 10, self.config_surf.topleft.y + self.config_surf.size.y - (ui.Font.getRenderSize('a').y + 40)  - 10),
            description='Run Script', 
            on_click=self.runScript, 
            margin=Vector2(20, 20)
        ))

        # Inputs
        self.mass_input = self.config_surf.addWidget(ui.InputField(description='Mass:', text='2.0', min_width=90))
        self.radius_input = self.config_surf.addWidget(ui.InputField(description='Radius:', text='4', min_width=90))
        self.g_input = self.config_surf.addWidget(ui.InputField(description='G:', text='400.0', min_width=90))
        self.path_length_input = self.config_surf.addWidget(ui.InputField(description='Path length:', text='0', min_width=90))
        self.path_color_multiplier_input = self.config_surf.addWidget(ui.InputField(description='Path color multiplier:', text='0.5', min_width=90))
        self.draw_lines_input = self.config_surf.addWidget(ui.Checkbox(description='Draw lines:', checked=True))
        self.bg_alpha_input = self.config_surf.addWidget(ui.InputField(description='Background alpha:', text='0.1', min_width=90))


    def runScript(self):
        '''
        This function is called when the user presses the run button.
        It will run the script and add the bodies to the simulation.
        '''

        # Clear the simulation
        self.bodies.clear()

        # Get the file path of a file with a dialog
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(initialdir='.', title='Select a file', filetypes=(('Python files', '*.py'), ('all files', '*.*')))

        # Run the script
        with open(file_path, 'r') as f:
            try:
                exec(f.read())
            except Exception as e:
                messagebox.showerror('Error', 'An error occured while running the script:\n{}'.format(e))


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

        # Draw & update bodies
        for body in self.bodies:
            if self.draw_lines_input.checked:
                for other in self.bodies:
                    if body != other:
                        pygame.draw.line(self.screen, (255, 255, 255), body.position.toTuple(), other.position.toTuple(), 1)

            body.draw()

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
            self.current_body.draw()

    
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.current_body = self.createBody()
                    elif event.button == 3:
                        for body in self.bodies:
                            if body.position.getDist(Vector2.fromTuple(pygame.mouse.get_pos())) < body.radius + 10:
                                self.dragged_body = body
                                break

                elif (event.type == pygame.MOUSEBUTTONUP):
                    if (event.button == 1) and self.current_body:
                        self.bodies.append(self.current_body)
                        self.current_body = None
                    elif (event.button == 3) and self.dragged_body:
                        self.dragged_body.color = Body.COLOR
                        self.dragged_body = None


            # Update g & path length & path color
            try:
                self.g = float(self.g_input.text)
                Body.path_length = int(self.path_length_input.text)
                Body.path_color_multiplier = float(self.path_color_multiplier_input.text)
            except ValueError:
                pass
                
            # Update the dragged body's position & color
            if self.dragged_body:
                self.dragged_body.position = Vector2.fromTuple(pygame.mouse.get_pos())
                self.dragged_body.velocity = Vector2(0, 0)
                self.dragged_body.color = (10, 200, 10)


            # Clear the screen
            try:
                bg_alpha = float(self.bg_alpha_input.text)
            except ValueError:
                bg_alpha = 1
            bg_img = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
            pygame.draw.rect(bg_img, (0, 0, 0, 255 * bg_alpha), bg_img.get_rect())
            self.screen.blit(bg_img, (0, 0))

            # Draw & update the bodies
            self.handleBodies()

            # Display the ui
            self.config_surf.draw()

            # Draw & delta time
            pygame.display.flip()
            self.delta_time = self.clock.tick(60) / 1000.0
            self.fps_text.text = f'FPS: {str(round(1 / self.delta_time, 1))}  |  {"Paused" if self.paused else "Running"}'
            

        # Cleanup
        pygame.quit()
