import pygame
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import main_menu

# pygame setup
pygame.init()
WIDTH =  1920   #sets screen limits 
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Simulation v1.0")
TEXTFONT = pygame.font.SysFont("monospace", 17)
BLUE = (0,0,255) #Healthy Particle Color
RED = (255,0,0)  #Infected Particle Color
BACKGROUND_COLOR = (10, 10, 10)

#Parameters
PARTICLECOUNT = 1000
PARTICLERADIUS = 0.1
CELL_SIZE = PARTICLERADIUS*4    #Cell size for collision detection
infectionEnabled = True
colorchaosEnabled = True

class Particle:
    TIMESTEP = 3600
    G = 6.67428e-11 #gravitational constant

    def __init__(self, x, y, isInfected, x_vel, y_vel, color, mass, radius, isSun):
        self.x = x
        self.y = y
        self.isInfected = isInfected    #sets infection status of the particle -> red for infected
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.PARTICLERADIUS = PARTICLERADIUS
        self.color = color
        self.mass = mass 
        self.radius = radius
        self.isSun = isSun
        
    def draw(self, window):
        x = self.x       #makes sure, that the coordinate system is shifted from top left of the window to the center
        y = self.y
        pygame.draw.circle(window, self.color, (x,y), self.radius)  #function creates circle with sepcific parameters
            
    def update_position(self, sun):
        fx = 0
        fy = 0
        if self.x > WIDTH/2 + 20 or self.x < WIDTH/2 - 20:
            fx, fy = self.attraction(sun)
        if self.y > HEIGHT/2 + 20 or self.y < HEIGHT/2 - 20:
            fx, fy = self.attraction(sun)
        self.x_vel += fx / self.mass * self.TIMESTEP       #F=m*a and a=v/t -> v = F*t/m, but the t = TIMESTEP
        self.y_vel += fy / self.mass * self.TIMESTEP
        self.x += self.x_vel * self.TIMESTEP    #s = v*t -> calculates the distance the planet travels every frame
        self.y += self.y_vel * self.TIMESTEP

    def handle_collision(self):  #handles collision with screen walls
        if self.x > WIDTH-self.PARTICLERADIUS:
            self.x_vel = self.x_vel * -1    #changes x direction after hitting wall
            self.x -= 1                     #prevents gltiching into the wall
        if self.x < 0:
            self.x += 1
            self.x_vel = self.x_vel * -1
        if self.y > HEIGHT-self.PARTICLERADIUS:
            self.y_vel = self.y_vel * -1
            self.y -= 1
        if self.y < 0:
            self.y_vel = self.y_vel * -1
            self.y += 1

    def attraction(self, other):    #calculates the components of the resulting gravitational force
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x 
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)
        force = self.G * self.mass * other.mass / distance**2      #"straight line" force calculated with the gravity-force-formula   
        theta = math.atan2(distance_y, distance_x)              #angle is needed, in order to get the two force components of the straight line force
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
        
def main():
    #Startup Operations
    particles = []
    run = True
    clock = pygame.time.Clock()
    sun = Particle(WIDTH/2, HEIGHT/2, False, 0, 0, "yellow", 1000000, 20, True)
    particles.append(sun)
    #Gameloop 
    while run:
        clock.tick(120)                 #sets simulation to 30 frames per second
        screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #checks for quitting condition
                run = False
            if main_menu.current_state == main_menu.MENU:  #conditions for starting the simulation
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:     #waits for press of space key in order to start the simulation
                        main_menu.current_state = main_menu.SIMULATION
        if main_menu.current_state == main_menu.MENU:
            main_menu.draw_start_menu(screen, WIDTH, BACKGROUND_COLOR)
        elif main_menu.current_state == main_menu.SIMULATION:
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:
                # This code runs EVERY frame the button is held
                x, y = pygame.mouse.get_pos()
                print(f"Mouse is at: {x}, {y}")
                particles.append(Particle(x, y, False, 0, 0, "white", 100000000, 3, False))
            for particle in particles:     
                #print(f"x: {particle.x}, y: {particle.y}")  
                if particle.isSun == False:
                    particle.update_position(sun)  #updates position of the particles
                particle.draw(screen)       #draws the particle on the canvas again each frame with updated position 
            pygame.display.update() 
    pygame.quit()                       #ends the simulation
main()