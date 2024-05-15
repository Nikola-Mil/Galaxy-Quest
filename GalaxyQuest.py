# -*- coding: utf-8 -*-
"""
Created on Wed May  5 14:49:20 2021

@author: ROSS THE BOSS & NIK THE BIK
"""

import math

import pygame, sys
from pygame.locals import *


c = 0.5*(10)
gravity_power = 0.5
particle_color = (255,255,0)
planet_color = (255, 0, 0)         
numberOfParticles = 100
friction_coefficient = 0.60
particle_mass = 1
particle_damping = 0.80
planet_radius = 40
white = (255, 255, 255)
drag_factor = 0.05
planet_velocity = [0, 0]

maze = [
    "################################################################",
    "#                                                              #",
    "#                                                              #",
    "#      #####################################            ########",
    "#        #####                                                 #",
    "######   #####                                           #######",
    "#        #                                                     #",
    "#  #######                                               #######",
    "#                                                              #",
    "#  ##                        #######             #######       #",
    "#      #######                                               ###",
    "#                                                              #",
    "#                                                              #",
    "#                                                              #",
    "#                                                              #",
    "#                                            #######           #",
    "#                   #######        #####                       #",
    "#                                                              #",
    "#                                                              #",
    "#                                                              #",
    "#                                                              #",
    "#      #######                     #######                     #",
    "#                            #####                             #",
    "#                                                              #",
    "#                                                              #",
    "#                                                              #",
    "#                                                              #",
    "#                  #######                                     #",
    "#                                                              #",
    "#                                                              #",
    "#                                           #######            #",
    "#                                                              #",
    "#                                                              #",
    "#                                                              #",
    "#                                                              #",
    "################################################################"
]

# CELL_WIDTH = 1920 // len(maze[0])
# CELL_HEIGHT = 1080 // len(maze)

CELL_HEIGHT = 30
CELL_WIDTH = 30

class Tile:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface, color):
        pygame.draw.rect(surface, color, self.rect)

def create_grid(tiles, cell_width, cell_height, maze_width, maze_height):
    grid_width = (maze_width + cell_width - 1) // cell_width
    grid_height = (maze_height + cell_height - 1) // cell_height
    grid = [[[] for _ in range(grid_width)] for _ in range(grid_height)]
    for tile in tiles:
        tile_x = min(int(tile.rect.x / cell_width), grid_width - 1)
        tile_y = min(int(tile.rect.y / cell_height), grid_height - 1)
        grid[tile_y][tile_x].append(tile)
    return grid


def draw_maze(surface, tiles):
    for tile in tiles:
        tile.draw(surface, white)
        
