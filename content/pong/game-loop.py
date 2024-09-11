import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colours
white = (255, 255, 255)  # White color
black = (0, 0, 0, 0)  # Black color

# Circle settings
circle_radius = 20
circle_x, circle_y = screen_width // 2, screen_height // 2  # Start at the center
circle_speed = 5  # Movement speed

clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get(pygame.KEYDOWN):
        if event.key == pygame.K_ESCAPE:
            running = False
        elif event.key == pygame.K_w:  # Move up
            circle_y -= circle_speed
        elif event.key == pygame.K_s:  # Move down
            circle_y += circle_speed
        elif event.key == pygame.K_a:  # Move left
            circle_x -= circle_speed
        elif event.key == pygame.K_d:  # Move right
            circle_x += circle_speed

    # Clear screen
    screen.fill(black)  # Black background

    # Draw the circle
    pygame.draw.circle(screen, white, (circle_x, circle_y), circle_radius)

    # Update the display
    pygame.display.flip()

    # Ensure the game runs at 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
