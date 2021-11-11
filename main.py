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

def move_objects(hearts,rocks,frame_counter):
    color = (255,0,0)
    if hearts or rocks:
        for rock in rocks:
            rock.y+=4
            screen.blit(rock_anim[frame_counter%4],rock)
            pygame.draw.rect(screen,color,rock,2)
        for heart in hearts:
            heart.y+=4
            screen.blit(heart_anim[frame_counter%6],heart)
            pygame.draw.rect(screen,color,heart,2)
        hearts = [heart for heart in hearts if heart.y<=600 ]
        rocks = [rock for rock in rocks if rock.y<=600 ]
        return hearts,rocks
    else:
         return [],[]

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
                heart.x = 901                
        hearts = [heart for heart in hearts if heart.x!=901]
    return health,hearts,score
def collide_rocks(rocks,player,health):
    crush_sound = pygame.mixer.Sound('rockhit.wav')
    crush_sound.set_volume(0.5)
    if rocks:
        for rock in rocks:
            if player.colliderect(rock):
                crush_sound.play()
                health-=1
                rock.x =901
                if health<0:
                    rocks = [rock for rock in rocks if rock.x!=901]
                    return -1,rocks
    return health,rocks
# width = 852
# height = 480
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
    # pc_anim.append(pc_sprite_sheet.get_image(i, 64, 64, 3, (0, 0, 0))) 
    pc_anim.append(pc_sprite_sheet.get_player(i, 36, 50, 3, (0, 0, 0))) 
pc_rect = pc_anim[0].get_rect(bottomleft = (400,height))
pc_x_mov = 0

rock_image = pygame.image.load('rock.png').convert_alpha()
rock_sprite_sheet = spritesheet.SpriteSheet(rock_image)
rock_anim = []
for i in range(4):
    rock_anim.append(rock_sprite_sheet.get_image(i, 32, 32, 3, (0, 0, 0))) 
rocks = []

heart_image = pygame.image.load('heart.png').convert_alpha()
heart_sprite_sheet = spritesheet.SpriteSheet(heart_image)

heart_anim = []
for i in range(6):
    heart_anim.append(heart_sprite_sheet.get_image(i, 64, 64, 1, (0, 0, 0))) 
# heart_rect = heart_anim[0].get_rect(midbottom =(heart_x,heart_y))
hearts = []


isActive =1
frame_counter = 0

spawn_timer = pygame.USEREVENT+1
pygame.time.set_timer(spawn_timer,1800)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if isActive:
            if event.type == pygame.KEYDOWN:
                
                if event.key ==pygame.K_SPACE:
                    isActive=0                
                if event.key ==pygame.K_RIGHT or event.key ==pygame.K_d:
                    pc_x_mov = 20
                if event.key ==pygame.K_LEFT or event.key ==pygame.K_a:
                    pc_x_mov = -20
            if event.type==pygame.KEYUP:
                if event.key ==pygame.K_RIGHT or event.key ==pygame.K_LEFT or event.key ==pygame.K_a  or event.key ==pygame.K_d:
                    pc_x_mov = 0
            if event.type == spawn_timer:
                match randint(0,2):
                    case 0:
                        hearts.append(heart_anim[0].get_rect(bottomleft=(randint(0,width-heart_anim[0].get_width()),0)))
                        # hearts.append(heart_anim[0].get_rect(bottomleft=(width-heart_anim[0].get_width(),0)))
                    case 1:
                        rocks.append(rock_anim[0].get_rect(bottomleft=(randint(0,width-rock_anim[0].get_width()),0)))
                        # rocks.append(rock_anim[0].get_rect(bottomleft=(704,0)))
                    case 2:
                        # rocks.append(rock_anim[0].get_rect(bottomleft=(704,0)))
                        rocks.append(rock_anim[0].get_rect(bottomleft=(randint(0,width-rock_anim[0].get_width()),0)))
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
        hearts,rocks = move_objects(hearts,rocks,frame_counter)
        health,hearts,score = collide_hearts(hearts,pc_rect,health,score)
        health, rocks = collide_rocks(rocks,pc_rect,health)
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
