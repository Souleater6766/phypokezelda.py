import pygame
import random
import sys

# Define constants
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
MAP_WIDTH = 16
MAP_HEIGHT = 12
TILE_SIZE = 32
TARGET_SCORE = 50

# Initialize Pygame
pygame.init()

# Load images
grass_image = pygame.image.load("grass.png")
player_images = {
    "up": pygame.image.load("charmander_up.png"),
    "down": pygame.image.load("charmander_down.png"),
    "left": pygame.image.load("charmander_left.png"),
    "right": pygame.image.load("charmander_right.png")
}
enemy_images = [
    pygame.image.load("caterpie.png"),
    pygame.image.load("pidgey.png"),
    pygame.image.load("ratatta.png"),
    pygame.image.load("zubat.png")
]

# Define game state variables
player_direction = "down"
player_rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
enemies = []
enemy_rects = []
score = 0
evolutions = {
    "Bulbasaur": "Ivysaur",
    "Ivysaur": "Venusaur",
    "Charmander": "Charmeleon",
    "Charmeleon": "Charizard",
    "Squirtle": "Wartortle",
    "Wartortle": "Blastoise"
}
legendary_items = {
    "Master Ball": "Mewtwo"
}

# Load a game map from a file
def load_map(filename):
    with open(filename) as f:
        return [line.strip() for line in f]

# Load a single image and scale it to the tile size
def load_image(filename):
    image = pygame.image.load(filename)
    return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

# Draw the game map and enemies to the screen
def draw_map(map_data, surface):
    global grass_image, enemy_images, enemies, enemy_rects

    for row, tiles in enumerate(map_data):
        for col, tile in enumerate(tiles):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            surface.blit(grass_image, (x, y))
            if tile == "E":
                enemy_image = random.choice(enemy_images)
                enemy_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                enemies.append(enemy_image)
                enemy_rects.append(enemy_rect)

# Draw the player to the screen
def draw_player(surface):
    global player_images, player_direction, player_rect

    surface.blit(player_images[player_direction], player_rect)

# Move the player and update the player direction
def move_player(dx, dy):
    global player_direction, player_rect

    # Update player direction
    if dx > 0:
        player_direction = "right"
    elif dx < 0:
        player_direction = "left"
    elif dy > 0:
        player_direction = "down"
    elif dy < 0:
        player_direction = "up"

    # Move player
    new_x = player_rect.x + dx
    new_y = player_rect.y + dy
    if new_x < 0 or new_x >= MAP_WIDTH * TILE_SIZE:
        return
    if new_y < 0 or new_y >= MAP_HEIGHT * TILE_SIZE:
        return
    player_rect.x = new_x
    player_rect.y = new_y

# Check for collisions between the player and enemies
def check_collisions():
    global score, evolutions, legendary_items, player_rect, enemies, enemy_rects

    # iterate over a copy so removing items inside the loop is safe
    for enemy_rect in enemy_rects[:]:
        if player_rect.colliderect(enemy_rect):
            # Remove the enemy from the list of enemies
            index = enemy_rects.index(enemy_rect)
            enemies.pop(index)
            enemy_rects.pop(index)

            # Update the score and check for evolutions and legendary items
            score += 1
            if score >= TARGET_SCORE:
                print("You win!")
                pygame.quit()
                sys.exit()

            # pick from both evolutions and legendary items
            choices = list(evolutions.keys()) + list(legendary_items.keys())
            if not choices:
                print("No more events.")
                return

            pokemon_name = random.choice(choices)
            if pokemon_name in evolutions:
                print("Your", pokemon_name, "evolves into", evolutions[pokemon_name])
                del evolutions[pokemon_name]
            else:
                # pokemon_name must be a legendary item name
                print("You found a", pokemon_name, "! You can now catch", legendary_items[pokemon_name])
                del legendary_items[pokemon_name]

            # stop after handling one collision this frame
            break
