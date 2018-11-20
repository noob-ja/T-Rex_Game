from util import *
import pygame
import random

class Cactus(pygame.sprite.Sprite):
    def __init__(self,speed=5,sizex=-1,sizey=-1,scr_size=(600,150)):
        (width,height)=scr_size
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = load_sprite_sheet('cacti-small.png',3,1,sizex,sizey,-1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width + self.rect.width
        self.image = self.images[random.randrange(0,3)]
        self.movement = [-1*speed,0]

    def draw(self, screen):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()

class Ptera(pygame.sprite.Sprite):
    def __init__(self,speed=5,sizex=-1,sizey=-1,scr_size=(600,150)):
        (width,height)=scr_size
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = load_sprite_sheet('ptera.png',2,1,sizex,sizey,-1)
        self.ptera_height = [height*0.82,height*0.75,height*0.60]
        self.rect.centery = self.ptera_height[random.randrange(0,3)]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1*speed,0]
        self.index = 0
        self.counter = 0

    def draw(self, screen):
        screen.blit(self.image,self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index+1)%2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()

class ObstacleController():
    def __init__(self, scr_size=(600,150)):
        (self.width, self.height) = scr_size

        self.cacti = pygame.sprite.Group()
        self.pteras = pygame.sprite.Group()
        self.last_obstacle = pygame.sprite.Group()
        Cactus.containers = self.cacti
        Ptera.containers = self.pteras

    def _move(self, obstacleGroup, gamespeed, player):
        isDead = False
        for obstacle in obstacleGroup:
            obstacle.movement[0] = -1*gamespeed
            if pygame.sprite.collide_mask(player, obstacle):    isDead = True
        return isDead

    def move(self, gamespeed, player):
        isDead = self._move(self.cacti, gamespeed, player) or self._move(self.pteras, gamespeed, player)
        return isDead

    def spawn(self, gamespeed, counter):
        if len(self.cacti) < 2:
            if len(self.cacti) == 0:
                self.last_obstacle.empty()
                self.last_obstacle.add(Cactus(gamespeed,40,40))
            else:
                for l in self.last_obstacle:
                    if l.rect.right < self.width*0.7 and random.randrange(0,50) == 10:
                        self.last_obstacle.empty()
                        self.last_obstacle.add(Cactus(gamespeed, 40, 40))

        if len(self.pteras) == 0 and random.randrange(0,200) == 10 and counter > 500:
            for l in self.last_obstacle:
                if l.rect.right < self.width*0.8:
                    self.last_obstacle.empty()
                    self.last_obstacle.add(Ptera(gamespeed, 46, 40))

    def update(self):
        self.cacti.update()
        self.pteras.update()

    def draw(self, screen):
        if pygame.display.get_surface() != None:
            self.cacti.draw(screen)
            self.pteras.draw(screen)
