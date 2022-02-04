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
G = 120 # 6.67e-11
bodies = []
old_paths = []
creating_body = 'None'
current_pos = Vector2(0, 0)
current_vel = Vector2(0, 0)
paused = False
running = True

# Widgets
current_pos_input = InputField(Vector2(10, 180), Vector2(80, 20), 'Body position:', 'AUTO')
current_vel_input = InputField(Vector2(10, 230), Vector2(80, 20), 'Body velocity:', 'AUTO')
dynamic_mass_input = InputField(Vector2(10, 280), Vector2(80, 20), 'Dynamic body mass:', str(Body.DEFAULT_DYNAMIC_MASS))
static_mass_input = InputField(Vector2(10, 330), Vector2(80, 20), 'Static body mass:', str(Body.DEFAULT_STATIC_MASS))
path_limit_input = InputField(Vector2(10, 380), Vector2(80, 20), 'Path limit:', str(Body.path_limit))
dynamic_attract_input = Checkbox(Vector2(10, 430), Vector2(20, 20), 'Dynamic bodies attract eachother:')
can_collide_input = Checkbox(Vector2(10, 480), Vector2(20, 20), 'Bodies can collide:')
path_color_multiplier_input = InputField(Vector2(10, 530), Vector2(40, 20), 'Path color multiplier:', str(Body.path_color_multiplier))


# Mainloop
while running:
    for event in pygame.event.get():
        # Default close operation
        if event.type == pygame.QUIT:
            running = False
        
        # Check for all widget events
        if Widget.events(event): continue

        # Get mouse position and calculate current velocity if creating body is true
        mousePos = pygame.mouse.get_pos()
        if creating_body != 'None':
            current_vel = current_pos - Vector2.fromTuple(mousePos)

        # Start creating a dynamic or static body
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                creating_body = 'Dynamic'
                current_pos = Vector2.fromTuple(mousePos)
            elif pygame.mouse.get_pressed()[2]:
                creating_body = 'Static'
                current_pos = Vector2.fromTuple(mousePos)
        
        # Finish creating a dynamic or static body
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
                    # Get the mass
                    try:
                        mass = float(static_mass_input.text)
                    except ValueError:
                        mass = Body.DEFAULT_STATIC_MASS
                    # Append the list
                    bodies.append(Body(pos, vel, static=True, color=Body.STATIC_COLOR, mass=mass))
                
                # Create dynamic body
                else:
                    # Get the mass
                    try:
                        mass = float(dynamic_mass_input.text)
                    except ValueError:
                        mass = Body.DEFAULT_DYNAMIC_MASS
                    # Append the list
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
        # Get the mass to calculate the radius
        try:
            mass = float(dynamic_mass_input.text if creating_body == 'Dynamic' else static_mass_input.text)
        except ValueError:
            mass = Body.DEFAULT_DYNAMIC_MASS if creating_body == 'Dynamic' else Body.DEFAULT_STATIC_MASS

        # Draw velocity preview
        pygame.draw.line(screen, (0, 0, 255), current_pos.toTuple(), (current_pos - current_vel).toTuple(), 2)

        # Draw the body
        pygame.draw.circle(
            screen, 
            Body.DYNAMIC_COLOR if creating_body == 'Dynamic' else Body.STATIC_COLOR, 
            current_pos.toTuple(), 
            sqrt(mass))
    else:
        # Reset position and velocity if not creating a body
        current_pos = Vector2(0, 0)
        current_vel = Vector2(0, 0)

    # Draw old paths (paths of bodies that collided with other bodies)
    for path in old_paths:
        for p in range(len(path[0])):
            if p >= 1:
                # Get dist between the last two points
                dist = path[0][p].getDist(path[0][p-1])

                # Get color
                org_path_color = Body.STATIC_PATH_COLOR if path[1] else Body.DYNAMIC_PATH_COLOR
                color = [constrain(dist * Body.path_color_multiplier * c, 0, 255) for c in org_path_color]

                # Render
                pygame.draw.line(pygame.display.get_surface(), color, path[0][p].toTuple(), path[0][p-1].toTuple())

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
                if (dynamic_attract_input.active) or (body.static):
                    body.attract(other, G)
                # Collision
                if (body.checkCollision(other)) and (can_collide_input.active):
                    # Remove the body with less mass
                    if body.mass > other.mass:
                        body.setMass(body.mass + other.mass)
                        bodies.remove(other)
                        old_paths.append((other.path, other.static))
                    else:
                        other.setMass(body.mass + other.mass)
                        bodies.remove(body)
                        old_paths.append((body.path, body.static))

    # Render paused info
    renderText(('PAUSED' if paused else 'RUNNING') + ' ([escape] to pause / continue)', Vector2(10, 10), font)

    # Render stats
    renderText(f'FPS: {clock.get_fps()}', Vector2(10, 40), font)
    renderText(f'G: {G}', Vector2(10, 60), font)
    renderText(f'Total path pixels: {total_path_pixels}', Vector2(10, 80), font)
    renderText(f'Total bodies: {len(bodies)}', Vector2(10, 100), font)
    renderText('Hold [leftclick] / [rightclick] to create dynamic / static body', Vector2(10, 140), font)

    # Render all widgets
    Widget.render(font)

    # Update the path limit
    Body.path_limit = path_limit_input.text

    # Set path color multiplier
    try:
        Body.path_color_multiplier = float(path_color_multiplier_input.text)
    except ValueError:
        Body.path_color_multiplier = Body.DEFAULT_PATH_COLOR_MULTIPLIER


    # Update dt & display
    deltaTime = 1/clock.get_fps() if clock.get_fps() != 0 else 0.0
    pygame.display.flip()
    clock.tick()

pygame.quit()
sys.exit()