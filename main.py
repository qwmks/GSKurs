import pygame
import sys

from pygame.constants import KEYDOWN
import spritesheet

from pygame.time import Clock

width = 852
height = 480
pygame.init()
screen = pygame.display.set_mode((width,height))
font = pygame.font.Font(None,50)
rock_image = pygame.image.load('rock.png').convert_alpha()
rock_sprite_sheet = spritesheet.SpriteSheet(rock_image)

health = 3
health_surface = font.render("This is the health",True,'Red')
health_rect = health_surface.get_rect(topright = (width,0))

pygame.display.set_caption("Super Runner")
timer = pygame.time.Clock()

rock_image = pygame.image.load('rock.png').convert_alpha()
rock_x = 400
rock_y = 250

base_background = pygame.image.load('grass.jpg').convert_alpha()

score_surface = font.render("This is the score",True,'Red')
score_rect = score_surface.get_rect(topleft = (0,0))

pause_surface = font.render("The game is paused",True,'Red')
pause_rect = pause_surface.get_rect(center=(width/2,height/2 ))

pc_surface = pygame.image.load('running.png').convert_alpha()
pc_sprite_sheet = spritesheet.SpriteSheet(pc_surface)

isActive =1

frame_counter = 0

BG = (50, 50, 50)
BLACK = (0, 0, 0)
rock_anim = []
pc_anim = []
pc_x = 400
for i in range(4):
    rock_anim.append(rock_sprite_sheet.get_image(i, 32, 32, 3, BLACK)) 
for i in range(9):
    pc_anim.append(pc_sprite_sheet.get_image(i, 64, 64, 3, BLACK)) 
pc_rect = pc_anim[0].get_rect(bottomleft = (pc_x,height))
rock_rect = rock_anim[0].get_rect(midbottom =(rock_x,rock_y))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if isActive:
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_RIGHT:
                    pc_rect.x+=10
                if event.key ==pygame.K_LEFT:
                    pc_rect.x-=20
                if event.key ==pygame.K_SPACE:
                    isActive=0                
        else:
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_SPACE:
                    isActive=1
    if isActive:
        rock_rect.y+=4
        if rock_rect.y>height:
            rock_rect.y=0
        screen.blit(base_background,(0,0))
        screen.blit(score_surface,score_rect)
        screen.blit(health_surface,health_rect)
        screen.blit(pc_anim[frame_counter%9],pc_rect)
        screen.blit(rock_anim[frame_counter%4],rock_rect)
        frame_counter+=1
        if frame_counter>72:
            frame_counter= 0
        if pc_rect.colliderect(rock_rect):
            rock_rect.y =0
            health-=1
            if health<0:
                pygame.quit()
                sys.exit()
    else:
        screen.blit(pause_surface,pause_rect)
    pygame.display.update()
    timer.tick(30)
