import pygame

pygame.init()

screen_width = 800
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Lone Adventurer')


#load images
#background images
background_img = pygame.image.load('img/caverns/layers/background.png').convert_alpha()

#drawing background
def draw_bg():
    screen.blit(background_img,(0,0))

run = True
while run:
    draw_bg()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()