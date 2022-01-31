from VectorUtils.Vector import *
import pygame


class Body:
    DYNAMIC_PATH_COLOR = (0, 200, 0)
    STATIC_PATH_COLOR = (215, 215, 215)
    DYNAMIC_COLOR = (0, 235, 215)
    STATIC_COLOR = (255, 0, 0)
    DEFAULT_DYNAMIC_MASS = 5
    DEFAULT_STATIC_MASS = 50
    path_limit = 'INFINITE'
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

    def update(self):
        self.velocity += self.acc
        self.position += self.velocity * 0.01
        self.acc = Vector2(0, 0)

        self.path.append(self.position.copy())
        if self.path_limit != 'INFINITE':
            try:
                if (len(self.path) > int(self.path_limit)):
                    self.path = self.path[len(self.path) - int(self.path_limit):]
            except ValueError:
                pass

    def show(self):
        for pos in self.path:
            pygame.draw.rect(
                pygame.display.get_surface(), 
                self.STATIC_PATH_COLOR if self.static else self.DYNAMIC_PATH_COLOR, 
                [pos.x, pos.y, 1, 1])
                
        pygame.draw.circle(pygame.display.get_surface(), self.color, self.position.toTuple(), self.r)