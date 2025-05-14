import pygame
import pytmx

#must initialyse pygame in order for program to work
pygame.init()

screen = pygame.display.set_mode((800, 800))

#title and icon
pygame.display.set_caption("Kampus Crawler")
icon = pygame.image.load('logo_icon.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('idle.gif')
#scale player image
playerImg = pygame.transform.scale(playerImg, (80, 80))
PLAYER_SIZE_X = 80
PLAYER_SIZE_Y = 80
PLAYER_MOVEMENT_SPEED = 0.05

#set player position
playerX = 400
playerY = 400
#for movement
playerX_change = 0
playerY_change = 0

def player():
    #draw player sprite
    screen.blit(playerImg,(playerX - PLAYER_SIZE_X/2, playerY - PLAYER_SIZE_Y/2))


#map
#load map from tmx file (made and editable in Tiled)
tmx_data = pytmx.load_pygame("tiled/mapa.tmx")

#drawing map using pytmx library ---not my code
SCALE = 5  # przykładowo: 2x większe kafelki
MAP_OFFSET_X = -1000
MAP_OFFSET_Y = -1000

def draw_map():
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    # Skaluj kafelek
                    scaled_tile = pygame.transform.scale(tile, (
                        tmx_data.tilewidth * SCALE,
                        tmx_data.tileheight * SCALE
                    ))
                    screen.blit(scaled_tile, (
                        x * tmx_data.tilewidth * SCALE + MAP_OFFSET_X,
                        y * tmx_data.tileheight * SCALE + MAP_OFFSET_Y
                    ))

#game loop
running = True
while running:
    for event in pygame.event.get():
        #event handler (the top right X button is pressed)
        if event.type == pygame.QUIT:
            running = False
        #keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                playerY_change = PLAYER_MOVEMENT_SPEED
            if event.key == pygame.K_UP:
                playerY_change = -PLAYER_MOVEMENT_SPEED
            if event.key == pygame.K_LEFT:
                playerX_change = -PLAYER_MOVEMENT_SPEED
            if event.key == pygame.K_RIGHT:
                playerX_change = PLAYER_MOVEMENT_SPEED
        #stop moving if key is no longer pressed
        if event.type == pygame.KEYUP:
            playerX_change = 0
            playerY_change = 0

    #change screen color (RGB format) // to see changes use update method
    screen.fill((200,0,24))
    #draw map
    draw_map()
    #move player
    playerY += playerY_change
    playerX += playerX_change
    #player draw function needs to be called after screen fill function as to not get obstructed
    player()
    pygame.display.update()