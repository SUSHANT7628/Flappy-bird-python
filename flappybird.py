import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Bird properties
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
BIRD_X = 50
BIRD_Y = SCREEN_HEIGHT // 2
BIRD_DROP_SPEED = 0
JUMP_STRENGTH = -8

# Pipe properties
PIPE_WIDTH = 70
PIPE_GAP = 200
PIPE_SPEED = 3
pipes = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

def draw_bird(x, y):
    pygame.draw.rect(screen, BLACK, [x, y, BIRD_WIDTH, BIRD_HEIGHT])

def draw_pipe(x, gap_start):
    top_pipe_height = gap_start
    bottom_pipe_height = SCREEN_HEIGHT - gap_start - PIPE_GAP
    pygame.draw.rect(screen, GREEN, [x, 0, PIPE_WIDTH, top_pipe_height])
    pygame.draw.rect(screen, GREEN, [x, gap_start + PIPE_GAP, PIPE_WIDTH, bottom_pipe_height])

def game_over():
    global score
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
    
    # Restart button
    pygame.draw.rect(screen, WHITE, (150, 400, 100, 50))
    restart_text = font.render("Restart", True, BLACK)
    screen.blit(restart_text, (120, 415))
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 150 <= mouse_pos[0] <= 250 and 400 <= mouse_pos[1] <= 450:
                    return True

def main():
    global BIRD_Y, BIRD_DROP_SPEED, score

    while True:
        # Reset game variables
        BIRD_Y = SCREEN_HEIGHT // 2
        BIRD_DROP_SPEED = 0
        pipes.clear()
        score = 0

        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        BIRD_DROP_SPEED = JUMP_STRENGTH

            # Bird movement
            BIRD_DROP_SPEED += 0.5
            BIRD_Y += BIRD_DROP_SPEED

            # Pipe movement and collision detection
            for pipe in pipes:
                pipe[0] -= PIPE_SPEED
                if pipe[0] < -PIPE_WIDTH:
                    pipes.remove(pipe)
                    score += 1
                if BIRD_X + BIRD_WIDTH > pipe[0] and BIRD_X < pipe[0] + PIPE_WIDTH:
                    if BIRD_Y < pipe[1] or BIRD_Y + BIRD_HEIGHT > pipe[1] + PIPE_GAP:
                        running = False

            # Generate new pipes
            if len(pipes) == 0 or pipes[-1][0] < SCREEN_WIDTH - 200:
                gap_start = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
                pipes.append([SCREEN_WIDTH, gap_start])

            # Score display
            screen.fill(WHITE)
            for pipe in pipes:
                draw_pipe(pipe[0], pipe[1])
            draw_bird(BIRD_X, BIRD_Y)
            score_text = font.render("Score: " + str(score), True, BLACK)
            screen.blit(score_text, (10, 10))
            pygame.display.flip()

            # Collision detection with top and bottom of the screen
            if BIRD_Y < 0 or BIRD_Y + BIRD_HEIGHT > SCREEN_HEIGHT:
                running = False

            pygame.time.Clock().tick(60)

        # When the game is over, display the game over screen
        if game_over():
            continue
        else:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
