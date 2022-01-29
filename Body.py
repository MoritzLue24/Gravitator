from VectorUtils.Vector import *
import pygame


class Body:
    PATH_COLOR = (0, 200, 0)
    BODY_COLOR = (0, 235, 215)
    def __init__(self, position: Vector2, initial_velocity: Vector2, mass: float):
        self.position = position
        self.velocity = initial_velocity
        self.mass = mass

        self.acc = Vector2(0, 0)
        self.path = []

    def applyForce(self, force: Vector2):
        f = force / self.mass
        self.acc += f

    def update(self, deltaTime: float):
        self.velocity += self.acc
        self.position += self.velocity * deltaTime
        self.acc = Vector2(0, 0)

        self.path.append(self.position.copy())
        if len(self.path) > 500:
            self.path.pop(0)

    def show(self, surface: pygame.Surface):
        for pos in self.path:
            pygame.draw.circle(surface, self.PATH_COLOR, pos.toTuple(), 1)
        pygame.draw.circle(surface, self.BODY_COLOR, self.position.toTuple(), 4)