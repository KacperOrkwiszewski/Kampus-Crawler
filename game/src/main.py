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
player = Player('idle_down.gif', pygame.Vector2(120, 120))

pressed_keys = set()
key_order = []

# Keys -> vector map
DIRECTION_KEYS = {
    pygame.K_UP: (pygame.Vector2(0, 1), "up"),
    pygame.K_DOWN: (pygame.Vector2(0, -1), "down"),
    pygame.K_LEFT: (pygame.Vector2(1, 0), "left"),
    pygame.K_RIGHT: (pygame.Vector2(-1, 0), "right")
}

def get_current_direction_by_key():
    for key in reversed(key_order):
        if key in pressed_keys:
            return DIRECTION_KEYS[key]
    return None

def are_opposite_keys():
    return (
        (pygame.K_UP in pressed_keys and pygame.K_DOWN in pressed_keys) or
        (pygame.K_LEFT in pressed_keys and pygame.K_RIGHT in pressed_keys)
    )

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in DIRECTION_KEYS:
                if event.key not in pressed_keys:
                    key_order.append(event.key)
                pressed_keys.add(event.key)

                vec, direction = DIRECTION_KEYS[event.key]

                if not player.is_moving:
                    if player.last_direction == direction:
                      player.move_to_offset(vec.x, vec.y, Constants.TILE_HEIGHT * Constants.MAP_SCALE, Constants.TILE_WIDTH * Constants.MAP_SCALE)
                    else:
                        player.last_direction = direction
                        player.set_animation(f"{direction}.gif")

        if event.type == pygame.KEYUP:
            if event.key in pressed_keys:
                pressed_keys.remove(event.key)
            if event.key in key_order:
                key_order.remove(event.key)

    if not player.is_moving and pressed_keys:
        if not are_opposite_keys():
            current = get_current_direction_by_key()
            if current:
                vec, direction = current
                player.last_direction = direction
                player.move_to_offset(vec.x, vec.y, Constants.TILE_HEIGHT * Constants.MAP_SCALE, Constants.TILE_WIDTH * Constants.MAP_SCALE)

    player.update_position(dt)

    if not player.is_moving:
        player.set_animation(f"idle_{player.last_direction}.gif")

    map.draw(screen, Constants.MAP_SCALE, player.pos.x, player.pos.y)
    player.draw(screen, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, dt)

    pygame.display.flip()
    pygame.display.update()
