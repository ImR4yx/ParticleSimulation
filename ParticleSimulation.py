import pygame
import math
import random
import numpy as np
import matplotlib.pyplot as plt

# pygame setup
pygame.init()
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
TEXTFONT = pygame.font.SysFont("monospace", 17)
BLUE = (0,0,255) #Healthy Particle Color
RED = (255,0,0)  #Infected Particle Color
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
    # Check if they are actually overlapping
    if distance < (p1.PARTICLERADIUS + p2.PARTICLERADIUS):
        # 2. Calculate the "Normal" vector (direction of the hit)
        nx = dx / distance
        ny = dy / distance
        # 3. Static Resolution: Separate them to prevent "stuck" particles
        overlap = (p1.PARTICLERADIUS + p2.PARTICLERADIUS) - distance
        p1.x -= nx * (overlap / 2)
        p1.y -= ny * (overlap / 2)
        p2.x += nx * (overlap / 2)
        p2.y += ny * (overlap / 2)
        # 4. Dynamic Resolution: Swap velocities (The Bounce)
        # We swap the components to make them rebound
        p1.x_vel, p2.x_vel = p2.x_vel, p1.x_vel
        p1.y_vel, p2.y_vel = p2.y_vel, p1.y_vel
        checkInfection(p1, p2)
        
def checkInfection(p1, p2):
    if infectionEnabled == True: #Checks whether or not the user wants to deal with infections     
        if p1.isInfected:
            p2.color = p1.color
            p1.isInfected= p2.isInfected = True
        if p2.isInfected:
            p1.color= p2.color
            p1.isInfected= p2.isInfected = True

def plot_complex_history(history):  #function plots the number of particles in a diagramm with matching color codes
    plt.figure(figsize=(12, 8))
    for color, counts in history.items():
        # Convert (255, 255, 255) to (1.0, 1.0, 1.0) for Matplotlib
        normalized_color = tuple(c / 255 for c in color)
        plt.plot(counts, color=normalized_color, linewidth=1, alpha=0.7)
    plt.title("Population of 200 Unique Particle Colors")
    plt.xlabel("Time (Snapshots)")
    plt.ylabel("Count")
    plt.show()
        

def main():
    #Startup Operations
    particles = []
    colors = np.zeros((1000, 3))    #creates an array with 1000 rows and 3 cols with 0 as input
    color_count = np.zeros(PARTICLECOUNT)
    if colorchaosEnabled == False:
        for i in range(PARTICLECOUNT-1):
            x = random.randrange(10, 1270, 1)
            y = random.randrange(10, 710, 1)
            xdir = random.uniform(-1, 1)
            ydir = random.uniform(-1, 1)
            particles.append(Particle(x, y, False, xdir, ydir, BLUE))
        if infectionEnabled == True: #creates red particle if infection is enabled
            particles.append(Particle(0,0, True, 1, 1, RED))
    if colorchaosEnabled:
        for i in range(PARTICLECOUNT):
            x = random.randrange(10, 1270, 1)   #sets random x and y coordinates
            y = random.randrange(10, 710, 1)
            xdir = random.uniform(-1, 1)        #sets starting direction of particles
            ydir = random.uniform(-1, 1)
            redColor = random.randrange(0, 255, 1)  #randomly generates color codes for the particles
            greenColor = random.randrange(0, 255, 1)
            blueColor = random.randrange(0, 255, 1)
            colors[i] = [redColor, greenColor, blueColor]   #saves the different color codes in colors array
            particles.append(Particle(x, y, True, xdir, ydir, (redColor, greenColor, blueColor)))
        
    run = True
    clock = pygame.time.Clock()    
    frame_count = 0     
    # This will look like: {(R, G, B): [count1, count2, ...]}
    history = {}     #creates the dictionary for the color codes and their value
    # Initialize the dictionary for each particle's unique color
    for p in particles:
        if p.color not in history:
            history[p.color] = []

    #Gameloop 
    while run:
        clock.tick(30)
        frame_count += 1
        if frame_count % 10 == 0:
        # 1. Create a temporary counter for THIS frame
            current_counts = {color: 0 for color in history.keys()}
        # 2. Count who is still "alive" or present
            for p in particles:
                current_counts[p.color] += 1
            # 3. Append these counts to our long-term history
            for color, count in current_counts.items():
                history[color].append(count)

        screen.fill((50, 50, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        num_particles = len(particles)
        for i in range(num_particles):
            for j in range(i + 1, num_particles):
                # Now you compare particle i with particle j
                p1 = particles[i]
                p2 = particles[j]
                resolve_collision(p1, p2)
        for particle in particles:      
            particle.update_position()
            particle.handle_collision()
            particle.draw(screen)
        # Assuming your particles are stored in a list called 'particles'
        pygame.display.update() 
    plot_complex_history(history)
    pygame.quit()
main()




        