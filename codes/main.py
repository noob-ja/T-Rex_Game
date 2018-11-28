__author__ = "Jen Wai, Yu Kang, Jia Aun"

import os
import sys
import pygame
import random
from pygame import *

from util import *
from dino import *
from environment import *
from obstacle import *

pygame.init()

scr_size = (width,height) = (600,150)
FPS = 60
gravity = 0.6

black = (0,0,0)
white = (255,255,255)
background_col = (235,235,235)

high_score = 0

screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()
pygame.display.set_caption("T-Rex Rush")

jump_sound = pygame.mixer.Sound('../sprites/jump.wav')
die_sound = pygame.mixer.Sound('../sprites/die.wav')
checkPoint_sound = pygame.mixer.Sound('../sprites/checkPoint.wav')

class TRex_game():

    def disp_gameOver_msg(self,retbutton_image,gameover_image):
        retbutton_rect = retbutton_image.get_rect()
        retbutton_rect.centerx = width / 2
        retbutton_rect.top = height*0.52

        gameover_rect = gameover_image.get_rect()
        gameover_rect.centerx = width / 2
        gameover_rect.centery = height*0.35

        screen.blit(retbutton_image, retbutton_rect)
        screen.blit(gameover_image, gameover_rect)

    def introscreen(self):
        temp_dino = Dino(44,47)
        temp_dino.isBlinking = True
        gameStart = False

        callout,callout_rect = load_image('call_out.png',196,45,-1)
        callout_rect.left = width*0.05
        callout_rect.top = height*0.4

        temp_ground,temp_ground_rect = load_sprite_sheet('ground.png',15,1,-1,-1,-1)
        temp_ground_rect.left = width/20
        temp_ground_rect.bottom = height

        logo,logo_rect = load_image('logo.png',240,40,-1)
        logo_rect.centerx = width*0.6
        logo_rect.centery = height*0.6
        while not gameStart:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                return True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                            temp_dino.isJumping = True
                            temp_dino.isBlinking = False
                            temp_dino.movement[1] = -1*temp_dino.jumpSpeed

            temp_dino.update(checkPoint_sound)

            if pygame.display.get_surface() != None:
                screen.fill(background_col)
                screen.blit(temp_ground[0],temp_ground_rect)
                if temp_dino.isBlinking:
                    screen.blit(logo,logo_rect)
                    screen.blit(callout,callout_rect)
                temp_dino.draw(screen)

                pygame.display.update()

            clock.tick(FPS)
            if temp_dino.isJumping == False and temp_dino.isBlinking == False:
                gameStart = True

    def gameplay(self):
        global high_score
        gamespeed = 4
        startMenu = False
        gameOver = False
        gameQuit = False

        self.playerDino = Dino(44,47)
        self.new_ground = Ground(-1*gamespeed)
        self.scb = Scoreboard()
        self.highsc = Scoreboard(width*0.78)
        counter = 0
        timer = 0

        self.clouds = pygame.sprite.Group()
        Cloud.containers = self.clouds

        self.obstacleController = ObstacleController(scr_size)

        retbutton_image,retbutton_rect = load_image('replay_button.png',35,31,-1)
        gameover_image,gameover_rect = load_image('game_over.png',190,11,-1)

        temp_images,temp_rect = load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
        HI_image = pygame.Surface((22,int(11*6/5)))
        HI_rect = HI_image.get_rect()
        HI_image.fill(background_col)
        HI_image.blit(temp_images[10],temp_rect)
        temp_rect.left += temp_rect.width
        HI_image.blit(temp_images[11],temp_rect)
        HI_rect.top = height*0.1
        HI_rect.left = width*0.73

        while not gameQuit:
            while startMenu:
                pass
            while not gameOver:

                if pygame.display.get_surface() == None:
                    print("Couldn't load display surface")
                    gameQuit = True
                    gameOver = True
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            gameQuit = True
                            gameOver = True

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                if self.playerDino.rect.bottom == int(0.98*height):
                                    self.playerDino.isJumping = True
                                    if pygame.mixer.get_init() != None:
                                        jump_sound.play()
                                    self.playerDino.movement[1] = -1*self.playerDino.jumpSpeed

                            if event.key == pygame.K_DOWN:
                                if not (self.playerDino.isJumping and self.playerDino.isDead):
                                    self.playerDino.isDucking = True

                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_DOWN:
                                self.playerDino.isDucking = False

                if self.obstacleController.move(gamespeed, self.playerDino): # true if player is dead
                    self.playerDino.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()

                spawn_time = random.randrange(50, 150)
                print('sss',spawn_time)
                print('timer', timer)
                if(timer >= spawn_time):
                    self.obstacleController.spawn(gamespeed, counter)
                    timer = 0

                if len(self.clouds) < 5 and random.randrange(0,300) == 10:
                    Cloud(width,random.randrange(height/5,height/2))

                self.playerDino.update(checkPoint_sound)
                self.clouds.update()
                self.new_ground.update()
                self.scb.update(self.playerDino.score)
                self.highsc.update(high_score)
                self.obstacleController.update()

                if pygame.display.get_surface() != None:
                    screen.fill(background_col)
                    self.new_ground.draw(screen)
                    self.clouds.draw(screen)
                    self.scb.draw(screen)
                    if high_score != 0:
                        self.highsc.draw(screen)
                        screen.blit(HI_image,HI_rect)
                    self.playerDino.draw(screen)
                    self.obstacleController.draw(screen)

                    pygame.display.update()
                clock.tick(FPS)

                if self.playerDino.isDead:
                    gameOver = True
                    if self.playerDino.score > high_score:
                        high_score = self.playerDino.score

                if counter%700 == 699:
                    self.new_ground.speed -= 1
                    gamespeed += 1

                counter = (counter + 1)
                timer = (timer + 1)

            if gameQuit:
                break

            while gameOver:
                if pygame.display.get_surface() == None:
                    print("Couldn't load display surface")
                    gameQuit = True
                    gameOver = False
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            gameQuit = True
                            gameOver = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                gameQuit = True
                                gameOver = False

                            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                gameOver = False
                                self.gameplay()
                self.highsc.update(high_score)
                if pygame.display.get_surface() != None:
                    self.disp_gameOver_msg(retbutton_image,gameover_image)
                    if high_score != 0:
                        self.highsc.draw(screen)
                        screen.blit(HI_image,HI_rect)
                    pygame.display.update()
                clock.tick(FPS)

        pygame.quit()
        quit()

    def main(self):
        isGameQuit = self.introscreen()
        if not isGameQuit:
            self.gameplay()

TRex_game().main()
