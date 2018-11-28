from util import *
import pygame
import random
from collections import deque
from dino import *

queue = deque([])
dino_right = 84
distance = 0

class Cactus(pygame.sprite.Sprite):
    def __init__(self,speed=5,sizex=-1,sizey=-1,scr_size=(600,150)):
        (width,height)=scr_size
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images, self.rect = load_sprite_sheet('cacti-small.png',3,1,sizex,sizey,-1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width + self.rect.width
        self.image = self.images[random.randrange(0,3)]
        self.movement = [-1*speed,0]
        self.limit = 1

    def draw(self, screen):
        screen.blit(self.image,self.rect)

    def update(self):
        # print('xxxxxxxxxxxxxxxxxxxxxxxx')
        self.rect = self.rect.move(self.movement)

       

        if self.rect.right < 0:
            self.kill()
        # print('<',self.rect.left < dino_right, 'left:', self.rect.left, 'dino: ',dino_right)
        # print('len', len(queue))
        if self.rect.left < dino_right and len(queue) > 0 and self.limit > 0:
            # print('popcat.............................')
            self.limit = self.limit -1
            queue.popleft()



class Ptera(pygame.sprite.Sprite):
    def __init__(self,speed=5,sizex=-1,sizey=-1,scr_size=(600,150)):
        (width,height)=scr_size
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images, self.rect = load_sprite_sheet('ptera.png',2,1,sizex,sizey,-1)
        self.ptera_height = [height*0.82,height*0.75,height*0.60]
        self.rect.centery = self.ptera_height[random.randrange(0,3)]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1*speed,0]
        self.index = 0
        self.limit = 1
        self.counter = 0

    def draw(self, screen):
        screen.blit(self.image,self.rect)

    def update(self):
        # print('yyyyyyyyyyyyyyyyyyy')
        if self.counter % 10 == 0:
            self.index = (self.index+1)%2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)


        if self.rect.right < 0:
            self.kill()

        if self.rect.left < dino_right and len(queue) > 0 and self.limit > 0:
            # print('poptera.............................')
            self.limit = self.limit - 1
            queue.popleft()

class ObstacleController():
    def __init__(self, scr_size=(600,150)):
        (self.width, self.height) = scr_size

        self.cacti = pygame.sprite.Group()
        self.pteras = pygame.sprite.Group()
        self.last_obstacle = pygame.sprite.Group()
        Cactus.containers = self.cacti
        Ptera.containers = self.pteras

    def collide(self, player):
        if(len(queue) > 0):
            # print()
            if pygame.sprite.collide_mask(player, queue[0]):
                print('collide')
                return True
        return False

    def _move(self, obstacleGroup, gamespeed, player):
        isDead = False
        for obstacle in obstacleGroup:
            obstacle.movement[0] = -1*gamespeed
            if pygame.sprite.collide_mask(player, obstacle):    isDead = True
        # return self.collide(player)
        return isDead


    def move(self, gamespeed, player):
        isDead = self._move(self.cacti, gamespeed, player) or self._move(self.pteras, gamespeed, player)
        return isDead

    def spawn(self, gamespeed, counter):
        value = random.randrange(0,10)
        new_obs = False
        if(value == 5 or value == 6):
            new_obs = Ptera(gamespeed, 46, 40)
        else:
            new_obs = Cactus(gamespeed,40,40)
        self.last_obstacle.empty()
        self.last_obstacle.add(new_obs)
        queue.append(new_obs)

    def update(self):
        global distance
        if(len(queue)>0):
            distance = queue[0].rect.left
        # print(queue)
        if(len(queue)>0):
            print('dist', queue[0].rect.left)
        self.cacti.update()
        self.pteras.update()

    def draw(self, screen):
        if pygame.display.get_surface() != None:
            self.cacti.draw(screen)
            self.pteras.draw(screen)

    global get_Distance
    def get_Distance():
        return distance
