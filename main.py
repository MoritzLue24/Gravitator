from math import sqrt
from VectorUtils.Vector import *
from StaticBody import *
from Body import *
from gui import *
import pygame
import sys


# <--- Setup pygame --->
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Gravitational Attraction')
font = pygame.font.SysFont('Cascadia Code', 20)
clock = pygame.time.Clock()
deltaTime = 0.0


# <--- Variables --->
G = 6.67e-11 # 6.67e-11
bodies = []
old_paths = []
creating_body = 'None'
current_body_pos = Vector2(0, 0)
current_vel = Vector2(0, 0)

paused = False
dynamic_mass_input = InputField(Vector2(10, 240), Vector2(80, 20), str(Body.DEFAULT_DYNAMIC_MASS))
static_mass_input = InputField(Vector2(10, 290), Vector2(80, 20), str(Body.DEFAULT_STATIC_MASS))
path_limit_input = InputField(Vector2(10, 350), Vector2(80, 20), str(Body.path_limit))

# <--- Mainloop --->
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if (dynamic_mass_input.events(event) or 
            static_mass_input.events(event) or
            path_limit_input.events(event)):
            continue

        # <--- Mouse events --->
        mousePos = pygame.mouse.get_pos()
        if creating_body != 'None':
            current_vel = current_body_pos - Vector2.fromTuple(mousePos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                creating_body = 'Dynamic'
                current_body_pos = Vector2.fromTuple(mousePos)
            # Create static body
            elif pygame.mouse.get_pressed()[2]:
                creating_body = 'Static'
                current_body_pos = Vector2.fromTuple(mousePos)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if creating_body != 'None':
                if creating_body == 'Static':
                    try:
                        mass = float(static_mass_input.text)
                    except ValueError:
                        mass = Body.DEFAULT_STATIC_MASS

                    bodies.append(Body(
                        current_body_pos, 
                        current_vel * 5, 
                        static=True, 
                        color=Body.STATIC_COLOR, 
                        mass=mass))
                else:
                    try:
                        mass = float(dynamic_mass_input.text)
                    except ValueError:
                        mass = Body.DEFAULT_DYNAMIC_MASS

                    bodies.append(Body(current_body_pos, current_vel * 5, mass=mass))
                creating_body = 'None'

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_c:
                old_paths = []
                bodies = []
            elif event.key == pygame.K_ESCAPE:
                paused = not paused
    
    # <--- Render here --->
    screen.fill((0, 0, 0))

    if creating_body != 'None':
        try:
            mass = float(dynamic_mass_input.text if creating_body == 'Dynamic' else static_mass_input.text)
        except ValueError:
            mass = Body.DEFAULT_DYNAMIC_MASS if creating_body == 'Dynamic' else Body.DEFAULT_STATIC_MASS

        pygame.draw.line(screen, (0, 0, 255), current_body_pos.toTuple(), (current_body_pos - current_vel).toTuple(), 2)
        pygame.draw.circle(
            screen, 
            Body.DYNAMIC_COLOR if creating_body == 'Dynamic' else Body.STATIC_COLOR, 
            current_body_pos.toTuple(), 
            sqrt(mass))
    else:
        current_body_pos = Vector2(0, 0)
        current_vel = Vector2(0, 0)
    
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

        body.update()
        for other in bodies:
            if body != other:
                body.attract(other)
                if body.checkCollision(other):
                    if body.mass > other.mass:
                        body.setMass(body.mass + other.mass)
                        bodies.remove(other)
                        old_paths.append((other.path, other.static))
                    else:
                        other.setMass(body.mass + other.mass)
                        bodies.remove(body)
                        old_paths.append((body.path, body.static))


    # Render info
    renderText(('PAUSED' if paused else 'RUNNING') + ' ([escape] to pause / continue)', Vector2(10, 10), font)

    renderText(f'FPS: {clock.get_fps()}', Vector2(10, 40), font)
    renderText(f'G: {G}', Vector2(10, 60), font)
    renderText(f'Total path pixels: {total_path_pixels}', Vector2(10, 80), font)
    renderText(f'Total bodies: {len(bodies)}', Vector2(10, 100), font)
    renderText('Hold [leftclick] / [rightclick] to create dynamic / static body', Vector2(10, 140), font)
    renderText(f'Body position: {current_body_pos}', Vector2(10, 160), font)
    renderText(f'Body velocity: {current_vel}', Vector2(10, 180), font)

    renderText('Dynamic body mass:', Vector2(10, 220), font)
    dynamic_mass_input.draw(font)
    renderText('Static body mass:', Vector2(10, 270), font)
    static_mass_input.draw(font)

    renderText('Path limit per body: ', Vector2(10, 330), font)
    path_limit_input.draw(font)
    Body.path_limit = path_limit_input.text

    # Update dt & display
    deltaTime = 1/clock.get_fps() if clock.get_fps() != 0 else 0.0
    pygame.display.flip()
    clock.tick()

