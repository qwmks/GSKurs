import pygame
import sys
from random import randint
from pygame.constants import KEYDOWN
import spritesheet
import os
from pygame.time import Clock
def drawGO(score):
    screen.fill((152,255,152))
    if score and score!=0:
        score_surface = small_font.render(f"Score: {score}",True,'Red')
        score_rect = score_surface.get_rect(midtop = (width/2,50))
        screen.blit(score_surface,score_rect)
    name_surface = font.render("Super runner",True,'Red')
    name_rect = name_surface.get_rect(midtop = (width/2,200))
    screen.blit(name_surface,name_rect)
    name_surface = small_font.render("Press any key to start",True,'Red')
    name_rect = name_surface.get_rect(midtop = (width/2,400))
    icon_rect = pc_icon.get_rect(midtop = (100,20))
    screen.blit(pc_icon,icon_rect)
    screen.blit(name_surface,name_rect)

def show_score(score):
    score_surface = font.render(f"Score: {score}",True,'Red')
    score_rect = score_surface.get_rect(topleft = (0,0))
    screen.blit(score_surface,score_rect)

def show_health(health):
    health_surface = font.render(f"Lives: {health}",True,'Red')
    health_rect = health_surface.get_rect(topright = (width,0))
    screen.blit(health_surface,health_rect)

def move_objects(hearts,rocks,coins,frame_counter):
    color = (255,0,0)
    speed = 6
    if hearts or rocks or coins:
        for coin in coins:
            coin.y+=speed
            screen.blit(coin_anim[frame_counter%8],coin)
            pygame.draw.rect(screen,color,coin,2)
        for rock in rocks:
            rock.y+=speed
            screen.blit(rock_anim[frame_counter%4],rock)
            pygame.draw.rect(screen,color,rock,2)
        for heart in hearts:
            heart.y+=speed
            screen.blit(heart_anim[frame_counter%6],heart)
            pygame.draw.rect(screen,color,heart,2)
        hearts = [heart for heart in hearts if heart.y<=height ]
        rocks = [rock for rock in rocks if rock.y<=height ]
        coins = [coin for coin in coins if coin.y<=height]
        return hearts,rocks,coins
    else:
         return [],[],[]

def collide_hearts(hearts,player,health,score):
    max_health=3
    heart_sound = pygame.mixer.Sound(os.path.join(app_path,'heart.wav'))
    heart_sound.set_volume(3)
    if hearts:
        for heart in hearts:
            if player.colliderect(heart):
                heart_sound.play()
                if health==max_health:
                    score+=50
                else:
                    health+=1
                heart.x = width+1                
        hearts = [heart for heart in hearts if heart.x!=width+1]
    return health,hearts,score

def collide_rocks(rocks,player,health):
    crush_sound = pygame.mixer.Sound(os.path.join(app_path,'rockhit.wav'))
    crush_sound.set_volume(0.5)
    if rocks:
        for rock in rocks:
            if player.colliderect(rock):
                crush_sound.play()
                health-=1
                rock.x =width+1
                if health<0:
                    rocks = [rock for rock in rocks if rock.x!=width+1]
                    return -1,rocks
        rocks = [rock for rock in rocks if rock.x!=width+1]        
    return health,rocks

def collide_coins(coins,player,score):
    coin_sound = pygame.mixer.Sound(os.path.join(app_path,'coin.wav'))
    coin_sound.set_volume(0.5)
    if coins:
        for coin in coins:
            if player.colliderect(coin):
                coin_sound.play()
                score+=100
                coin.x = width+1
        coins = [coin for coin in coins if coin.x!=width+1]
    return score,coins

def start_game(start_health,start_score):
    health =start_health
    score = start_score
    hearts =[]
    coins = []
    rocks = []
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.5)
    return health,score,hearts,coins,rocks
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    app_path = sys._MEIPASS
else:
    app_path = os.path.dirname(os.path.abspath(__file__))
width = 900
height = 600
start_health =0
start_score =0
tickrate = 30
pygame.init()
 
pygame.mixer.music.load(os.path.join(app_path,'bg_dream.mp3'))

pygame.display.set_caption("Super Runner")
screen = pygame.display.set_mode((width,height))
font = pygame.font.Font(os.path.join(app_path,'pacifico.ttf'),50)
small_font = pygame.font.Font(None,30)
base_background = pygame.image.load(os.path.join(app_path,'grass.jpg')).convert_alpha()
base_background = pygame.transform.scale(base_background,(width,height))
base_background_rect = base_background.get_rect(topleft = (0,0))
health = start_health
score = start_score
curr_time = 0
start_time = 0
timer = pygame.time.Clock()

pause_surface = font.render("The game is paused",True,'Blue')
pause_rect = pause_surface.get_rect(center=(width/2,height/2 ))

