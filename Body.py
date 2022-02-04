from VectorUtils.Vector import *
import pygame


constrain = lambda val, minVal, maxVal: min(maxVal, max(minVal, val))


class Body:
    DYNAMIC_PATH_COLOR = (0, 200, 0)
    STATIC_PATH_COLOR = (215, 215, 215)
    DEFAULT_PATH_COLOR_MULTIPLIER = 0.3
    DYNAMIC_COLOR = (0, 235, 215)
    STATIC_COLOR = (255, 0, 0)
    DEFAULT_DYNAMIC_MASS = 5
    DEFAULT_STATIC_MASS = 50
    path_limit = 'INFINITE'
    path_color_multiplier = DEFAULT_PATH_COLOR_MULTIPLIER
    draw_path = True
    def __init__(self, position: Vector2, initial_velocity: Vector2, static: bool=False, color: tuple=DYNAMIC_COLOR, mass: float=None):
        self.position = position
        self.velocity = initial_velocity
        self.static = static
        self.color = color

        self.acc = Vector2(0, 0)
        self.path = []
        if mass == None:
            self.mass = self.DEFAULT_STATIC_MASS if self.static else self.DEFAULT_DYNAMIC_MASS
        else:
            self.mass = mass
        self.r = sqrt(self.mass)

    def setMass(self, mass:float):
        self.mass = mass
        self.r = sqrt(self.mass)

    def applyForce(self, force: Vector2):
        if self.static: return
        f = force / self.mass
        self.acc += f

    def checkCollision(self, body):
        dist = self.position.getDist(body.position)
        if dist <= 0: return True
        if dist <= self.r + body.r: return True
        return False

    def attract(self, body, G: float=6):
        force = self.position - body.position
        distanceSq = sqrt(force.getMag())
        if distanceSq <= 0: return

        strength = G * (self.mass * body.mass) / distanceSq
        force.setMag(strength)
        body.applyForce(force)

    def update(self, dt: float):
        self.velocity += self.acc * dt
        self.position += self.velocity * dt
        self.acc = Vector2(0, 0)

        self.path.append(self.position.copy())
        if self.path_limit != 'INFINITE':
            try:
                if (len(self.path) > int(self.path_limit)):
                    self.path = self.path[len(self.path) - int(self.path_limit):]
            except ValueError:
                pass

    def show(self):
        if self.draw_path:
            for p in range(len(self.path)):
                if p >= 1:
                    # Get dist between the last two points
                    dist = self.path[p].getDist(self.path[p-1])

                    # Get color
                    org_path_color = self.STATIC_PATH_COLOR if self.static else self.DYNAMIC_PATH_COLOR
                    color = [constrain(dist * self.path_color_multiplier * c, 0, 255) for c in org_path_color]
                    
                    # Render
                    pygame.draw.line(
                        pygame.display.get_surface(), 
                        color, 
                        self.path[p].toTuple(),
                        self.path[p-1].toTuple())
        
        pygame.draw.circle(pygame.display.get_surface(), self.color, self.position.toTuple(), self.r)