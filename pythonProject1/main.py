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

#set player position
playerX = 400
playerY = 400

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

    #change screen color (RGB format) // to see changes use update method
    screen.fill((200,0,24))
    #player needs to be undernearth screen fill function as to not get obstructed
    player()
    pygame.display.update()