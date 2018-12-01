__author__ = "Jen Wai, Yu Kang, Jia Aun"

import os
import sys
import pygame
import random
from pygame import *
import numpy as np

from ai.dinoController import *
from util import *
from dino import *
from environment import *
from obstacle import *

scr_size = (width,height) = (600,150)
FPS = 60
gravity = 0.6

black = (0,0,0)
white = (255,255,255)
background_col = (235,235,235)

high_score = 0

iteration = 1
training = False
fresh_pop = True
epoch = 1

play_sound = True
human = True

class TRex_game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(scr_size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Genetically Modified T-Rex")

        self.jump_sound = pygame.mixer.Sound('../sprites/jump.wav')
        self.die_sound = pygame.mixer.Sound('../sprites/die.wav')
        self.checkPoint_sound = pygame.mixer.Sound('../sprites/checkPoint.wav')

    def disp_gameOver_msg(self,retbutton_image,gameover_image):
        retbutton_rect = retbutton_image.get_rect()
        retbutton_rect.centerx = width / 2
        retbutton_rect.top = height*0.52

        gameover_rect = gameover_image.get_rect()
        gameover_rect.centerx = width / 2
        gameover_rect.centery = height*0.35

        self.screen.blit(retbutton_image, retbutton_rect)
        self.screen.blit(gameover_image, gameover_rect)

    def intro(self):
        temp_dino = Dino(44,47,playSound=play_sound)
        temp_dino.isBlinking = True
        gameStart = False

        temp_ground,temp_ground_rect = load_sprite_sheet('ground.png',15,1,-1,-1,-1)
        temp_ground_rect.left = width/20
        temp_ground_rect.bottom = height

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
                            temp_dino.jump(self.jump_sound)
                            temp_dino.isBlinking = False

            temp_dino.update(self.checkPoint_sound, self.die_sound)

            if pygame.display.get_surface() != None:
                self.screen.fill(background_col)
                self.screen.blit(temp_ground[0],temp_ground_rect)
                temp_dino.draw(self.screen, True)

                pygame.display.update()

            self.clock.tick(FPS)
            if temp_dino.isJumping == False and temp_dino.isBlinking == False:
                gameStart = True

        return False

    def gameplay(self):
        global high_score, iteration
        gamespeed = 10
        startMenu = False
        gameOver = False
        gameQuit = False

        if human:
            self.dinoController = DinoController(44, 47, human, num_dino=1, num_best_dino=1, play_sound=play_sound)
        else:
            if not hasattr(self, 'dinoController'):
                self.dinoController = DinoController(44, 47, human, num_dino=5, num_best_dino=2, play_sound=play_sound)
                if not fresh_pop:
                    oldDinos = readWeights()
                    if not oldDinos is None:
                        self.dinoController.loadDinos(oldDinos)
            else:
                self.dinoController.nextGeneration()
        self.dinoController.loadSounds(self.checkPoint_sound, self.die_sound, self.jump_sound)
        num_dino_alive = self.dinoController.num_dino

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
                    break

                if human:
                    self.dinoController.moveHuman()
                else:
                    inputs = self.obstacleController.get_info() + [gamespeed]
                    self.dinoController.moveAI(inputs)

                self.obstacleController.move(gamespeed)

                dinoDead = []
                for dino in self.dinoController.dinos:
                    if dino.isDead: dinoDead.append(True)
                    else:           dinoDead.append(self.obstacleController.collide(dino))

                count_alive = np.size(dinoDead) - np.count_nonzero(dinoDead)
                if count_alive != num_dino_alive:
                    num_dino_alive = count_alive
                    print("Dino alive: ", count_alive)

                spawn_time = random.randrange(50, 150)
                if(timer >= spawn_time):
                    self.obstacleController.spawn(gamespeed, counter)
                    timer = 0

                if len(self.clouds) < 5 and random.randrange(0,300) == 10:
                    Cloud(width,random.randrange(height/5,height/2))

                high_score_curr = self.dinoController.getHighestScore()

                self.dinoController.update(dinoDead)
                self.clouds.update()
                self.new_ground.update()
                self.scb.update(high_score_curr)
                self.highsc.update(high_score)
                self.obstacleController.update()

                if pygame.display.get_surface() != None:
                    self.screen.fill(background_col)
                    self.new_ground.draw(self.screen)
                    self.clouds.draw(self.screen)
                    self.scb.draw(self.screen)
                    if high_score != 0:
                        self.highsc.draw(self.screen)
                        self.screen.blit(HI_image,HI_rect)
                    self.dinoController.draw(self.screen, count_alive==0)
                    self.obstacleController.draw(self.screen)

                    pygame.display.update()
                self.clock.tick(FPS)

                if np.all(dinoDead):
                    gameOver = True
                    if high_score_curr > high_score:
                        high_score = high_score_curr

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
                    if iteration >= epoch:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                gameQuit = True
                                gameOver = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                    gameOver = False
                                else:
                                    gameQuit = True
                                    gameOver = False

                    else:
                        gameOver = False
                self.highsc.update(high_score)
                if pygame.display.get_surface() != None:
                    self.disp_gameOver_msg(retbutton_image,gameover_image)
                    if high_score != 0:
                        self.highsc.draw(self.screen)
                        self.screen.blit(HI_image,HI_rect)
                    pygame.display.update()
                self.clock.tick(FPS)

                if gameOver == False and gameQuit == False:
                    if not human:
                        print("iteration: ",iteration)
                        iteration = (iteration + 1) % epoch
                        if training:
                            saveWeights(self.dinoController.getBestCandidatesData())
                    self.gameplay()

        pygame.quit()
        quit()

    def main(self):
        isGameQuit = self.intro()
        if not isGameQuit:
            self.gameplay()

TRex_game().main()
