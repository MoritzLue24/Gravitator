import pygame
from math import sqrt
from VectorUtils import Vector2
from config import *


constrain = lambda val, minVal, maxVal: min(maxVal, max(minVal, val))


class Body:
    def __init__(self, position: Vector2, initial_velocity: Vector2, mass: float, radius: float):
        '''
        The Body class is responsible for creating a body that is affected by gravity of other bodies.
        '''
        self.position = position
        self.velocity = initial_velocity
        self.acceleration = Vector2(0, 0)
        self.mass = mass
        self.radius = radius

        self.path = []


    def applyForce(self, force: Vector2):
        # Calculate the acceleration of the body by dividing the force by the mass of the body and 
        # multiply by delta_time to get the acceleration in pixels per second per second. 
        try:
            f = force / self.mass
        except ZeroDivisionError:
            f = Vector2(0, 0)
            
        self.acceleration += f


    def attract(self, body, g: float):
        '''
        Calculate the force between the two bodies.
        '''

        force = self.position - body.position
        distanceSquared = sqrt(force.getMag())

        if distanceSquared <= 0: return

        strength = g * self.mass * body.mass / distanceSquared
        force.setMag(strength)
        body.applyForce(force)


    def drawPath(self, screen, color_multiplier: float):
        '''
        Draw the path of the body. 
        '''

        # Get dist between the last two points to calculate the color
        # (The bigger the distance, the brighter the color)

        for p in range(len(self.path)):
            # Skip the first point to avoid graphical glitches
            # TODO: Fix this in a better way
            if p == 0: continue
            if p+1 != len(self.path):
                # Get dist between the last two points to calculate the color
                # (The bigger the distance, the brighter the color)

                dist = self.path[p].getDist(self.path[p-1])
                color = [constrain(dist * color_multiplier * c, 0, 255) for c in PATH_COLOR]

                pygame.draw.line(screen, color, self.path[p].toTuple(), self.path[p+1].toTuple(), 1)


    def update(self, delta_time: float, path_length: int):
        '''
        Has to be called once per time step.
        '''

        if draw_path:
            # Remove the last point from the path if the path is too long
            if len(self.path) >= path_length:
                self.path = self.path[int(len(self.path)-path_length):]

            # Add the current position to the path
            self.path.append(self.position)

        # Update the position of the body
        self.velocity += self.acceleration * delta_time
        self.position += self.velocity * delta_time
        self.acceleration = Vector2(0, 0)