# Create tiles
tiles = []
for y, row in enumerate(maze):
    for x, cell in enumerate(row):
        if cell == "#":
            tiles.append(Tile(x * CELL_WIDTH, y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

# Create grid
grid = create_grid(tiles, CELL_WIDTH, CELL_HEIGHT, len(maze[0]) * CELL_WIDTH, len(maze) * CELL_HEIGHT)

                    
class vector():

    # constructor

    def __init__(self, x, y):  

        self.x = x

        self.y = y
       
 

    # add a second vector

    def add(self, v2):

        self.x += v2.x

        self.y += v2.y
   
 

    # subtract a second vector

    def sub(self, v2):
    
        self.x -= v2.x

        self.y -= v2.y

    

    # multiply the vector by a scalar value

    def scalar_mult(self, scalar):

        self.x *= scalar

        self.y *= scalar

 

    # returns the magnitude of the vector

    def get_mag(self):   

        return ((self.x**2) + (self.y**2))**0.5

    

    # normalise to a unit vector

    def normalise(self):

        mag = self.get_mag()

        if mag != 0:

            self.x *= (1/mag)

            self.y *= (1/mag)

        

    # sets the magnitude of the vector

    def set_mag(self, mag):

        self.normalise()

        self.scalar_mult(mag)

    

    # limits the magnitude of the vector

    def limit(self, lim):

        if self.get_mag() > lim:

            self.set_mag(lim)

    

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class Particle():

    def __init__(self, start_pos):

        self.pos = vector(start_pos[0], start_pos[1])

        self.vel = vector(0,0)

        self.accel = vector(0,0)
        
        self.mass = particle_mass
        self.damping_factor = particle_damping
 

        # create multiple fills

        # r = random.randint(1,2)

        # if r == 1:

        # self.fill = (random.randint(50,255),0,random.randint(50,255))
        # self.fill = (230,0,0)
        # self.fill = particle_color

        # else:

        #     self.fill = (0,0,random.randint(100,255))

        

        self.fill = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

        

 

    def update(self, vel, accel):

        self.vel.add(accel)

        self.vel.limit(c)

        self.pos.add(vel)

    

    def apply(self, force):

        self.accel.add(force)

    

    def reset_accel(self):

        self.accel.x = 0

        self.accel.y = 0

 

    def reset_vel(self):

        self.vel.x = 0

        self.vel.y = 0

 

    def reset_pos(self):

        self.pos.x = 400

        self.pos.y = 400    

 

    def draw(self):

        self.update(self.vel, self.accel)

        pygame.draw.circle(window, self.fill, (int(self.pos.x), int(self.pos.y)), 6)

        # pygame.draw.circle(window, (255,0,0), (int(self.pos.x), int(self.pos.y)), 1)
        
    def collide_with_planet(self, planet):
        # Calculate distance between particle and planet
        distance = ((self.pos.x - planet.pos.x) ** 2 + (self.pos.y - planet.pos.y) ** 2) ** 0.5
        combined_radius = 5 + planet.radius  # Adjust the radius as needed
        if distance < combined_radius:
            # Calculate penetration depth
            overlap = combined_radius - distance

            # Calculate direction from particle to planet
            direction = vector(planet.pos.x - self.pos.x, planet.pos.y - self.pos.y)
            direction.normalise()

            # Move particle away from planet
            self.pos.x -= direction.x * overlap
            self.pos.y -= direction.y * overlap

            # Reflect particle's velocity
            normal = vector(self.pos.x - planet.pos.x, self.pos.y - planet.pos.y)
            normal.normalise()
            dot_product = self.vel.x * normal.x + self.vel.y * normal.y
            self.vel.x -= 2 * dot_product * normal.x
            self.vel.y -= 2 * dot_product * normal.y
            
    def collide_with_particle(self, other):
        dx = other.pos.x - self.pos.x
        dy = other.pos.y - self.pos.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance < 12:  # Adjust collision radius considering the size of the particles
            angle = math.atan2(dy, dx)
            sine = math.sin(angle)
            cosine = math.cos(angle)

            # Calculate relative velocity
            rvx = other.vel.x - self.vel.x
            rvy = other.vel.y - self.vel.y

            # Calculate relative velocity in terms of the normal direction
            vel_normal = rvx * cosine + rvy * sine

            # If particles are moving apart, do not collide
            if vel_normal > 0:
                return

            # Calculate impulse scalar
            e = 0.7  # coefficient of restitution
            j = -(1 + e) * vel_normal
            j /= (1 / self.mass + 1 / other.mass)

            # Apply impulse
            impulse = vector(j * cosine, j * sine)
            self.vel.x -= impulse.x / self.mass
            self.vel.y -= impulse.y / self.mass
            other.vel.x += impulse.x / other.mass
            other.vel.y += impulse.y / other.mass

            # Separate particles to handle overlaps
            overlap = 12 - distance
            self.pos.x -= overlap * (dx / distance) / 2
            self.pos.y -= overlap * (dy / distance) / 2
            other.pos.x += overlap * (dx / distance) / 2
            other.pos.y += overlap * (dy / distance) / 2

    def collide_with_tiles(self, tiles, grid, cell_width, cell_height):
        grid_x = int(self.pos.x / cell_width)
        grid_y = int(self.pos.y / cell_height)
    
        # Check for collisions with adjacent tiles
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                x = grid_x + dx
                y = grid_y + dy
                if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
                    cell = grid[y][x]
                    for tile in cell:
                        if self.circle_rect_collision(self.pos.x, self.pos.y, 6, tile.rect):
                            self.resolve_collision_with_tile(tile)
    
        # Check for collisions with the current tile
        for tile in grid[grid_y][grid_x]:
            if self.circle_rect_collision(self.pos.x, self.pos.y, 6, tile.rect):
                self.resolve_collision_with_tile(tile)
    
    def resolve_collision_with_tile(self, tile):
        closest_x = clamp(self.pos.x, tile.rect.left, tile.rect.right)
        closest_y = clamp(self.pos.y, tile.rect.top, tile.rect.bottom)
    
        # Calculate the vector from the center of the circle to the closest point on the rectangle
        collision_normal_x = self.pos.x - closest_x
        collision_normal_y = self.pos.y - closest_y
    
        # If the circle is inside the rectangle, move it to the nearest edge
        if collision_normal_x ** 2 + collision_normal_y ** 2 < 6 ** 2:
            magnitude = math.sqrt(collision_normal_x ** 2 + collision_normal_y ** 2)
            if magnitude != 0:
                collision_normal_x = collision_normal_x / magnitude * 6 
                collision_normal_y = collision_normal_y / magnitude * 6
            self.pos.x = closest_x + collision_normal_x
            self.pos.y = closest_y + collision_normal_y
            
            # Move particle slightly further away to avoid detecting collision again
            epsilon = 0.1
            self.pos.x += collision_normal_x * epsilon
            self.pos.y += collision_normal_y * epsilon
    
        # Calculate the overlap between the circle and the rectangle
        overlap = 6 - math.sqrt(collision_normal_x ** 2 + collision_normal_y ** 2)
    
        # Resolve the collision by moving the particle away from the tile's edge
        self.pos.x += collision_normal_x * overlap
        self.pos.y += collision_normal_y * overlap
    
        # Check if the particle is moving away from the tile's surface
        dot_product = self.vel.x * collision_normal_x + self.vel.y * collision_normal_y
        if dot_product < 0:
            # Reflect velocity only if the particle is moving towards the tile's surface
            self.reflect_velocity(collision_normal_x, collision_normal_y)
    
    def reflect_velocity(self, collision_normal_x, collision_normal_y):
        # Calculate the dot product of velocity and collision normal
        dot_product = self.vel.x * collision_normal_x + self.vel.y * collision_normal_y
    
        # Check if the particle is moving towards the tile's surface
        if dot_product < 0:
            # Reflect the velocity vector
            self.vel.x -= 2 * dot_product * collision_normal_x
            self.vel.y -= 2 * dot_product * collision_normal_y
    
            # Normalize the velocity vector
            velocity_magnitude = math.sqrt(self.vel.x ** 2 + self.vel.y ** 2)
            if velocity_magnitude != 0:
                self.vel.x /= velocity_magnitude
                self.vel.y /= velocity_magnitude
        
    def circle_rect_collision(self, circle_pos_x, circle_pos_y, circle_radius, rect):
        # Calculate the closest point on the rectangle to the circle's center
        closest_x = clamp(circle_pos_x, rect.left, rect.right)
        closest_y = clamp(circle_pos_y, rect.top, rect.bottom)
    
        # Calculate the distance between the circle's center and the closest point
        distance_x = circle_pos_x - closest_x
        distance_y = circle_pos_y - closest_y
    
        # If the distance is less than the circle's radius, there's a collision
        return (distance_x ** 2 + distance_y ** 2) < (6 ** 2)




class Planet(Particle):
    def __init__(self, start_pos):
        super().__init__(start_pos)
        
        self.fill = planet_color
        self.radius = planet_radius

    def collide_with_particle(self, other):
        dx = other.pos.x - self.pos.x
        dy = other.pos.y - self.pos.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance < 12:  # Adjust collision radius considering the size of the particles
            angle = math.atan2(dy, dx)
            sine = math.sin(angle)
            cosine = math.cos(angle)

            # Calculate relative velocity
            rvx = other.vel.x - self.vel.x
            rvy = other.vel.y - self.vel.y

            # Calculate relative velocity in terms of the normal direction
            vel_normal = rvx * cosine + rvy * sine

            # If particles are moving apart, do not collide
            if vel_normal > 0:
                return

            # Calculate impulse scalar
            e = 0.7  # coefficient of restitution
            j = -(1 + e) * vel_normal
            j /= (1 / self.mass + 1 / other.mass)

            # Apply impulse to both particles
            impulse = vector(j * cosine, j * sine)
            self.vel.x -= impulse.x / self.mass
            self.vel.y -= impulse.y / self.mass
            other.vel.x += impulse.x / other.mass
            other.vel.y += impulse.y / other.mass

            # Separate particles based on their velocities
            overlap = 12 - distance
            self.pos.x -= overlap * (dx / distance) / 2 + self.vel.x / 10
            self.pos.y -= overlap * (dy / distance) / 2 + self.vel.y / 10
            other.pos.x += overlap * (dx / distance) / 2 + other.vel.x / 10
            other.pos.y += overlap * (dy / distance) / 2 + other.vel.y / 10
                
    def handle_collision_with_tiles(self, tiles):
        for tile in tiles:
            # Calculate the closest point on the perimeter of the tile to the planet's position
            closest_x = clamp(self.pos.x, tile.rect.left, tile.rect.right)
            closest_y = clamp(self.pos.y, tile.rect.top, tile.rect.bottom)
            
            # Calculate the distance between the planet and the closest point
            dx = self.pos.x - closest_x
            dy = self.pos.y - closest_y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            
            # If the distance is less than the planet's radius, adjust the position of the planet
            if distance < self.radius:
                if distance == 0:
                    # Planet is exactly on the perimeter, move it away by a small amount
                    self.pos.x += 1
                    self.pos.y += 1
                else:
                    # Calculate the overlap distance
                    overlap = self.radius - distance
                    
                    # Move the planet away from the tile along the vector between their centers
                    self.pos.x += overlap * (dx / distance)
                    self.pos.y += overlap * (dy / distance)

                    # Check if the planet is still inside the tile
                    if tile.rect.collidepoint(int(self.pos.x), int(self.pos.y)):
                        # Move the planet away from the tile based on the direction of the collision vector
                        self.pos.x += dx / distance
                        self.pos.y += dy / distance

                        # Ensure the planet remains outside the tile boundaries
                        self.pos.x = clamp(self.pos.x, tile.rect.left - self.radius, tile.rect.right + self.radius)
                        self.pos.y = clamp(self.pos.y, tile.rect.top - self.radius, tile.rect.bottom + self.radius)
            
    def draw(self):
        self.update(self.vel, self.accel)
        pygame.draw.circle(window, self.fill, (int(self.pos.x), int(self.pos.y)), planet_radius)  # Increase the radius (e.g., 20)
        
BACK_FILL = (0,0,0)

 
#Getting Acceleration

def calcAccel(radius):
        
        accel = (6.67*6*(10**2))/(radius**2)
        
        return accel*gravity_power

# window = pygame.display.set_mode((800,800))

window = pygame.display.set_mode((1920,1080), FULLSCREEN)

window.fill(BACK_FILL)

pygame.display.set_caption("Simple physics engine   |   By Ross The Boss And Nik The Bik 09 03 2021")

pygame.init()

mainClock = pygame.time.Clock()


# create a player dot

import random

players = [Particle((random.randint(0,1800),random.randint(0,1000))) for i in range(numberOfParticles)]

 

def draw():

    window.fill(BACK_FILL)

    for player in players:

        player.draw()
    planet.radius = planet_radius
    planet.draw()
    draw_maze(window, tiles)
    pygame.display.update()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
 

import time

run = True
spaceNotClicked = True
planet = Planet((960, 540))

# Hide the mouse cursor
pygame.mouse.set_visible(True)

# Define variable to store previous time
prev_time = time.time()
                                              
while run:

    # Calculate delta time
    current_time = time.time()
    dt = current_time - prev_time
    prev_time = current_time
    draw()
    
    for event in pygame.event.get():    

        if event.type == pygame.QUIT:

            run = False

        elif event.type == pygame.KEYDOWN:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    spaceNotClicked = not spaceNotClicked
                if event.key == pygame.K_x:
                    if planet_radius == 40:
                        planet_radius = 120
                    else:
                        planet_radius = 40

    # update the accel according to mouse pos

    mpos = pygame.mouse.get_pos()
    
    # Calculate the velocity based on the difference between current and previous cursor positions
    velocity_x = (mpos[0] - planet.pos.x) * drag_factor
    velocity_y = (mpos[1] - planet.pos.y) * drag_factor
    
    if velocity_x > 5:
        velocity_x = 5
    elif velocity_x < -5:
        velocity_x = -5
    if velocity_y > 5:
        velocity_y = 5
    elif velocity_y < -5:
        velocity_y = -5
        
    # Update the position of the planet based on the velocity
    planet.pos.x += velocity_x
    planet.pos.y += velocity_y
    
    planet.handle_collision_with_tiles(tiles)

          # Handle collision with window boundaries for the single planet
    if planet.pos.x <= 10:
        planet.vel.x = -planet.vel.x
        planet.pos.x = 12
    if planet.pos.x >= 1910:
        planet.vel.x = -planet.vel.x
        planet.pos.x = 1908
    if planet.pos.y <= 10:
        planet.vel.y = -planet.vel.y
        planet.pos.y = 12
    if planet.pos.y >= 1070:
        planet.vel.y = -planet.vel.y
        planet.pos.y = 1068

    for i, player in enumerate(players):
        
        player.collide_with_planet(planet)
        player.collide_with_tiles(tiles, grid, CELL_WIDTH, CELL_HEIGHT)
        
        if spaceNotClicked == True:
            player.accel = vector(planet.pos.x,planet.pos.y)
    
            player.accel.sub(player.pos)
            
            radius = ((abs(player.pos.x - planet.pos.x))**2+(abs(player.pos.y - planet.pos.y))**2)**0.5
            
            magnitude = calcAccel(radius)
    
            player.accel.set_mag(magnitude)
        
        else:
            player.reset_accel()
                # Check collisions between particles
        for other_player in players[i + 1:]:
            player.collide_with_particle(other_player)
    
    draw_text(str(mainClock.get_fps()), pygame.font.SysFont("comicsansms", 100), (255, 0, 0), window, 0, 0)
        
    mainClock.tick(60)
    

