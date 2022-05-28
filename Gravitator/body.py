import pygame
import math
from utils import constrain
from VectorUtils import Vector2


class Body:
    path_length = 200
    path_color_multiplier = 0.5
    def __init__(self, position: Vector2, velocity: Vector2, mass: float, radius: float):
        '''
        The Body class is responsible for creating a body that is affected by gravity of other bodies.

        Args:
            * position (Vector2) - The starting position of the body.
            * velocity (Vector2) - The initial velocity of the body.
            * mass (float) - The mass of the body.
            * radius (float) - The radius of the body (does not affect the physics).
        '''

        self.position = position
        self.velocity = velocity
        self.acceleration = Vector2(0, 0)
        self.mass = mass
        self.radius = radius
        self.path = []


    def applyForce(self, force: Vector2):
        '''
        Apply a force to the body.
        '''

        try:
            self.acceleration += force / self.mass
        except ZeroDivisionError:
            pass
    

    def attract(self, body, g: float):
        '''
        Calculate the force between the two bodies and apply it to the body.
        '''

        force = self.position - body.position
        distanceSquared = math.sqrt(force.getMag())

        if distanceSquared <= 0: return

        strength = g * self.mass * body.mass / distanceSquared
        force.setMag(strength)
        body.applyForce(force)


    def render(self):
        '''
        Render the body & the path.
        '''

        # Draw the path of the body
        for p in range(len(self.path)):
            # Skip the first point to avoid graphical glitches
            # TODO: Fix this in a better way
            if p == 0: continue
            if p+1 != len(self.path):
                # Get dist between the last two points to calculate the color
                # (The bigger the distance, the brighter the color)

                dist = self.path[p].getDist(self.path[p-1])
                color = [constrain(dist * Body.path_color_multiplier * c, 0, 255) for c in [0, 255, 0]]

                pygame.draw.line(pygame.display.get_surface(), color, self.path[p].toTuple(), self.path[p+1].toTuple(), 1)

        # Draw the body
        pygame.draw.circle(pygame.display.get_surface(), (255, 0, 0), self.position.toTuple(), self.radius)

    
    def update(self, deltaTime: float):
        '''
        Update the body.
        '''

        # Remove the last point from the path if the path is too long
        if len(self.path) >= Body.path_length:
            self.path = self.path[int(len(self.path) - Body.path_length):]

        # Add the current position to the path
        self.path.append(self.position)

        # Update the position and velocity of the body.
        self.velocity += self.acceleration * deltaTime
        self.position += self.velocity * deltaTime
        self.acceleration = Vector2(0, 0)
