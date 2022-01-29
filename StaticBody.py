from VectorUtils.Vector import *
from Body import *
import pygame


constrain = lambda val, minVal, maxVal: min(maxVal, max(minVal, val))

class StaticBody:
    def __init__(self, position: Vector2, mass: float):
        self.position = position
        self.mass = mass
        self.r = sqrt(self.mass)

    def attract(self, body: Body, g: float=6):
        force = self.position - body.position
        distanceSq = constrain(sqrt(force.getMag()), 25, 2500)
        strength = g * (self.mass * body.mass) / distanceSq
        force.setMag(strength)
        body.applyForce(force)

    def show(self, surface: pygame.Surface):
        pygame.draw.circle(surface, (255, 0, 0), self.position.toTuple(), self.r)