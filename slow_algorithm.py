import pygame
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import MainMenu


# pygame setup
pygame.init()
WIDTH =  1280   #sets screen limits 
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Simulation v1.0")
TEXTFONT = pygame.font.SysFont("monospace", 17)
BLUE = (0,0,255) #Healthy Particle Color
RED = (255,0,0)  #Infected Particle Color
BACKGROUND_COLOR = (50, 50, 50)

#Parameters
PARTICLECOUNT = 100
PARTICLERADIUS = 10
infectionEnabled = True
colorchaosEnabled = True

class Particle:
    TIMESTEP = 10

    def __init__(self, x, y, isInfected, x_vel, y_vel, color):
        self.x = x
        self.y = y
        self.isInfected = isInfected    #sets infection status of the particle -> red for infected
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.PARTICLERADIUS = PARTICLERADIUS
        self.color = color
        
    def draw(self, window):
        x = self.x       #makes sure, that the coordinate system is shifted from top left of the window to the center
        y = self.y
        pygame.draw.circle(window, self.color, (x,y), self.PARTICLERADIUS)  #function creates circle with sepcific parameters
            
    def update_position(self):
        self.x += self.x_vel * self.TIMESTEP    #s = v*t
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

def resolve_collision(p1, p2):
    # 1. Calculate distance between centers
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance = math.sqrt(dx**2 + dy**2)
    if distance < (p1.PARTICLERADIUS + p2.PARTICLERADIUS):  #checks for overlap of two particles
        nx = dx / distance  #calculates normal vectors of hit direction
        ny = dy / distance
        overlap = (p1.PARTICLERADIUS + p2.PARTICLERADIUS) - distance    #this unstucks the particles to prevent glitching by calculating the overlap
        p1.x -= nx * (overlap / 2)                                      #places the particle away from the other to make the collide and not stuck together
        p1.y -= ny * (overlap / 2)  
        p2.x += nx * (overlap / 2)
        p2.y += ny * (overlap / 2)
        p1.x_vel, p2.x_vel = p2.x_vel, p1.x_vel #swaps velocities to make them rebound
        p1.y_vel, p2.y_vel = p2.y_vel, p1.y_vel
        checkInfection(p1, p2)                  #checks for infection spreading
        
def checkInfection(p1, p2):
    if infectionEnabled == True:                            #Checks whether or not the user wants to deal with infections     
        if p1.isInfected:                                   #checks if one of the particle is infected and then passes the color and infection status to the other one
            p2.color = p1.color
            p1.isInfected= p2.isInfected = True
        if p2.isInfected:
            p1.color= p2.color
            p1.isInfected= p2.isInfected = True

def plot_complex_history(history):                          #function plots the number of particles in a diagramm with matching color codes
    plt.figure(figsize=(12, 8))
    for color, counts in history.items():
        normalized_color = tuple(c / 255 for c in color)    #convert 0-255 to 0-1.0 for matplotlib
        plt.plot(counts, color=normalized_color, linewidth=1, alpha=0.7)
    plt.title(f"Population of {PARTICLECOUNT} Unique Particle Colors")   #plot title
    plt.xlabel("Time (Snapshots)")                          #x-axis label
    plt.ylabel("Count")                                     #y-axis label
    plt.show()                                              #shows plot
        

def main():
    #Startup Operations
    particles = []
    colors = np.zeros((1000, 3))                    #creates an array with 1000 rows and 3 cols with 0 as input
    if colorchaosEnabled == False:                  
        for i in range(PARTICLECOUNT-1):
            x = random.randrange(10, WIDTH-10, 1)       
            y = random.randrange(10, HEIGHT-10, 1)
            xdir = random.uniform(-1, 1)            #uniform returns a decimal number between the depicted range
            ydir = random.uniform(-1, 1)
            particles.append(Particle(x, y, False, xdir, ydir, BLUE))   #appends the new particle to array particles[]
        if infectionEnabled == True:                #creates red particle if infection is enabled
            particles.append(Particle(0,0, True, 1, 1, RED))            #creates the one infected particle
    if colorchaosEnabled:   
        for i in range(PARTICLECOUNT):
            x = random.randrange(10, WIDTH-10, 1)       #sets random x and y coordinates
            y = random.randrange(10, HEIGHT-10, 1)
            xdir = random.uniform(-1, 1)            #sets starting direction of particles
            ydir = random.uniform(-1, 1)
            redColor = random.randrange(0, 255, 1)  #randomly generates color codes for the particles
            greenColor = random.randrange(0, 255, 1)
            blueColor = random.randrange(0, 255, 1)
            colors[i] = [redColor, greenColor, blueColor]   #saves the different color codes in colors array
            particles.append(Particle(x, y, True, xdir, ydir, (redColor, greenColor, blueColor)))
        
    run = True
    clock = pygame.time.Clock()    
    frame_count = 0     
    history = {}                      #creates the dictionary for the color codes and their value (R,G,B): amount
    for p in particles:               #creates dictionary entry for each color, -> color code: 0
        if p.color not in history:
            history[p.color] = []

    #Gameloop 
    while run:
        clock.tick(30)                 #sets simulation to 30 frames per second
        frame_count += 1               #+1 for every frame
        if frame_count % 10 == 0:      #every 10 frames an input is given to the dictionary
            current_counts = {color: 0 for color in history.keys()} #temporary amounts of particles of a color are stored in here
            for p in particles:
                current_counts[p.color] += 1    #for every particle of a specfici color 1 is added to the amount
            for color, count in current_counts.items(): 
                history[color].append(count)
        screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #checks for quitting condition
                run = False
            if MainMenu.current_state == MainMenu.MENU:  #conditions for starting the simulation
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:     #waits for press of space key in order to start the simulation
                        MainMenu.current_state = MainMenu.SIMULATION
        if MainMenu.current_state == MainMenu.MENU:
            MainMenu.draw_start_menu(screen, WIDTH, BACKGROUND_COLOR)
        elif MainMenu.current_state == MainMenu.SIMULATION:
            for i in range(len(particles)):  #loop for detecting collisions between the particles
                for j in range(i + 1, len(particles)):
                    p1 = particles[i]
                    p2 = particles[j]
                    resolve_collision(p1, p2)
            for particle in particles:       
                particle.update_position()  #updates position of the particles
                particle.handle_collision() #handles collision with screen borders
                particle.draw(screen)       #draws the particle on the canvas again each frame with updated position 
            pygame.display.update() 
    plot_complex_history(history)       #calls the plot function to plot the amount of particles of different colors
    pygame.quit()                       #ends the simulation
main()




        