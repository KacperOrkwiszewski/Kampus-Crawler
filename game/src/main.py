import pygame
from constants import Constants
from map.game_map import GameMap
from player.player import Player

clock = pygame.time.Clock()
pygame.init()

screen = pygame.display.set_mode((Constants.WINDOW_HEIGHT, Constants.WINDOW_WIDTH))
pygame.display.set_caption("Kampus Crawler")
pygame.display.set_icon(pygame.image.load('logo_icon.png'))

map = GameMap("map_data/simple_map.tmx")
player = Player('idle_down.gif')

pressed_keys = set()
key_order = []

# Mapa klawiszy -> wektor
DIRECTION_KEYS = {
    pygame.K_UP: (0, 1, "up"),
    pygame.K_DOWN: (0, -1, "down"),
    pygame.K_LEFT: (1, 0, "left"),
    pygame.K_RIGHT: (-1, 0, "right")
}

def get_current_direction():
    # Priorytet: ostatnio naciśnięty
    for key in reversed(key_order):
        if key in pressed_keys:
            return DIRECTION_KEYS[key]
    return None

def are_opposite_keys():
    vert = any(k in pressed_keys for k in [pygame.K_UP, pygame.K_DOWN])
    hori = any(k in pressed_keys for k in [pygame.K_LEFT, pygame.K_RIGHT])
    return (
        (pygame.K_UP in pressed_keys and pygame.K_DOWN in pressed_keys) or
        (pygame.K_LEFT in pressed_keys and pygame.K_RIGHT in pressed_keys)
    )

running = True
while running:
    dt = clock.tick(60) / 1000

    # --- EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in DIRECTION_KEYS:
                if event.key not in pressed_keys:
                    key_order.append(event.key)
                pressed_keys.add(event.key)

                dx, dy, direction = DIRECTION_KEYS[event.key]

                if not player.is_moving:
                    if player.last_direction == direction:
                        player.move_to_offset(dx, dy)
                    else:
                        player.last_direction = direction
                        player.set_direction_animation()

        if event.type == pygame.KEYUP:
            if event.key in pressed_keys:
                pressed_keys.remove(event.key)
            if event.key in key_order:
                key_order.remove(event.key)

    # --- AUTO MOVEMENT ---
    if not player.is_moving and pressed_keys:
        if are_opposite_keys():
            pass  # Don't move
        else:
            current = get_current_direction()
            if current:
                dx, dy, direction = current
                player.last_direction = direction
                player.move_to_offset(dx, dy)

    # --- UPDATE & RENDER ---
    player.update_position(dt)

    if not player.is_moving:
        player.set_idle_animation()

    map.draw(screen, Constants.MAP_SCALE, player.pos_x, player.pos_y)
    player.draw(screen, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, dt)

    pygame.display.flip()
