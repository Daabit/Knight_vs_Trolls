import pygame
import random

pygame.init() # Inicialize the game
WINDOW_WIDTH = 800 # Constant width
WINDOW_HEIGHT = 500 # Constant heigth
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Create the display and its dimensions (x, y)
pygame.display.set_caption("Knight vs Trolls") # set_caption create the title of the window
clock = pygame.time.Clock() # All games need a running clock for all events that occur.
running = True # Variable that keep game running

# Create variables to keep track of score and lives
score = 0
lives = 5
speed = 5
play_sound = True

dt = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2 ) # Split by 2 means that player will appear in the middle of the width and height

# Define background music
pygame.mixer.music.load("D:\\Curso Python\\Pygame\\sounds\\bg.wav")

# Play background music
pygame.mixer.music.play(-1, 0.0) # -1 means on loop, 0.0 means start at the beginning of the sound

# Define sound effects
hit_sound = pygame.mixer.Sound("D:\\Curso Python\\Pygame\\sounds\\strike.wav")
miss_sound = pygame.mixer.Sound("D:\\Curso Python\\Pygame\\sounds\\miss.wav")
game_over_sound = pygame.mixer.Sound("D:\\Curso Python\\Pygame\\sounds\\game_over.wav")

# Background image
bg_image = pygame.image.load("D:\\Curso Python\\Pygame\\background_1.png").convert_alpha()

# Function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# Define fonts
title_font = pygame.font.SysFont("impact", 40)
score_font = pygame.font.SysFont("impact", 25)
lives_font = pygame.font.SysFont("impact", 25)
game_over_font = pygame.font.SysFont("impact", 75)
restart_game_font = pygame.font.SysFont("impact", 40)

# Render the text (as surface) Text, boolean for antialiasing, text color, background color
title_text = title_font.render("Fight!", True, "black", "white")
score_text = score_font.render(f"Score: {score}", True, "black", "white")
lives_text = lives_font.render(f"Lives: {lives}", True, "black", "white")
game_over_text = game_over_font.render("Game Over", True, "black", None)
restart_game_text = restart_game_font.render("Press [P] to play again...", True, "black", None)

# Get text rect
title_text_rect = title_text.get_rect()
score_text_rect = score_text.get_rect()
lives_text_rect = lives_text.get_rect()
game_over_text_rect = game_over_text.get_rect()
restart_game_text_rect = restart_game_text.get_rect()

# Position the text
title_text_rect.center = (WINDOW_WIDTH / 2, 30)
score_text_rect.topleft = (10, 5)
lives_text_rect.topleft = ((WINDOW_WIDTH - lives_text.get_width() - 10), 5)
game_over_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
restart_game_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 90)

# Load images
knight = pygame.image.load("D:\\Curso Python\\Pygame\\sprites\\knight.png").convert_alpha()
troll = pygame.image.load("D:\\Curso Python\\Pygame\\sprites\\troll.png").convert_alpha()

# Get rect surrounding the images
knight_rect = knight.get_rect()
troll_rect = troll.get_rect()

# Position the images
knight_rect.center = (80, WINDOW_HEIGHT/2)
troll_rect.x = WINDOW_WIDTH + 100 # The troll comes off the screen
troll_rect.y = random.randint(65, (WINDOW_HEIGHT - troll.get_height()))

while running:
    
    # Draw bg image
    draw_bg()
    
    # pygame.QUIT event (in capital case) means that the user clicked the X to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # Change the variable running to False
    
    # Pick the screen color
    #screen.fill("silver")
    
    # Blit text onto screen
    screen.blit(title_text, title_text_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(lives_text, lives_text_rect)
    
    # Check if lives ran out
    if lives == 0:
        # Game over text
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(restart_game_text, restart_game_text_rect)
        # Stop the troll from moving
        troll_rect.x = WINDOW_WIDTH + 100
        
        if play_sound:
            # Play sound
            game_over_sound.play()
            pygame.mixer.music.stop() # Stop the background music
            play_sound = False # Play only once game over sound
        
        #Check for [P] Play again
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            # Update start game variables
            score = 0
            lives = 5
            speed = 5
            play_sound = True #Reset the sound for the next game
            
            # Re-render the score and lives
            score_text = score_font.render(f"Score: {score}", True, "black", "white")
            lives_text = lives_font.render(f"Lives: {lives}", True, "black", "white")
            
            # Restart the backgound music
            pygame.mixer.music.play(-1, 0.0)

    # Blit images onto screen
    screen.blit(knight, knight_rect)
    screen.blit(troll, troll_rect)
    
    # Draw a line at top of the screen
    pygame.draw.line(screen, "black", (0, 60), (WINDOW_WIDTH, 60), 5)
    
    # Move images
    keys = pygame.key.get_pressed()
    
    # Move Knight
    if keys[pygame.K_UP] and knight_rect.y > 65:
        knight_rect.y -= 750 * dt
    if keys[pygame.K_DOWN] and knight_rect.y < WINDOW_HEIGHT - knight.get_height() - 5:
        knight_rect.y += 750 * dt
        
    # Move troll
    if troll_rect.x < 0:
        # The knight did not kill the troll
        # Play sound
        miss_sound.play()
        # The knight lose a life
        lives -= 1
        # Update lives on screen
        lives_text = lives_font.render(f"Lives: {lives}", True, "black", "white")
        troll_rect.x = WINDOW_WIDTH + 100 # The troll comes off the screen
        troll_rect.y = random.randint(65, (WINDOW_HEIGHT - troll.get_height())) #Generates another troll in random position
    else:
        # Move the troll to the left
        troll_rect.x -= speed
    
    # Collision detection
    if knight_rect.colliderect(troll_rect):
        #Play sound
        hit_sound.play()
        # Increase the score
        score += 1
        speed += 2
        # Update the score
        score_text = score_font.render(f"Score: {score}", True, "black", "white")
        troll_rect.x = WINDOW_WIDTH + 100 # The troll comes off the screen
        troll_rect.y = random.randint(65, (WINDOW_HEIGHT - troll.get_height())) #Generates another troll in random position
    
    # Flip the display to output our work to the screen
    #pygame.display.flip()
    
    # Update display
    pygame.display.update()
    
    dt = clock.tick(60) / 1000


pygame.quit() #Turn off the game, if the running while loop is working, this line will never be executed
