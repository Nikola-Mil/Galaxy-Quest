# -*- coding: utf-8 -*-
"""
Created on Wed May  5 14:49:20 2021

@author: ROSS THE BOSS & NIK THE BIK
"""

import math

import pygame, sys
from pygame.locals import *
import random
from button import Button


fun_facts = [
    "Fun Fact: Did you know that Jupiter, the largest planet in our solar system, has a giant storm called the Great Red Spot? It's been raging for at least 400 years!",
    "Space Phenomenon: Quasars are incredibly bright and distant objects in space, powered by supermassive black holes. Some quasars emit as much energy as a trillion stars!",
    "Fun Fact: Earth is the only known planet where life exists. Its atmosphere, water, and distance from the Sun make it the perfect habitat for diverse forms of life.",
    "Space Phenomenon: Black holes are regions in space where gravity is so strong that nothing, not even light, can escape. They form when massive stars collapse at the end of their life cycle.",
    "Fun Fact: Saturn, famous for its beautiful rings, is not the only planet with rings. Jupiter, Uranus, and Neptune also have rings, although they are much fainter and less prominent.",
    "Space Phenomenon: Meteors, also known as shooting stars, are pieces of rock or metal that burn up upon entering Earth's atmosphere. They create streaks of light that we can see from the ground."
]

c = 0.5*(10)
gravity_power = 0.5
particle_color = (255,255,0)
planet_color = (255, 0, 0)         
numberOfParticles = 20
numberOfMeteors = 5
numberOfBosses = 1
friction_coefficient = 0.60
particle_mass = 1
particle_damping = 0.80
planet_radius = 40
white = (255, 255, 255)
drag_factor = 0.05
planet_velocity = [0, 0]
boss_alive = True