# objects 
pc_surface = pygame.image.load(os.path.join(app_path,'running.png')).convert_alpha()
pc_sprite_sheet = spritesheet.SpriteSheet(pc_surface)
pc_anim = []
for i in range(9):
    pc_anim.append(pc_sprite_sheet.get_player(i, 36, 50, 3, (0, 0, 0))) 
pc_rect = pc_anim[0].get_rect(midbottom =(width/2,height))
pc_x_mov = 0
pc_icon = pc_sprite_sheet.get_icon(64,64,4,(0,0,0))

rock_image = pygame.image.load(os.path.join(app_path,'rock.png')).convert_alpha()
rock_sprite_sheet = spritesheet.SpriteSheet(rock_image)
rock_anim = []
for i in range(4):
    rock_anim.append(rock_sprite_sheet.get_image(i, 32, 32, 3, (0, 0, 0))) 
rocks = []

coin_image = pygame.image.load(os.path.join(app_path,'coins.png')).convert_alpha()
coin_sprite_sheet = spritesheet.SpriteSheet(coin_image)
coin_anim = []
for i in range(8):
    coin_anim.append(coin_sprite_sheet.get_image(i, 16, 16, 3, (0, 0, 0))) 
coins = []

heart_image = pygame.image.load(os.path.join(app_path,'heart.png')).convert_alpha()
heart_sprite_sheet = spritesheet.SpriteSheet(heart_image)
heart_anim = []
for i in range(6):
    heart_anim.append(heart_sprite_sheet.get_image(i, 64, 64, 1, (0, 0, 0))) 
hearts = []

showGO= 1
isActive =0
frame_counter = 0
rng_handle = 0
spawn_timer = pygame.USEREVENT+1
pygame.time.set_timer(spawn_timer,1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if showGO:
            if event.type == pygame.KEYDOWN:
                health,score,hearts,coins,rocks = start_game(start_health,start_score)
                pc_rect.x = width/2-pc_rect.w/2
                pc_x_mov=0
                showGO=0
                isActive=1
                
        else:
            if isActive:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                        pc_x_mov/=5
                    if event.key ==pygame.K_SPACE:
                        isActive=0                
                    if event.key ==pygame.K_RIGHT or event.key ==pygame.K_d:
                        pc_x_mov = 20
                        if event.mod & pygame.KMOD_SHIFT:
                            pc_x_mov = 4
                    if event.key ==pygame.K_LEFT or event.key ==pygame.K_a:
                        pc_x_mov = -20
                        if event.mod & pygame.KMOD_SHIFT:
                            pc_x_mov = -4
                if event.type==pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT:
                        pc_x_mov*=5
                    if event.key ==pygame.K_RIGHT or event.key ==pygame.K_LEFT or event.key ==pygame.K_a  or event.key ==pygame.K_d:
                        pc_x_mov = 0
                if event.type == spawn_timer:
                    if rng_handle<2:
                        match randint(0,7):
                            case 0:
                                hearts.append(heart_anim[0].get_rect(bottomleft=(randint(0,width-heart_anim[0].get_width()),0)))
                                rng_handle+=1
                            case 1:
                                coins.append(coin_anim[0].get_rect(bottomleft=(randint(0,width-coin_anim[0].get_width()),0)))
                                rng_handle+=1
                            case 2:
                                coins.append(coin_anim[0].get_rect(bottomleft=(randint(0,width-coin_anim[0].get_width()),0)))
                                rng_handle+=1
                            case _:
                                rocks.append(rock_anim[0].get_rect(bottomleft=(randint(0,width-rock_anim[0].get_width()),0)))
                    else:
                        rocks.append(rock_anim[0].get_rect(bottomleft=(randint(0,width-rock_anim[0].get_width()),0)))
                        rng_handle=0
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key ==pygame.K_SPACE:
                        isActive=1
                        pygame.mixer.music.unpause()
    if showGO:
        drawGO(score)        
    else:
        if isActive:
            screen.blit(base_background,(0,0))
            pc_rect.x+=pc_x_mov
            if pc_rect.x<0:
                pc_rect.x=0
            if pc_rect.x>width-pc_rect.w:
                pc_rect.x  = width-pc_rect.w
            screen.blit(pc_anim[frame_counter%9],pc_rect)
            pygame.draw.rect(screen,(255,0,0),pc_rect,2)
            hearts,rocks,coins = move_objects(hearts,rocks,coins,frame_counter)
            health,hearts,score = collide_hearts(hearts,pc_rect,health,score)
            health, rocks = collide_rocks(rocks,pc_rect,health)
            score,coins = collide_coins(coins,pc_rect,score)
            if health == -1:
                    showGO =1
                    pygame.mixer.music.stop()
            frame_counter+=1
            if frame_counter>72:
                frame_counter= 0
            show_score(score)
            show_health(health)
        else:
            pygame.mixer.music.pause()
            screen.blit(pause_surface,pause_rect)
    pygame.display.update()
    timer.tick(tickrate)
