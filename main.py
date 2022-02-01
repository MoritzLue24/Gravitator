from math import sqrt
from VectorUtils.Vector import *
from Body import *
from gui import *
import pygame
import sys


# Setup pygame
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Gravitational Attraction')
font = pygame.font.SysFont('Cascadia Code', 20)
clock = pygame.time.Clock()
deltaTime = 0.0


# Variables
G = 6.67e-11 # 6.67e-11
bodies = []
old_paths = []
creating_body = 'None'
current_pos = Vector2(0, 0)
current_vel = Vector2(0, 0)
paused = False
running = True

# Inputs
current_pos_input = InputField(Vector2(10, 180), Vector2(80, 20), 'AUTO')
current_vel_input = InputField(Vector2(10, 230), Vector2(80, 20), 'AUTO')
dynamic_mass_input = InputField(Vector2(10, 280), Vector2(80, 20), str(Body.DEFAULT_DYNAMIC_MASS))
static_mass_input = InputField(Vector2(10, 330), Vector2(80, 20), str(Body.DEFAULT_STATIC_MASS))
path_limit_input = InputField(Vector2(10, 380), Vector2(80, 20), str(Body.path_limit))
dynamic_attract_input = InputField(Vector2(10, 430), Vector2(80, 20), 'True')
can_collide_input = InputField(Vector2(10, 480), Vector2(80, 20), 'True')

# Mainloop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Check for input field events
        if (current_pos_input.events(event) or
            current_vel_input.events(event) or
            dynamic_mass_input.events(event) or 
            static_mass_input.events(event) or
            path_limit_input.events(event) or 
            dynamic_attract_input.events(event) or
            can_collide_input.events(event)):
            continue

        # Mouse events
        mousePos = pygame.mouse.get_pos()
        if creating_body != 'None':
            current_vel = current_pos - Vector2.fromTuple(mousePos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                creating_body = 'Dynamic'
                current_pos = Vector2.fromTuple(mousePos)
            # Create static body
            elif pygame.mouse.get_pressed()[2]:
                creating_body = 'Static'
                current_pos = Vector2.fromTuple(mousePos)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if creating_body != 'None':
                # Get position
                if current_pos_input.text.lower() != 'auto':
                    try:
                        pos = current_pos_input.text.split(', ')
                        pos = Vector2(float(pos[0]), float(pos[1]))
                    except ValueError:
                        pos = current_pos
                else:
                    pos = current_pos

                # Get velocity
                if current_vel_input.text.lower() != 'auto':
                    try:
                        vel = current_vel_input.text.split(', ')
                        vel = Vector2(float(vel[0]), float(vel[1]))
                    except ValueError:
                        vel = current_vel * 5
                else:
                    vel = current_vel * 5

                # Create static body
                if creating_body == 'Static':
                    try:
                        mass = float(static_mass_input.text)
                    except ValueError:
                        mass = Body.DEFAULT_STATIC_MASS

                    bodies.append(Body(
                        pos, 
                        vel, 
                        static=True, 
                        color=Body.STATIC_COLOR, 
                        mass=mass))
                else:
                    # Create dynamic body
                    try:
                        mass = float(dynamic_mass_input.text)
                    except ValueError:
                        mass = Body.DEFAULT_DYNAMIC_MASS
                    bodies.append(Body(pos, vel, mass=mass))
                creating_body = 'None'

        # Key events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_c:
                old_paths = []
                bodies = []
            elif event.key == pygame.K_ESCAPE:
                paused = not paused
    
    # Render & update
    screen.fill((0, 0, 0))

    # Draw body preview when creating body
    if creating_body != 'None':
        try:
            mass = float(dynamic_mass_input.text if creating_body == 'Dynamic' else static_mass_input.text)
        except ValueError:
            mass = Body.DEFAULT_DYNAMIC_MASS if creating_body == 'Dynamic' else Body.DEFAULT_STATIC_MASS

        pygame.draw.line(screen, (0, 0, 255), current_pos.toTuple(), (current_pos - current_vel).toTuple(), 2)
        pygame.draw.circle(
            screen, 
            Body.DYNAMIC_COLOR if creating_body == 'Dynamic' else Body.STATIC_COLOR, 
            current_pos.toTuple(), 
            sqrt(mass))
    else:
        current_pos = Vector2(0, 0)
        current_vel = Vector2(0, 0)

    # Draw old paths (paths of bodies that collided with other bodies)
    for path in old_paths:
        for pixel in path[0]:
            pygame.draw.rect(
                screen,
                Body.STATIC_PATH_COLOR if path[1] else Body.DYNAMIC_PATH_COLOR, 
                [pixel.x, pixel.y, 1, 1])

    # Update & draw bodies
    total_path_pixels = 0
    for body in bodies:
        body.show()
        total_path_pixels += len(body.path) 
        if paused: continue

        body.update(deltaTime)
        for other in bodies:
            if body != other:
                # Attract
                if (dynamic_attract_input.text == 'True') or (body.static):
                    body.attract(other)
                # Collision
                if (body.checkCollision(other)) and (can_collide_input.text == 'True'):
                    # Remove the body with less mass
                    if body.mass > other.mass:
                        body.setMass(body.mass + other.mass)
                        bodies.remove(other)
                        old_paths.append((other.path, other.static))
                    else:
                        other.setMass(body.mass + other.mass)
                        bodies.remove(body)
                        old_paths.append((body.path, body.static))


    # Paused info
    renderText(('PAUSED' if paused else 'RUNNING') + ' ([escape] to pause / continue)', Vector2(10, 10), font)

    # Stats
    renderText(f'FPS: {clock.get_fps()}', Vector2(10, 40), font)
    renderText(f'G: {G}', Vector2(10, 60), font)
    renderText(f'Total path pixels: {total_path_pixels}', Vector2(10, 80), font)
    renderText(f'Total bodies: {len(bodies)}', Vector2(10, 100), font)
    renderText('Hold [leftclick] / [rightclick] to create dynamic / static body', Vector2(10, 140), font)

    # Pos & vel input
    renderText('Body position:', Vector2(10, 160), font)
    current_pos_input.draw(font)
    renderText('Body velocity:', Vector2(10, 210), font)
    current_vel_input.draw(font)

    # Mass input
    renderText('Dynamic body mass:', Vector2(10, 260), font)
    dynamic_mass_input.draw(font)
    renderText('Static body mass:', Vector2(10, 310), font)
    static_mass_input.draw(font)

    # Path limit input
    renderText('Path limit per body: ', Vector2(10, 360), font)
    path_limit_input.draw(font)
    Body.path_limit = path_limit_input.text

    # Dynamic attract input
    renderText('Dynamic bodies attract eachother: ', Vector2(10, 410), font)
    dynamic_attract_input.draw(font)

    # Can collide input
    renderText('Bodies can collide: ', Vector2(10, 460), font)
    can_collide_input.draw(font)

    # Update dt & display
    deltaTime = 1/clock.get_fps() if clock.get_fps() != 0 else 0.0
    pygame.display.flip()
    clock.tick()

pygame.quit()
sys.exit()