maze = [
    "################################################################",
    "#                                                              #",
    "#                                                              #",
    "#                                                       ########",
    "#      ##################################                      #",
    "########                                                       #",
    "#                                                              #",
    "#                                                        #######",
    "#                                                              #",
    "#                            #######             #######       #",
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

CELL_HEIGHT = 30
CELL_WIDTH = 30

class Tile:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.left_adjacent = False
        self.right_adjacent = False
        self.top_adjacent = False
        self.bottom_adjacent = False
        
    def set_adjacent_tiles(self, left, right, top, bottom):
        self.left_adjacent = left
        self.right_adjacent = right
        self.top_adjacent = top
        self.bottom_adjacent = bottom

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
    
class Meteor:
    def __init__(self, start_pos):
        self.pos = vector(start_pos[0], start_pos[1])
        self.vel = vector(0, 0)
        self.accel = vector(0, 0)  # Ensure self.accel is initialized
        self.radius = 20  # Adjust the radius as needed
        self.fill = (100, 233, 112)  # Adjust the color as needed
        self.target = None
        self.speed = 1  # Adjust the speed as needed
        self.damage = 10  # Adjust the damage as needed
        self.health = 20

    def update(self, vel, accel):
        self.vel.add(accel)
        self.vel.limit(c)
        self.pos.add(vel)

    def draw(self):
        self.update(self.vel, self.accel)
        pygame.draw.circle(window, self.fill, (int(self.pos.x), int(self.pos.y)), self.radius)

    def collide_with_planet(self, planet):
        # Calculate distance between meteor and planet
        distance = ((self.pos.x - planet.pos.x) ** 2 + (self.pos.y - planet.pos.y) ** 2) ** 0.5
        combined_radius = self.radius + planet.radius  # Adjust the radius as needed
        if distance < combined_radius:
            # Apply damage to the planet
            planet.health -= self.damage
            return True
        return False
    
    
    def update(self, vel, accel):

        self.vel.add(accel)

        self.vel.limit(c)

        self.pos.add(vel)


    def draw(self):
        self.update(self.vel, self.accel)
        pygame.draw.circle(window, self.fill, (int(self.pos.x), int(self.pos.y)), self.radius)


        
    def collide_with_particle(self, particle):
        distance = ((self.pos.x - particle.pos.x) ** 2 + (self.pos.y - particle.pos.y) ** 2) ** 0.5
        combined_radius = self.radius + 6  # Adjust the radius as needed
        
        # Adjust the threshold based on your requirements
        if distance < combined_radius:
            return True
        return False
    
    def detect_and_resolve_tile_collision(self, tiles):
        for tile in tiles:
            if self.collision_with_tile(tile):
                self.resolve_collision_with_tile(tile)

    def collision_with_tile(self, tile):
        dx = self.pos.x - max(tile.rect.left, min(self.pos.x, tile.rect.right))
        dy = self.pos.y - max(tile.rect.top, min(self.pos.y, tile.rect.bottom))

        if abs(dx) < self.radius and abs(dy) < self.radius:
            return True
        return False

    def resolve_collision_with_tile(self, tile):
        # Calculate distance between particle center and tile edges
        dx = self.pos.x + self.radius + 10 - max(tile.rect.left, min(self.pos.x, tile.rect.right))
        dy = self.pos.y + self.radius + 10 - max(tile.rect.top, min(self.pos.y, tile.rect.bottom))
    
        # Determine collision side
        if abs(dx) < abs(dy):
            # Collided horizontally
            if dx < 0:
                # Collided from the left  
                if tile.right_adjacent:
                    # Ignore collision if there's a tile on the right
                    return
                self.vel.x *= -1  # Reverse horizontal velocity
            else:
                # Collided from the right
                if tile.left_adjacent:
                    # Ignore collision if there's a tile on the left
                    return
                self.vel.x *= -1  # Reverse horizontal velocity
        else:
            # Collided vertically
            if dy < 0:
                # Collided from the top
                if tile.bottom_adjacent:
                    # Ignore collision if there's a tile on the bottom
                    return
                self.vel.y *= -1  # Reverse vertical velocity
            else:
                # Collided from the bottom
                if tile.top_adjacent:
                    # Ignore collision if there's a tile on the top
                    return
                self.vel.y *= -1  # Reverse vertical velocity
    
        # Move particle to avoid overlap
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
    
class Bullet:
    def __init__(self, pos, angle, speed):
        self.pos = vector(pos.x, pos.y)
        self.vel = vector(speed * math.cos(angle), speed * math.sin(angle))
        self.radius = 10  # Adjust bullet size as needed
        self.fill = (255, 0, 0)  # Adjust bullet color as needed

    def update(self):
        # Update bullet position based on velocity
        self.pos.add(self.vel)

    def draw(self):
        # Draw the bullet on the screen
        pygame.draw.circle(window, self.fill, (int(self.pos.x), int(self.pos.y)), self.radius)

class BossEnemy:
    def __init__(self):
        self.pos = vector(1800, 1000)  # Position at the bottom right of the map
        self.vel = vector(0, 0)
        self.accel = vector(0, 0)
        self.radius = 40  # Adjust size as needed
        self.fill = (50, 50, 255)  # Adjust color as needed
        self.health = 10 # Adjust health as needed
        self.damage = 100
        self.shoot_interval = 50  # Adjust shooting interval as needed
        self.shoot_timer = self.shoot_interval  # Timer to track shooting intervals
    
    def update(self):
        # Add any update logic here, such as movement or AI behavior
        self.move_randomly()
        self.update_bullets()
        
    def draw(self):
        pygame.draw.circle(window, self.fill, (int(self.pos.x), int(self.pos.y)), self.radius)

    def shoot_bullet(self, player):
        # Implement bullet shooting logic here
        bullet_angle = math.atan2(player.pos.y - self.pos.y, player.pos.x - self.pos.x)
        bullet_speed = 5  # Adjust bullet speed as needed
        bullet = Bullet(self.pos, bullet_angle, bullet_speed)
        return bullet

    def move_randomly(self):
        # Move randomly within a certain range
        if random.randint(0, 100) < 5:  # Adjust probability of changing direction
            self.accel.x = random.uniform(-1, 1)  # Adjust the range of acceleration
            self.accel.y = random.uniform(-1, 1)  # Adjust the range of acceleration

        # Update velocity based on acceleration
        self.vel.add(self.accel)

        # Limit velocity to a maximum value (optional)
        max_speed = 5  # Adjust maximum speed as needed
        self.vel.limit(max_speed)

        # Update position based on velocity
        self.pos.add(self.vel)

        # Reset acceleration
        self.accel.scalar_mult(0)
        
    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.update()
            # Remove bullets that are off-screen
            if bullet.pos.x < 0 or bullet.pos.x > 1920 or bullet.pos.y < 0 or bullet.pos.y > 1080:
                self.bullets.remove(bullet)

    def collide_with_particle(self, particle):
        distance = ((self.pos.x - particle.pos.x) ** 2 + (self.pos.y - particle.pos.y) ** 2) ** 0.5
        combined_radius = self.radius + 6  # Adjust the radius as needed
        
        # Adjust the threshold based on your requirements
        if distance < combined_radius:
            return True
        return False

    def collide_with_planet(self, planet):
        distance = ((self.pos.x - planet.pos.x) ** 2 + (self.pos.y - planet.pos.y) ** 2) ** 0.5
        combined_radius = self.radius + planet.radius  # Adjust the radius as needed
        if distance < combined_radius:
            # Apply damage to the planet
            planet.health -= self.damage
            return True
        return False

boss_enemy = BossEnemy()

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
    
    def detect_and_resolve_tile_collision(self, tiles):
        for tile in tiles:
            if self.collision_with_tile(tile):
                self.resolve_collision_with_tile(tile)

    def collision_with_tile(self, tile):
        dx = self.pos.x - max(tile.rect.left, min(self.pos.x, tile.rect.right))
        dy = self.pos.y - max(tile.rect.top, min(self.pos.y, tile.rect.bottom))

        if abs(dx) < 6 and abs(dy) < 6:
            return True
        return False

    def resolve_collision_with_tile(self, tile):
        # Calculate distance between particle center and tile edges
        dx = self.pos.x + 6 - max(tile.rect.left, min(self.pos.x, tile.rect.right))
        dy = self.pos.y + 6 - max(tile.rect.top, min(self.pos.y, tile.rect.bottom))
    
        # Determine collision side
        if abs(dx) < abs(dy):
            # Collided horizontally
            if dx < 0:
                # Collided from the left  
                if tile.right_adjacent:
                    # Ignore collision if there's a tile on the right
                    return
                self.vel.x *= -1  # Reverse horizontal velocity
            else:
                # Collided from the right
                if tile.left_adjacent:
                    # Ignore collision if there's a tile on the left
                    return
                self.vel.x *= -1  # Reverse horizontal velocity
        else:
            # Collided vertically
            if dy < 0:
                # Collided from the top
                if tile.bottom_adjacent:
                    # Ignore collision if there's a tile on the bottom
                    return
                self.vel.y *= -1  # Reverse vertical velocity
            else:
                # Collided from the bottom
                if tile.top_adjacent:
                    # Ignore collision if there's a tile on the top
                    return
                self.vel.y *= -1  # Reverse vertical velocity
    
        # Move particle to avoid overlap
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

class Planet(Particle):
    def __init__(self, start_pos):
        super().__init__(start_pos)
        
        self.fill = planet_color
        self.radius = planet_radius
        self.health = 100  # Initial health value for the planet

    def collide_with_meteor(self, meteor):
        # Calculate distance between meteor and planet
        distance = ((self.pos.x - meteor.pos.x) ** 2 + (self.pos.y - meteor.pos.y) ** 2) ** 0.5
        combined_radius = self.radius + meteor.radius  # Adjust the radius as needed
        if distance < combined_radius:
            # Reduce the planet's health upon collision with a meteor
            self.health -= meteor.damage

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

pygame.display.set_caption("Galaxy Quest")

pygame.init()

mainClock = pygame.time.Clock()

# create a player dot

import random

players = [Particle((random.randint(0,1800),random.randint(0,1000))) for i in range(numberOfParticles)]
meteors = [Meteor([random.randint(0,1800), random.randint(0,1000)]) for i in range(numberOfMeteors)]
bosses = [BossEnemy() for i in range(numberOfBosses)]
bullets = []

import math
import random
import pygame, sys
from pygame.locals import *


def draw():
    window.fill(BACK_FILL)

    for player in players:
        player.draw()
    for meteor in meteors:
        meteor.draw()
    for boss in bosses:
        boss_enemy.draw()
    for bullet in bullets:
        bullet.update()
        bullet.draw()


    planet.radius = planet_radius
    planet.draw()
    draw_maze(window, tiles)
    #ovo je za crtanje hp
    font = pygame.font.Font(None, 36)
    draw_text(f'Health: {planet.health}', font, white, window, 40, 40)

    pygame.display.update()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

import time

planet = Planet((960, 540))

def game():
    
    count = -1
    while count < len(tiles):
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == "#":
                    count += 1
                    tile = tiles[count]
                left_adjacent = False
                right_adjacent = False
                top_adjacent = False
                bottom_adjacent = False
        
                # Check if there are adjacent tiles to the left, right, top, and bottom
                if j > 0:
                    left_adjacent = maze[i][j - 1] == "#"
                if j < len(maze[0]) - 1:
                    right_adjacent = maze[i][j + 1] == "#"
                if i > 0:
                    top_adjacent = maze[i - 1][j] == "#"
                if i < len(maze) - 1:
                    bottom_adjacent = maze[i + 1][j] == "#"
        
                # Set adjacent tiles for the current tile
                tile.set_adjacent_tiles(left_adjacent, right_adjacent, top_adjacent, bottom_adjacent)
        count += 1

    
    run = True
    spaceNotClicked = True
    # Define variable to store previous time
    prev_time = time.time()
    # # Hide the mouse cursor
    # pygame.mouse.set_visible(False)
    
    planet_radius = 40
    
    while run:
        
        if planet.health <= 0:
            run = False
            pygame.quit()
            sys.exit()
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
                        pause()
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
    
        for meteor in meteors[:]:
            meteor.detect_and_resolve_tile_collision(tiles)
            if meteor.collide_with_planet(planet):
                meteors.remove(meteor)
            else:
                meteor.accel = vector(planet.pos.x, planet.pos.y)
                meteor.accel.sub(meteor.pos)
                radius = ((abs(meteor.pos.x - planet.pos.x)) ** 2 + (abs(meteor.pos.y - planet.pos.y)) ** 2) ** 0.5
                magnitude = calcAccel(radius)
                meteor.accel.set_mag(magnitude)
    
        for boss in bosses[:]:
            if boss.collide_with_planet(planet):
                bosses.remove(boss)
            else:
                boss.accel = vector(mpos[0], mpos[1])
                boss.accel.sub(boss.pos)
                radius = ((abs(boss.pos.x - mpos[0])) ** 2 + (abs(boss.pos.y - mpos[1])) ** 2) ** 0.5
                magnitude = calcAccel(radius)
                boss.accel.set_mag(magnitude)
    
        for bullet in bullets[:]:
            distance = ((bullet.pos.x - planet.pos.x) ** 2 + (bullet.pos.y - planet.pos.y) ** 2) ** 0.5
            combined_radius = bullet.radius + planet.radius  # Adjust the radius as needed
            if distance < combined_radius:
                # Reduce the planet's health upon bullet impact
                planet.health -= 10  # Adjust the damage as needed
                # Remove the bullet from the list
                bullets.remove(bullet)
            else:
                bullet.update()
                bullet.draw()
        # Check for collisions with enemies or other objects
        # Remove bullets that are off-screen
            if bullet.pos.x < 0 or bullet.pos.x > 1920 or bullet.pos.y < 0 or bullet.pos.y > 1080:
                bullets.remove(bullet)
        
    
        for i, player in enumerate(players):
            player.collide_with_planet(planet)
            # Check for collisions with tiles
            player.detect_and_resolve_tile_collision(tiles)
            
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
                
        for meteor in meteors[:]:
            for player in players:
                if meteor.collide_with_particle(player):
                    meteor.health -= player.vel.get_mag() * 2
                    if meteor.health <= 0:
                        meteors.remove(meteor)
                    players.remove(player)
                    break
        for boss in bosses[:]:
            if boss.shoot_timer <= 0:
                # Shoot a bullet
                new_bullet = boss.shoot_bullet(planet)
                # Add the bullet to the list
                bullets.append(new_bullet)
                # Reset the shoot timer
                boss.shoot_timer = boss.shoot_interval
            else:
                # Decrease the shoot timer
                boss.shoot_timer -= 1
            for player in players:
                if boss:
                    if boss.collide_with_particle(player):
                        boss.health -= player.vel.get_mag() * 2
                        if boss.health <= 0:
                            bosses.remove(boss)
                            fun_fact = random.choice(fun_facts)
                            # Display the fun fact on the screen
                            draw_text(fun_fact, pygame.font.SysFont("comicsansms", 20), (255, 0, 0), window, 100, 100)
                            pygame.display.update()
                            pygame.time.delay(5000)  # Display the fun fact for 5 seconds before resuming the game loop
                            bosses.remove(boss)  # Remove the defeated boss from the list
                        players.remove(player)
                    
        draw_text(str(mainClock.get_fps()), pygame.font.SysFont("comicsansms", 100), (255, 0, 0), window, 0, 0)
        mainClock.tick(60)

SCREEN = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/wp7872665.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        
        SCREEN.blit(BG,(0,0))

        OPTIONS_TEXT = get_font(65).render("Choose Difficulty", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(960, 370))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        EASY_BUTTON = Button(image=None, pos=(960, 500), 
                            text_input="Easy", font=get_font(55), base_color="White", hovering_color="#d7fcd4")
        NORMAL_BUTTON = Button(image=None, pos=(960, 600), 
                            text_input="Normal", font=get_font(55), base_color="White", hovering_color="#d7fcd4")
        HARD_BUTTON = Button(image=None, pos=(960, 700), 
                            text_input="Hard", font=get_font(55), base_color="White", hovering_color="#d7fcd4")


        OPTIONS_BACK = Button(image=None, pos=(960, 850), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="#d7fcd4")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        EASY_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        NORMAL_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        HARD_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        EASY_BUTTON.update(SCREEN)
        NORMAL_BUTTON.update(SCREEN)
        HARD_BUTTON.update(SCREEN)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    # Set the difficulty level to easy
                    print("Easy difficulty selected")
                if NORMAL_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    # Set the difficulty level to normal
                    print("Normal difficulty selected")
                if HARD_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    # Set the difficulty level to hard
                    print("Hard difficulty selected")
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(90).render("Galaxy Quest", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(960, 300))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Novi_play_backround.png"), pos=(960, 500), 
                            text_input="PLAY", font=get_font(75), base_color="White", hovering_color="#d7fcd4")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Button_Difficulty_Backround.png"), pos=(960, 650), 
                            text_input="DIFFICULTY", font=get_font(75), base_color="White", hovering_color="#d7fcd4")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Novi_quit_backround.png"), pos=(960, 800), 
                            text_input="QUIT", font=get_font(75), base_color="White", hovering_color="#d7fcd4")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    game()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def game_over():
    while True:
        GAME_OVER_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        GAME_OVER_TEXT = get_font(100).render("GAME OVER", True, "Red")
        GAME_OVER_RECT = GAME_OVER_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(GAME_OVER_TEXT, GAME_OVER_RECT)

        GAME_OVER_RETRY = Button(image=None, pos=(640, 460),
                                text_input="RETRY", font=get_font(75), base_color="White", hovering_color="Green")

        GAME_OVER_RETRY.changeColor(GAME_OVER_MOUSE_POS)
        GAME_OVER_RETRY.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if GAME_OVER_RETRY.checkForInput(GAME_OVER_MOUSE_POS):
                    play()

        pygame.display.update()

def pause():
    while True:
        PAUSE_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PAUSE_TEXT = get_font(100).render("PAUSED", True, "White")
        PAUSE_RECT = PAUSE_TEXT.get_rect(center=(960, 400))
        SCREEN.blit(PAUSE_TEXT, PAUSE_RECT)

        PAUSE_RESUME = Button(image=None, pos=(960, 550),
                                text_input="RESUME", font=get_font(75), base_color="White", hovering_color="Green")

        PAUSE_QUIT = Button(image=None, pos=(960, 650),
                                text_input="QUIT", font=get_font(75), base_color="White", hovering_color="Red")

        PAUSE_RESUME.changeColor(PAUSE_MOUSE_POS)
        PAUSE_QUIT.changeColor(PAUSE_MOUSE_POS)
        PAUSE_RESUME.update(SCREEN)
        PAUSE_QUIT.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PAUSE_RESUME.checkForInput(PAUSE_MOUSE_POS):
                    return
                if PAUSE_QUIT.checkForInput(PAUSE_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
    
