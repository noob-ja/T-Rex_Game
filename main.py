__author__ = "Jen Wai, Yu Kang, Jia Aun"

import os
import sys
import pygame
import random
from pygame import *
import numpy as np

sys.path.append(os.curdir)

from ai.dinoController import *
from codes.util import *
from codes.dino import *
from codes.environment import *
from codes.obstacle import *
import values

scr_size = (width,height) = (600,150)
FPS = 60
gravity = 0.6

black = (0,0,0)
white = (255,255,255)
background_col = (235,235,235)

dinox = 44
dinoy = 47

high_score = 0
iteration = 1
training = values.training
fresh_pop = values.fresh_pop
epoch = values.epoch

play_sound = values.play_sound
human = values.human

class TRex_game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(scr_size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Genetically Modified T-Rex")

        self.jump_sound = pygame.mixer.Sound(values.jump_wav)
        self.die_sound = pygame.mixer.Sound(values.die_wav)
        self.checkPoint_sound = pygame.mixer.Sound(values.checkpoint_wav)

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
        temp_dino = Dino(imgJump=values.dinoJump, imgDuck=values.dinoDuck, sizex=dinox, sizey=dinoy, playSound=play_sound, scr_size=scr_size)
        temp_dino.isBlinking = True
        gameStart = False

        temp_ground,temp_ground_rect = load_sprite_sheet(values.ground,15,1,-1,-1,-1)
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

            temp_dino.update(self.die_sound)

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

        # dino stuff
        if human:
            self.dinoController = DinoController(dinox, dinoy, human, imgJump=values.dinoJump, imgDuck=values.dinoDuck, num_dino=1, num_best_dino=1, play_sound=play_sound, scr_size=scr_size)
        else:
            if not hasattr(self, 'dinoController'):
                self.dinoController = DinoController(dinox, dinoy, human, imgJump=values.dinoJump, imgDuck=values.dinoDuck, play_sound=play_sound, scr_size=scr_size, \
                    num_dino=values.population, num_best_dino=values.best_candidates, \
                    mutation_rate=values.mutation_rate, mutation_range=values.mutation_range, crossing_points=values.crossing_points)
                if not fresh_pop:
                    oldDinos = readWeights()
                    if not oldDinos is None:
                        self.dinoController.loadDinos(oldDinos)
            else:
                self.dinoController.nextGeneration()
        self.dinoController.loadSounds(self.die_sound, self.jump_sound)
        num_dino_alive = self.dinoController.num_dino

        # obstacle and enemy stuff
        self.obstacleController = ObstacleController(imgCactus=values.cactusS, imgPtera=values.ptera, scr_size=scr_size)

        # environment stuff
        self.new_ground = Ground(img=values.ground, speed=-1*gamespeed, scr_size=scr_size)
        self.clouds = pygame.sprite.Group()
        Cloud.containers = self.clouds

        # game datas
        self.scb = Scoreboard(img=values.numbers, scr_size=scr_size)
        self.highsc = Scoreboard(img=values.numbers, x=width*0.78, scr_size=scr_size)
        if not human:
            self.dinoAlive = Scoreboard(img=values.numbers, x=width*0.5, scr_size=scr_size)
            self.iteration = Scoreboard(img=values.numbers, x=width*0.28, scr_size=scr_size)

        # misc stuff
        retbutton_image,retbutton_rect = load_image(values.replay,35,31,-1)
        gameover_image,gameover_rect = load_image(values.game_over,190,11,-1)
        temp_images,temp_rect = load_sprite_sheet(values.numbers,12,1,11,int(11*6/5),-1)
        HI_image = pygame.Surface((22,int(11*6/5)))
        HI_rect = HI_image.get_rect()
        HI_image.fill(background_col)
        HI_image.blit(temp_images[10],temp_rect)
        temp_rect.left += temp_rect.width
        HI_image.blit(temp_images[11],temp_rect)
        HI_rect.top = height*0.1
        HI_rect.left = width*0.73

        counter = 0
        timer = 0
        score = 0

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
                    Cloud(img=values.cloud, x=width, y=random.randrange(height/5,height/2))

                self.dinoController.update(dinoDead, score)
                self.clouds.update()
                self.new_ground.update()
                self.scb.update(score)
                self.highsc.update(high_score)
                if not human:
                    self.dinoAlive.update(num_dino_alive)
                    self.iteration.update(iteration)
                self.obstacleController.update()

                if pygame.display.get_surface() != None:
                    self.screen.fill(background_col)
                    self.new_ground.draw(self.screen)
                    self.clouds.draw(self.screen)
                    self.scb.draw(self.screen)
                    if high_score != 0:
                        self.highsc.draw(self.screen)
                        self.screen.blit(HI_image,HI_rect)
                    if not human:
                        self.dinoAlive.draw(self.screen)
                        self.iteration.draw(self.screen)
                    self.dinoController.draw(self.screen, count_alive==0)
                    self.obstacleController.draw(self.screen)
                    pygame.display.update()
                self.clock.tick(FPS)

                if np.all(dinoDead):
                    gameOver = True
                    if score > high_score:
                        high_score = score
                else:
                    if counter % 7 == 6:
                        score += values.speedup
                        if score % 100 == 0 and score != 0:
                            if pygame.mixer.get_init() != None and play_sound:
                                self.checkPoint_sound.play()

                if counter > 0 and counter%(700/values.speedup) == 0:
                    self.new_ground.speed -= 1
                    gamespeed += 1

                counter = (counter + 1)
                timer = (timer + 1)


            while gameOver:
                if pygame.display.get_surface() == None:
                    print("Couldn't load display surface")
                    gameQuit = True
                    gameOver = False
                else:
                    if not training or (iteration > 0 and iteration%epoch==0):
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
                        iteration = (iteration + 1)
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
