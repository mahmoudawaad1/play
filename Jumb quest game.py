import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer for sound
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Player settings
player_size = 100
player_speed = 5
player_velocity_y = 0
gravity = 1
jump_power = 20  # Consistent jump power
is_jumping = False
jump_cooldown = False  # Cooldown to ensure only taps register

# Platform settings
platform_width = 200
platform_height = 20
platforms = [pygame.Rect(300, SCREEN_HEIGHT - 50, platform_width, platform_height)]

# Load images with error handling
try:
    player_image = pygame.image.load(r'C:\Users\Nour\Desktop\Programming pictures\Mr ninja.png')
    player_image = pygame.transform.scale(player_image, (player_size, player_size))
except pygame.error:
    print("Error loading player image")

try:
    background_image = pygame.image.load(r'C:\Users\Nour\Desktop\Programming pictures\sky 2D.png')
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error:
    print("Error loading background image")

try:
    platform_image = pygame.image.load(r'C:\Users\Nour\Desktop\Programming pictures\grass.png')
    platform_image = pygame.transform.scale(platform_image, (platform_width, platform_height))
except pygame.error:
    print("Error loading platform image")

# Load jump sound
try:
    jump_sound = pygame.mixer.Sound(r'C:\Users\Nour\Downloads\8-bit-jump-001-171817.mp3')
except pygame.error:
    print("Error loading jump sound")

# Set initial player position above the first platform
player_x = platforms[0].x + (platform_width - player_size) // 2
player_y = platforms[0].y - player_size

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Infinite Platform Game")

# Scoring
score = 0
font = pygame.font.SysFont(None, 36)
touched_platforms = set()

# Function to create a new platform at a given height
def create_platform(previous_platform_y):
    # Create new platform at a higher height than the last one
    x = random.randint(0, SCREEN_WIDTH - platform_width)
    y = previous_platform_y - random.randint(100, 200)  # Ensuring platforms are spaced correctly
    return pygame.Rect(x, y, platform_width, platform_height)

# Set initial frame rate
fps = 30

# Main game loop
running = True
clock = pygame.time.Clock()

# Direction flag to track movement
moving_left = False

# Initialize the first platform
previous_platform_y = SCREEN_HEIGHT - 50

while running:
    # Increase FPS based on score
    fps = 30 + score  # Increase FPS by 1 for every platform reached (score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            jump_cooldown = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_x - player_speed > 0:
        player_x -= player_speed
        moving_left = True
    if keys[pygame.K_d] and player_x + player_speed < SCREEN_WIDTH - player_size:
        player_x += player_speed
        moving_left = False
    if keys[pygame.K_SPACE] and not is_jumping and not jump_cooldown:
        is_jumping = True
        player_velocity_y = -jump_power
        jump_cooldown = True
        if jump_sound:
            jump_sound.play()

    if is_jumping:
        player_y += player_velocity_y
        player_velocity_y += gravity

    on_platform = False
    for platform in platforms:
        if (
            player_y + player_size >= platform.top
            and player_y + player_size <= platform.bottom
            and player_x + player_size > platform.left
            and player_x < platform.right
            and player_velocity_y >= 0  # Only land if moving downward (falling)
        ):
            platform_coords = (platform.x, platform.y)
            if platform_coords not in touched_platforms:
                touched_platforms.add(platform_coords)
                score += 1
            player_y = platform.top - player_size
            player_velocity_y = 0
            is_jumping = False
            on_platform = True
            break

    if not on_platform and not is_jumping:
        is_jumping = True
        player_velocity_y = gravity

    # Scroll the screen up when the player reaches a certain height
    if player_y < SCREEN_HEIGHT // 2:
        scroll_y = SCREEN_HEIGHT // 2 - player_y
        player_y = SCREEN_HEIGHT // 2
        for platform in platforms:
            platform.y += scroll_y

        # Create a new platform at a higher point
        new_platform = create_platform(previous_platform_y)
        platforms.append(new_platform)
        previous_platform_y = new_platform.top

    # Remove platforms that are off the screen
    platforms = [platform for platform in platforms if platform.top < SCREEN_HEIGHT]

    # Check if the player falls off the screen
    if player_y >= SCREEN_HEIGHT:
        print("You Lost")
        screen.fill(YELLOW)
        game_over_text = font.render("Game Over! Press R to Quit", True, (0, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    pygame.quit()  # Close the game
                    sys.exit()  # Exit the program

    # Fill the screen with the background image
    screen.blit(background_image, (0, 0))

    # Flip the player image based on direction
    flipped_image = pygame.transform.flip(player_image, moving_left, False)
    screen.blit(flipped_image, (player_x, player_y))

    # Draw the platform images
    for platform in platforms:
        screen.blit(platform_image, (platform.x, platform.y))

    # Draw the score on the left side of the screen
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Frame rate control
    clock.tick(fps)

pygame.quit()
sys.exit()
