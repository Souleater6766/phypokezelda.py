# Load the game map
map_data = load_map("map.txt")

# Set up the Pygame display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pokémon/Zelda-style game with evolutions and legendary items")

# Draw the game map and enemies to the screen
draw_map(map_data, screen)

# Randomly position the player on the map
while True:
    player_rect.x = random.randint(0, MAP_WIDTH - 1) * TILE_SIZE
    player_rect.y = random.randint(0, MAP_HEIGHT - 1) * TILE_SIZE
    if map_data[player_rect.y // TILE_SIZE][player_rect.x // TILE_SIZE] == " ":
        break

# Start the Pygame main loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                return
            elif event.key == pygame.K_LEFT:
                move_player(-TILE_SIZE, 0)
            elif event.key == pygame.K_RIGHT:
                move_player(TILE_SIZE, 0)
            elif event.key == pygame.K_UP:
                move_player(0, -TILE_SIZE)
            elif event.key == pygame.K_DOWN:
                move_player(0, TILE_SIZE)

    # Check for collisions between the player and enemies
    check_collisions()

    # Draw everything to the screen
    draw_map(map_data, screen)
    draw_player(screen)
    pygame.display.update()
