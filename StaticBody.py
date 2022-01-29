from unittest.mock import DEFAULT
from VectorUtils.Vector import *
from Body import *
import pygame


constrain = lambda val, minVal, maxVal: min(maxVal, max(minVal, val))

class StaticBody:
    DEFAULT_MASS = 50
    def __init__(self, position: Vector2, mass: float=None):
        self.position = position
        self.mass = self.DEFAULT_MASS if mass == None else mass
        self.r = sqrt(self.mass)

    def attract(self, body: Body, G: float=6):
        force = self.position - body.position
        distanceSq = constrain(sqrt(force.getMag()), 25, 2500)
        strength = G * (self.mass * body.mass) / distanceSq
        force.setMag(strength)
        body.applyForce(force)

    def show(self, surface: pygame.Surface):
        pygame.draw.circle(surface, (255, 0, 0), self.position.toTuple(), self.r)