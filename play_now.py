import pygame
import random
import sys

# Simple playable fallback using colored rectangles (no external assets required)
# Constants
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
MAP_WIDTH = 16
MAP_HEIGHT = 12
TILE_SIZE = 32
TARGET_SCORE = 5  # reduced for a quick play

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Phypokezelda — Playable Fallback")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

# Colors
COLOR_GRASS = (80, 200, 120)
COLOR_PLAYER = (255, 140, 0)
COLOR_ENEMY = (200, 60, 60)
COLOR_BG = (40, 40, 40)
COLOR_TEXT = (255, 255, 255)

# Player state
player_rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
player_dir = "down"

# Game state
score = 0

# Simple lists to simulate evolutions and legendary items
Evolutions = {
    "Bulbasaur": "Ivysaur",
    "Charmander": "Charmeleon",
    "Squirtle": "Wartortle"
}
Legendary = {"Master Ball": "Mewtwo"}

# Generate a simple map (all grass) and place enemies randomly
map_tiles = [[" " for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

def generate_enemies(count=12):
    enemies = []
    positions = set()
    while len(enemies) < count:
        x = random.randint(0, MAP_WIDTH - 1)
        y = random.randint(0, MAP_HEIGHT - 1)
        if (x, y) in positions:
            continue
        positions.add((x, y))
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        enemies.append(rect)
    return enemies

enemies = generate_enemies(12)

# Place player at a free random tile
def place_player():
    while True:
        x = random.randint(0, MAP_WIDTH - 1)
        y = random.randint(0, MAP_HEIGHT - 1)
        if all(not (e.x == x * TILE_SIZE and e.y == y * TILE_SIZE) for e in enemies):
            player_rect.x = x * TILE_SIZE
            player_rect.y = y * TILE_SIZE
            break

place_player()


def draw():
    screen.fill(COLOR_BG)
    # draw tiles
    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, COLOR_GRASS, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # grid lines

    # draw enemies
    for e in enemies:
        pygame.draw.rect(screen, COLOR_ENEMY, e)

    # draw player
    pygame.draw.rect(screen, COLOR_PLAYER, player_rect)

    # draw score
    txt = font.render(f"Score: {score}/{TARGET_SCORE}", True, COLOR_TEXT)
    screen.blit(txt, (8, 8))

    pygame.display.flip()


def handle_collision():
    global score
    for e in enemies[:]:
        if player_rect.colliderect(e):
            enemies.remove(e)
            score += 1
            # Choose a random event from evolutions or legendary
            choices = list(Evolutions.keys()) + list(Legendary.keys())
            if not choices:
                print("No more events.")
            else:
                name = random.choice(choices)
                if name in Evolutions:
                    print(f"Your {name} evolves into {Evolutions[name]}!")
                    del Evolutions[name]
                else:
                    print(f"You found a {name}! You can now catch {Legendary[name]}.")
                    del Legendary[name]
            break


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                player_rect.x = max(0, player_rect.x - TILE_SIZE)
                player_dir = "left"
            elif event.key == pygame.K_RIGHT:
                player_rect.x = min((MAP_WIDTH - 1) * TILE_SIZE, player_rect.x + TILE_SIZE)
                player_dir = "right"
            elif event.key == pygame.K_UP:
                player_rect.y = max(0, player_rect.y - TILE_SIZE)
                player_dir = "up"
            elif event.key == pygame.K_DOWN:
                player_rect.y = min((MAP_HEIGHT - 1) * TILE_SIZE, player_rect.y + TILE_SIZE)
                player_dir = "down"

    handle_collision()

    if score >= TARGET_SCORE:
        print("You win! Final score:", score)
        running = False

    draw()
    clock.tick(30)

pygame.quit()
sys.exit()
