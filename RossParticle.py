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
    "#                   #######                                    #",
    "#                                                              #",
    "#                                                              #",
    "#                                                              #",
    "#                                                              #",
    "#      #######                     #######                     #",
    "#                                                              #",
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

        for y in range(max(0, grid_y - 1), min(len(grid), grid_y + 2)):
            for x in range(max(0, grid_x - 1), min(len(grid[0]), grid_x + 2)):
                cell = grid[y][x]
                for tile in cell:
                    if (tile.rect.left <= self.pos.x <= tile.rect.right) and (tile.rect.top <= self.pos.y <= tile.rect.bottom):
                        self.resolve_collision_with_tile(tile)

    def resolve_collision_with_tile(self, tile):
        overlap_x = min(abs(self.pos.x - tile.rect.left), abs(self.pos.x - tile.rect.right))
        overlap_y = min(abs(self.pos.y - tile.rect.top), abs(self.pos.y - tile.rect.bottom))

        if overlap_x < overlap_y:
            if self.pos.x < tile.rect.centerx:
                self.pos.x -= overlap_x
            else:
                self.pos.x += overlap_x
            self.vel.x *= -1
        else:
            if self.pos.y < tile.rect.centery:
                self.pos.y -= overlap_y
            else:
                self.pos.y += overlap_y
            self.vel.y *= -1



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

tiles = []
for y, row in enumerate(maze):
    for x, cell in enumerate(row):
        if cell == "#":
            tiles.append(Tile(x * CELL_WIDTH, y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))


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
    
    # Update the position of the planet to follow the cursor

    planet.pos.x = mpos[0]
    planet.pos.y = mpos[1]

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
            player.accel = vector(mpos[0],mpos[1])
    
            player.accel.sub(player.pos)
            
            radius = ((abs(player.pos.x - mpos[0]))**2+(abs(player.pos.y - mpos[1]))**2)**0.5
            
            magnitude = calcAccel(radius)
    
            player.accel.set_mag(magnitude)
        
        else:
            player.reset_accel()
                # Check collisions between particles
        for other_player in players[i + 1:]:
            player.collide_with_particle(other_player)
    
#================= COLLISIONS ==========================
        if player.pos.x <= 10:
            if abs(player.vel.x) > 1.6:
                player.vel = vector(-player.vel.x - 0.5, player.vel.y)
            else:
                player.vel = vector(-player.vel.x, player.vel.y)
            player.pos.x = 12
        if player.pos.x >= 1900:
            if abs(player.vel.x) > 1.6:
                player.vel = vector(-player.vel.x + 0.5, player.vel.y)
            else:
                player.vel = vector(-player.vel.x, player.vel.y)
            player.pos.x = 1898
        if player.pos.y <= 10:
            if abs(player.vel.y) > 1.6:
                player.vel = vector(player.vel.x, -player.vel.y - 0.5)
            else:
                player.vel = vector(player.vel.x, -player.vel.y)
            player.pos.y = 12
        if player.pos.y >= 1050:
            if abs(player.vel.y) > 1.6:
                player.vel = vector(player.vel.x, -player.vel.y + 1)
            else:
                player.vel = vector(player.vel.x, -player.vel.y)
            player.pos.y = 1048
        
        if player.pos.x > 2000 or player.pos.x < -20 or player.pos.y > 1100 or player.pos.y < -20:
            print("OUT OF BOUNDS")  
# ===========================================================
    draw_text(str(mainClock.get_fps()), pygame.font.SysFont("comicsansms", 100), (255, 0, 0), window, 0, 0)
        
    mainClock.tick(60)
    

