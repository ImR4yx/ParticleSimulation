import pygame
# Constants for states
MENU = 0
SIMULATION = 1
current_state = MENU

def draw_start_menu(screen, width, background_color):
    screen.fill((30, 30, 30))  # Dark Grey
    font = pygame.font.SysFont('Arial', 40)
    title_font = pygame.font.SysFont('Arial', 60, bold=True)
    
    # Render text
    title_text = title_font.render("Particle Simulator", True, (255, 255, 255))
    start_text = font.render("Press SPACE to Start", True, (200, 200, 200))
    
    # Draw text to screen center
    screen.blit(title_text, (width//2 - title_text.get_width()//2, 200))
    screen.blit(start_text, (width//2 - start_text.get_width()//2, 350))
    
    pygame.display.flip()