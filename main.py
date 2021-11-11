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

def collide_hearts(hearts,player,health):
    if hearts:
        for heart in hearts:
            if player.colliderect(heart):
                health+=1
                heart.x = 901
        if health>5:
            health =5
        hearts = [heart for heart in hearts if heart.x!=901]
    return health,hearts
def collide_rocks(rocks,player,health):
    if rocks:
        for rock in rocks:
            if player.colliderect(rock):
                health-=1
                rock.x =901
                if health<0:
                    rocks = [rock for rock in rocks if rock.x!=901]
                    return -1,rocks
    return health,rocks
width = 852
height = 480
pygame.init()
pygame.display.set_caption("Super Runner")
screen = pygame.display.set_mode((width,height))
font = pygame.font.Font(None,50)
base_background = pygame.image.load('grass.jpg').convert_alpha()
health = 3
score = 0

timer = pygame.time.Clock()

pause_surface = font.render("The game is paused",True,'Red')
pause_rect = pause_surface.get_rect(center=(width/2,height/2 ))
# objects 
pc_surface = pygame.image.load('running.png').convert_alpha()
pc_sprite_sheet = spritesheet.SpriteSheet(pc_surface)
pc_anim = []
pc_x = 400
for i in range(9):
    # pc_anim.append(pc_sprite_sheet.get_image(i, 64, 64, 3, (0, 0, 0))) 
    pc_anim.append(pc_sprite_sheet.get_player(i, 36, 50, 3, (0, 0, 0))) 
pc_rect = pc_anim[0].get_rect(bottomleft = (pc_x,height))
print(pc_rect.width)

rock_image = pygame.image.load('rock.png').convert_alpha()
rock_sprite_sheet = spritesheet.SpriteSheet(rock_image)
rock_x = 400
rock_y = 250
rock_anim = []
for i in range(4):
    rock_anim.append(rock_sprite_sheet.get_image(i, 32, 32, 3, (0, 0, 0))) 
rock_rect = rock_anim[0].get_rect(midbottom =(rock_x,rock_y))
rocks = []

heart_image = pygame.image.load('heart.png').convert_alpha()
heart_sprite_sheet = spritesheet.SpriteSheet(heart_image)
heart_x = 300
heart_y = 250
heart_anim = []
for i in range(6):
    heart_anim.append(heart_sprite_sheet.get_image(i, 64, 64, 1, (0, 0, 0))) 
heart_rect = heart_anim[0].get_rect(midbottom =(heart_x,heart_y))
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
                if event.key ==pygame.K_RIGHT:
                    pc_rect.x+=20
                elif event.key ==pygame.K_LEFT:
                    pc_rect.x-=20
            if event.type == spawn_timer:
                match randint(0,2):
                    case 0:
                        hearts.append(heart_anim[0].get_rect(bottomleft=(randint(0,800),0)))
                    case 1:
                        rocks.append(rock_anim[0].get_rect(bottomleft=(randint(0,800),0)))
                    case 2:
                        rocks.append(rock_anim[0].get_rect(bottomleft=(randint(0,800),0)))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_SPACE:
                    isActive=1
    if isActive:
        screen.blit(base_background,(0,0))
        show_score(score)
        show_health(health)
        screen.blit(pc_anim[frame_counter%9],pc_rect)
        pygame.draw.rect(screen,(255,0,0),pc_rect,2)
        hearts,rocks = move_objects(hearts,rocks,frame_counter)
        health,hearts = collide_hearts(hearts,pc_rect,health)
        health, rocks = collide_rocks(rocks,pc_rect,health)
        if health == -1:
                pygame.quit()
                sys.exit()
        # rock_rect.y+=4
        # if rock_rect.y>height:
        #     rock_rect.y=0
        # screen.blit(rock_anim[frame_counter%4],rock_rect)
        frame_counter+=1
        if frame_counter>72:
            frame_counter= 0
        # if pc_rect.colliderect(rock_rect):
        #     rock_rect.y =0
        #     health-=1
        #     if health<0:
        #         pygame.quit()
        #         sys.exit()
    else:
        screen.blit(pause_surface,pause_rect)
    pygame.display.update()
    timer.tick(30)
