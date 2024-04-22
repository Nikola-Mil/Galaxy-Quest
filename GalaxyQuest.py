# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 09:54:27 2024

@author: nikol
"""

import pygame
import sys
import random
import math

pygame.init()

WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 800
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Galaxy Quest")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

maze = [
    "####################",
    "#                  #",
    "#                  #",
    "#      ########  ###",
    "#        #         #",
    "######   #   #######",
    "#        #         #",
    "#  #######   #######",
    "#                  #",
    "#  ##              #",
    "#      #######   ###",
    "#                  #",
    "####################"
]


CELL_WIDTH = WINDOW_WIDTH // len(maze[0])
CELL_HEIGHT = WINDOW_HEIGHT // len(maze)

def draw_maze(surface):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "#":
                # Draw top wall
                if y == 0 or maze[y - 1][x] != "#":
                    pygame.draw.line(surface, WHITE, (x * CELL_WIDTH, y * CELL_HEIGHT), ((x + 1) * CELL_WIDTH, y * CELL_HEIGHT), 2)
                # Draw left wall
                if x == 0 or maze[y][x - 1] != "#":
                    pygame.draw.line(surface, WHITE, (x * CELL_WIDTH, y * CELL_HEIGHT), (x * CELL_WIDTH, (y + 1) * CELL_HEIGHT), 2)
                # Draw right wall
                if x == len(row) - 1 or maze[y][x + 1] != "#":
                    pygame.draw.line(surface, WHITE, ((x + 1) * CELL_WIDTH, y * CELL_HEIGHT), ((x + 1) * CELL_WIDTH, (y + 1) * CELL_HEIGHT), 2)
                # Draw bottom wall
                if y == len(maze) - 1 or maze[y + 1][x] != "#":
                    pygame.draw.line(surface, WHITE, (x * CELL_WIDTH, (y + 1) * CELL_HEIGHT), ((x + 1) * CELL_WIDTH, (y + 1) * CELL_HEIGHT), 2)

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, v2):
        self.x += v2.x
        self.y += v2.y

    def sub(self, v2):
        self.x -= v2.x
        self.y -= v2.y

    def scalar_mult(self, scalar):
        self.x *= scalar
        self.y *= scalar

    def get_mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        mag = self.get_mag()
        if mag != 0:
            self.x /= mag
            self.y /= mag

    def set_mag(self, mag):
        self.normalize()
        self.scalar_mult(mag)

    def limit(self, lim):
        if self.get_mag() > lim:
            self.set_mag(lim)

class Particle:
    def __init__(self, start_pos):
        self.pos = Vector(start_pos[0], start_pos[1])
        self.vel = Vector(0, 0)
        self.accel = Vector(0, 0)
        self.mass = 1
        self.damping_factor = 0.8
        self.fill = YELLOW
        self.attracted = False  # Flag to indicate if particle is attracted to the planet

    def update(self):
        self.vel.add(self.accel)
        self.pos.add(self.vel)

    def apply_force(self, force):
        self.accel.add(force)

    def reset_acceleration(self):
        self.accel.x = 0
        self.accel.y = 0

    def reset_velocity(self):
        self.vel.x = 0
        self.vel.y = 0

    def draw(self, surface):
        pygame.draw.circle(surface, self.fill, (int(self.pos.x), int(self.pos.y)), 6)

    def collide_with_planet(self, planet):
        # Calculate distance between particle and planet
        distance = ((self.pos.x - planet.pos.x) ** 2 + (self.pos.y - planet.pos.y) ** 2) ** 0.5
        combined_radius = 5 + planet.radius  # Adjust the radius as needed
        if distance < combined_radius:
            # Calculate penetration depth
            overlap = combined_radius - distance

            # Calculate direction from particle to planet
            direction = Vector(planet.pos.x - self.pos.x, planet.pos.y - self.pos.y)
            direction.normalize()

            # Move particle away from planet
            self.pos.x -= direction.x * overlap
            self.pos.y -= direction.y * overlap

            # Reflect particle's velocity
            normal = Vector(self.pos.x - planet.pos.x, self.pos.y - planet.pos.y)
            normal.normalize()
            dot_product = self.vel.x * normal.x + self.vel.y * normal.y
            self.vel.x -= 2 * dot_product * normal.x
            self.vel.y -= 2 * dot_product * normal.y

    def attract_to_planet(self, planet):
        distance = ((self.pos.x - planet.pos.x) ** 2 + (self.pos.y - planet.pos.y) ** 2) ** 0.5

    # Check if the particle is close enough to the planet for attraction
        if distance < planet.radius * 2:
            self.attracted = True
        else:
            self.attracted = False

    # Apply attraction force only if the particle is close to the planet
        if self.attracted:
        # Calculate force vector between particle and planet
            force = Vector(planet.pos.x - self.pos.x, planet.pos.y - self.pos.y)

        # Calculate the magnitude of the force with a weaker gravitational constant
            distance = force.get_mag()
            distance = max(distance, 5)  # Avoid division by zero and excessive force at close distances
            force_mag = (6.67 * 0.00004) / (distance ** 2)  # Adjust the gravitational constant as needed (weaker)

        # Normalize the force vector
            force.normalize()

        # Scale the force according to its magnitude
            force.scalar_mult(force_mag)

        # Apply the force to the particle
            self.apply_force(force)


class Planet(Particle):
    def __init__(self, start_pos):
        super().__init__(start_pos)
        self.fill = WHITE
        self.radius = 20  # Adjust as needed for the size of the planet

    def draw(self, surface):
        pygame.draw.circle(surface, self.fill, (int(self.pos.x), int(self.pos.y)), self.radius)

    def suck_particles(self, particles):
        for particle in particles:
            particle.attract_to_planet(self)
            # Calculate distance between particle and planet
            distance = math.sqrt((self.pos.x - particle.pos.x) ** 2 + (self.pos.y - particle.pos.y) ** 2)
            if distance < self.radius:
                particles.remove(particle)  # Remove particle from list
                # Optionally, you can increase the planet's power or ammunition here

    def shoot_bullet(self, bullets):
        # Implement shooting mechanism using particles
        pass  # Placeholder for now

def main():
    # Initialize the planet with a starting position
    planet = Planet((160, 160))

    particles = [Particle((random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))) for _ in range(100)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle keyboard input for planet movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            planet.pos.y -= 0.5
        if keys[pygame.K_s]:
            planet.pos.y += 0.5
        if keys[pygame.K_a]:
            planet.pos.x -= 0.5
        if keys[pygame.K_d]:
            planet.pos.x += 0.5

        # Update particles
        for particle in particles:
            particle.update()
            particle.collide_with_planet(planet)

        # Apply gravitational force from the planet to the particles
        planet.suck_particles(particles)

        window.fill(BLACK)

        draw_maze(window)
        planet.draw(window)
        for particle in particles:
            particle.draw(window)

        pygame.display.update()

if __name__ == "__main__":
    main()