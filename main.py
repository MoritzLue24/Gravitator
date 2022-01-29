from VectorUtils.Vector import *
from StaticBody import *
from Body import *
import pygame
import sys


# <--- Setup pygame --->
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Attraction")
font = pygame.font.SysFont("Cascadia Code", 20)
clock = pygame.time.Clock()
deltaTime = 0.0

def renderText(text: str, position: Vector2, color: pygame.Color):
    text = font.render(text, 1, color)
    screen.blit(text, position.toTuple())


# <--- Variables --->
bodies = []
static_bodies = []
creating_body = False
current_body_pos = Vector2(0, 0)
current_vel = Vector2(0, 0)


# <--- Mainloop --->
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # <--- Mouse events --->
        mousePos = pygame.mouse.get_pos()
        if creating_body:
            current_vel = current_body_pos - Vector2.fromTuple(mousePos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                creating_body = True
                current_body_pos = Vector2.fromTuple(mousePos)
            # Add static body if second mouse button is pressed
            elif pygame.mouse.get_pressed()[2]:
                static_bodies.append(StaticBody(Vector2.fromTuple(mousePos), 50))
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if creating_body:
                creating_body = False
                bodies.append(Body(current_body_pos, current_vel * 5, 50))

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if len(bodies) > 0: bodies.pop()
    
    # <--- Render here --->
    screen.fill((0, 0, 0))

    if creating_body:
        pygame.draw.line(screen, (0, 0, 255), current_body_pos.toTuple(), (current_body_pos - current_vel).toTuple(), 2)
        pygame.draw.circle(screen, Body.BODY_COLOR, current_body_pos.toTuple(), 4)
    else:
        current_body_pos = Vector2(0, 0)
        current_vel = Vector2(0, 0)

    for static_body in static_bodies:
        static_body.show(screen)
        for body in bodies:
            static_body.attract(body)
    
    total_path_pixels = 0
    for body in bodies:
        body.update(deltaTime)
        body.show(screen)
        total_path_pixels += len(body.path)

    renderText(f'FPS: {str(clock.get_fps())}', Vector2(10, 10), (255, 255, 255))
    renderText(f'Total path pixels: {str(total_path_pixels)}', Vector2(10, 30), (255, 255, 255))
    renderText(f'Total bodies: {str(len(bodies))}', Vector2(10, 50), (255, 255, 255))
    renderText(f'Total static bodies: {str(len(static_bodies))}', Vector2(10, 70), (255, 255, 255))
    renderText('Left click to create body', Vector2(10, 120), (255, 255, 255))
    renderText(f'Body position: {current_body_pos}', Vector2(10, 140), (255, 255, 255))
    renderText(f'Body velocity: {current_vel}', Vector2(10, 160), (255, 255, 255))

    deltaTime = 1/clock.get_fps() if clock.get_fps() != 0 else 0.0
    pygame.display.flip()
    clock.tick()

