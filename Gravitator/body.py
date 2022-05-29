import pygame
import math
from utils import constrain
from VectorUtils import Vector2


class Body:
    COLOR = (200, 10, 10)
    PATH_COLOR = (0, 255, 0)
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
        self.color = Body.COLOR
        self.path = []


    def applyForce(self, force: Vector2):
        '''
        Apply a force to the body.
        '''
        
        if self.mass <= 0: return
        self.acceleration += force / self.mass
    

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


    def draw(self):
        '''
        Draws the body & the path.
        '''

        # Draw the path of the body
        for p in range(len(self.path)):
            if (p == 0) or (p+1 == len(self.path)): continue

            # Get dist between the last two points to calculate the color
            # (The bigger the distance, the brighter the color)
            dist = self.path[p].getDist(self.path[p-1])

            # Multiply the color by the distance and by the path color multiplier to make it more / less visible
            color = [constrain(dist * Body.path_color_multiplier * c, 0, 255) for c in Body.PATH_COLOR]
            pygame.draw.line(pygame.display.get_surface(), color, self.path[p].round().toTuple(), self.path[p+1].round().toTuple(), 1)

        pygame.draw.circle(pygame.display.get_surface(), self.color, self.position.round().toTuple(), self.radius)

    
    def update(self, deltaTime: float):
        '''
        Update the body.
        '''

        # Remove the last point from the path if the path exceeds the max length
        if len(self.path) >= Body.path_length:
            self.path = self.path[int(len(self.path) - Body.path_length):]
        self.path.append(self.position)

        self.velocity += self.acceleration * deltaTime
        self.position += self.velocity * deltaTime
        self.acceleration = Vector2(0, 0)
