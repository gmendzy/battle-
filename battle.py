import pygame
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Lone Adventurer')


#game variables
current_fighter = 1
total_fighters = 2
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
clicked = False
game_over = 0 



#font
font = pygame.font.Font('C:\projects\Python\AncientModernTales.ttf.ttf', 26)

#define colors
red = (255, 0, 0)
green = (0, 255, 0)

#load images
#background images
background_img1 = pygame.image.load('battle/img/caverns/layers/background.png').convert_alpha()
background_img2 = pygame.image.load('battle/img/caverns/layers/back-walls.png').convert_alpha()
background_img3 = pygame.image.load('battle/img/caverns/layers/tiles.png').convert_alpha()

#panel image
panel_img = pygame.image.load('battle/img/icons/panel.png').convert_alpha()

#cursor image
cursor_img = pygame.image.load('battle/img/icons/cursor.png').convert_alpha()

#drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#drawing background
def draw_bg():
    screen.blit(background_img1,(0,0))
    screen.blit(background_img2,(0,0))
    screen.blit(background_img3,(0,0))
#draws UI action panel
def draw_panel():
    #draw panel 
    screen.blit(panel_img,(0,screen_height - bottom_panel))
    #show knight stats
    draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
    #show name and health
    draw_text(f'{bandit1.name} HP: {bandit1.hp}', font, red, 550, screen_height - bottom_panel + 10)







#player class
class Player():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list =  []
        self.frame_index = 0
        self.action = 0  #0: idle, 1:attack, 2: dead
        self.update_time = pygame.time.get_ticks()
        #load idle images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'battle/img/{self.name}/idle/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 1.6, img.get_height() *1.6))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'battle/img/{self.name}/Attack/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 1.6, img.get_height() *1.6))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index] 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self):
        animation_cooldown = 100
        #handle animation
        #update animation
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out, then reset back to first frame
        if self.frame_index >= len(self.animation_list[self.action]):
            self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()



    def attack(self, target):
        #deal damage
        damage = self.strength
        target.hp -= damage
        #check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
        #set variables to attack animation
        self.action = 1
        self.fram_index = 0
        self.update_time = pygame.time.get_ticks()




    def draw(self):
        screen.blit(self.image, self.rect)



class Healthbar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        #update with new health
        self.hp = hp
        #calculate health
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))
        




knight = Player(225, 175, 'knight', 50, 10, 3)
bandit1 = Player(500, 170, 'Bandit', 30, 6, 1)

bandit_list = []
bandit_list.append(bandit1)

knight_health_bar = Healthbar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_health_bar = Healthbar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)


run = True
while run:

    clock.tick(fps)

    #draws background
    draw_bg()

    #draw_panel
    draw_panel()
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)

    #draw Player
    knight.update()
    knight.draw()
    for bandit in bandit_list:
        bandit.update()
        bandit.draw()
    #control player input
    #reset action variables
    attack = False
    potion = False
    target = None
    #makes sure mouse is visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            
            pygame.mouse.set_visible(False)
            #show sword in place of mouse cursor
            screen.blit(cursor_img, pos)
            if clicked == True:
                attack = True
                target = bandit_list[count]



    #player action
    if knight.alive == True:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                #look for player action
                #attack
                if attack == True and target != None: 
                    knight.attack(target)
                    current_fighter += 1
                    action_cooldown = 0

    #enemy action
    for count, bandit in enumerate(bandit_list):
        if current_fighter == 2 + count:
            if bandit.alive == True:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:

                    bandit.attack(knight)
                    current_fighter += 1
                    action_cooldown = 0
            else:
                current_fighter += 1

        #if all fighters had a turn then reset
        if current_fighter > total_fighters:
            current_fighter = 1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False
    pygame.display.update()

pygame.quit()