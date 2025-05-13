import pygame

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
    #move player
    playerY += playerY_change
    playerX += playerX_change
    #player draw function needs to be called after screen fill function as to not get obstructed
    player()
    pygame.display.update()