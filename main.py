import pygame
import sys
from random import randint
from pygame.constants import KEYDOWN
import spritesheet

from pygame.time import Clock
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
    speed = 5
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
    heart_sound = pygame.mixer.Sound('heart.wav')
    heart_sound.set_volume(3)
    if hearts:
        for heart in hearts:
            if player.colliderect(heart):
                heart_sound.play()
                if health==5:
                    score+=50
                else:
                    health+=1
                heart.x = width+1                
        hearts = [heart for heart in hearts if heart.x!=width+1]
    return health,hearts,score

def collide_rocks(rocks,player,health):
    crush_sound = pygame.mixer.Sound('rockhit.wav')
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
    coin_sound = pygame.mixer.Sound('coin.wav')
    coin_sound.set_volume(0.7)
    if coins:
        for coin in coins:
            if player.colliderect(coin):
                coin_sound.play()
                score+=100
                coin.x = width+1
        coins = [coin for coin in coins if coin.x!=width+1]
    return score,coins

width = 900
height = 600
pygame.init()
 
pygame.mixer.music.load('bg_dream.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.5)
pygame.display.set_caption("Super Runner")
screen = pygame.display.set_mode((width,height))
font = pygame.font.Font(None,50)
base_background = pygame.image.load('grass.jpg').convert_alpha()
base_background = pygame.transform.scale(base_background,(width,height))
health = 3
score = 0

timer = pygame.time.Clock()

pause_surface = font.render("The game is paused",True,'Blue')
pause_rect = pause_surface.get_rect(center=(width/2,height/2 ))

# objects 
pc_surface = pygame.image.load('running.png').convert_alpha()
pc_sprite_sheet = spritesheet.SpriteSheet(pc_surface)
pc_anim = []
for i in range(9):
    pc_anim.append(pc_sprite_sheet.get_player(i, 36, 50, 3, (0, 0, 0))) 
pc_rect = pc_anim[0].get_rect(bottomleft = (400,height))
pc_x_mov = 0

rock_image = pygame.image.load('rock.png').convert_alpha()
rock_sprite_sheet = spritesheet.SpriteSheet(rock_image)
rock_anim = []
for i in range(4):
    rock_anim.append(rock_sprite_sheet.get_image(i, 32, 32, 3, (0, 0, 0))) 
rocks = []

coin_image = pygame.image.load('coins.png').convert_alpha()
coin_sprite_sheet = spritesheet.SpriteSheet(coin_image)
coin_anim = []
for i in range(8):
    coin_anim.append(coin_sprite_sheet.get_image(i, 16, 16, 3, (0, 0, 0))) 
coins = []

heart_image = pygame.image.load('heart.png').convert_alpha()
heart_sprite_sheet = spritesheet.SpriteSheet(heart_image)
heart_anim = []
for i in range(6):
    heart_anim.append(heart_sprite_sheet.get_image(i, 64, 64, 1, (0, 0, 0))) 
# heart_rect = heart_anim[0].get_rect(midbottom =(heart_x,heart_y))
hearts = []

showGO= 1
isActive =1
frame_counter = 0
rng_handle = 0
spawn_timer = pygame.USEREVENT+1
pygame.time.set_timer(spawn_timer,1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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
                    match randint(0,5):
                        case 0:
                            hearts.append(heart_anim[0].get_rect(bottomleft=(randint(0,width-heart_anim[0].get_width()),0)))
                            rng_handle+=1
                        case 1:
                            rocks.append(rock_anim[0].get_rect(bottomleft=(randint(0,width-rock_anim[0].get_width()),0)))
                        case 2:
                            rocks.append(rock_anim[0].get_rect(bottomleft=(randint(0,width-rock_anim[0].get_width()),0)))
                        case 3:
                            coins.append(coin_anim[0].get_rect(bottomleft=(randint(0,width-coin_anim[0].get_width()),0)))
                            rng_handle+=1
                        case 4:
                            rocks.append(rock_anim[0].get_rect(bottomleft=(randint(0,width-rock_anim[0].get_width()),0)))
                        case 5:
                            rocks.append(rock_anim[0].get_rect(bottomleft=(randint(0,width-rock_anim[0].get_width()),0)))
                else:
                    rocks.append(rock_anim[0].get_rect(bottomleft=(randint(0,width-rock_anim[0].get_width()),0)))
                    rng_handle=0
        else:
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_SPACE:
                    isActive=1
                    pygame.mixer.music.unpause()
    
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
                pygame.quit()
                sys.exit()
        frame_counter+=1
        if frame_counter>72:
            frame_counter= 0
        show_score(score)
        show_health(health)
    else:
        pygame.mixer.music.pause()
        screen.blit(pause_surface,pause_rect)
    pygame.display.update()
    timer.tick(30)
