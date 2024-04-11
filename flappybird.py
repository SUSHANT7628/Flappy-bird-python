import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0,0,255)

# Bird properties
bird_width = 40
bird_height = 30
bird_x = 100
bird_y = SCREEN_HEIGHT // 2
bird_drop_speed = 7
gravity = 0.4
jump_strength = -7

# Pipe properties
pipe_width = 50
pipe_gap = 140
pipe_speed = 3
pipes = []

# Score
score = 0
font = pygame.font.SysFont(None, 36)



# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

def draw_bird(x, y):
    pygame.draw.rect(screen, BLACK, [x, y, bird_width, bird_height])

def draw_pipe(x, gap_start):
    top_pipe_height = gap_start
    bottom_pipe_height = SCREEN_HEIGHT - gap_start - pipe_gap
    pygame.draw.rect(screen, BLACK, [x, 0, pipe_width, top_pipe_height])
    pygame.draw.rect(screen, BLACK, [x, gap_start + pipe_gap, pipe_width, bottom_pipe_height])

def game_over():
    font = pygame.font.SysFont(None, 72)
    text = font.render("Game Over", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    quit()

def draw_start_screen():
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 72)
    text = font.render("Flappy Bird", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//4 - text.get_height()//2))
    button_text = font.render("Start", True, WHITE, BLUE)
    button_rect = button_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    pygame.draw.rect(screen, BLUE, button_rect)
    screen.blit(button_text, button_rect.topleft)


def main():
    global bird_y, bird_drop_speed, score

     # Start screen loop
    start_screen = True
    while start_screen:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                button_rect = pygame.Rect(SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 - 25, 100, 50)
                if button_rect.collidepoint(mouse_pos):
                    start_screen = False
        pygame.display.update() 

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_drop_speed = jump_strength
                

        # Bird movement
        bird_drop_speed += gravity
        bird_y += bird_drop_speed

        # Pipe movement and collision detection
        for pipe in pipes:
            pipe[0] -= pipe_speed
            if pipe[0] < -pipe_width:
                pipes.remove(pipe)
                score += 1
            if bird_x + bird_width > pipe[0] and bird_x < pipe[0] + pipe_width:
                if bird_y < pipe[1] or bird_y + bird_height > pipe[1] + pipe_gap:
                    game_over()
        
        # Generate new pipes
        if len(pipes) == 0 or pipes[-1][0] < SCREEN_WIDTH - 200:
            gap_start = random.randint(50, SCREEN_HEIGHT - pipe_gap - 50)
            pipes.append([SCREEN_WIDTH, gap_start])

        # Score display
        screen.fill(WHITE)
        for pipe in pipes:
            draw_pipe(pipe[0], pipe[1])
        draw_bird(bird_x, bird_y)
        score_text = font.render("Score: " + str(score), True, BLACK)
        screen.blit(score_text, (10, 10))
        pygame.display.update()

        # Collision detection with top and bottom of the screen
        if bird_y < 0 or bird_y + bird_height > SCREEN_HEIGHT:
            game_over()

        
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()
