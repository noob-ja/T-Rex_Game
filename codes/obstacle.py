from util import *
import pygame
import random
from collections import deque
from dino import *

queue = deque()
dino_right = 84

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
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()
            queue.popleft()

        if self.rect.left < dino_right and len(queue) > 0 and self.limit > 0:
            # print('popcat.............................')
            self.limit = self.limit -1
            # queue.popleft()


class Ptera(pygame.sprite.Sprite):
    def __init__(self,speed=5,sizex=-1,sizey=-1,scr_size=(600,150)):
        (width,height)=scr_size
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images, self.rect = load_sprite_sheet('ptera.png',2,1,sizex,sizey,-1)
        self.ptera_height = [height*0.82,height*0.75,height*0.60,height*0.20]
        self.rect.centery = self.ptera_height[random.randrange(0,len(self.ptera_height))]
        # self.rect.centery = random.uniform(0.2,0.82)*height
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1*speed,0]
        self.index = 0
        self.limit = 1
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
            queue.popleft()

        if self.rect.left < dino_right and len(queue) > 0 and self.limit > 0:
            # print('poptera.............................')
            self.limit = self.limit - 1
            # queue.popleft()

class ObstacleController():
    def __init__(self, scr_size=(600,150)):
        (self.width, self.height) = scr_size

        self.cacti = pygame.sprite.Group()
        self.pteras = pygame.sprite.Group()
        self.last_obstacle = pygame.sprite.Group()
        Cactus.containers = self.cacti
        Ptera.containers = self.pteras

        queue.clear()

    def collide(self, dino):
        if len(queue) > 0:
            for obs in queue:
                if obs.rect.left <= 90:
                    if pygame.sprite.collide_mask(dino, obs):
                        return True
        return False

    def _move(self, obstacleGroup, gamespeed, player=None):
        for obstacle in obstacleGroup:
            obstacle.movement[0] = -1*gamespeed

        if not player is None:
            return self.collide(player)
        else:
            return False


    def move(self, gamespeed, player=None):
        isDead = self._move(self.cacti, gamespeed, player) or self._move(self.pteras, gamespeed, player)
        return isDead

    def spawn(self, gamespeed, counter):
        value = random.randrange(0,10)
        new_obs = False
        if(value >= 5 and value <= 7):
            new_obs = Ptera(gamespeed, 46, 40)
        else:
            new_obs = Cactus(gamespeed,40,40)
        self.last_obstacle.empty()
        self.last_obstacle.add(new_obs)
        queue.append(new_obs)

    def update(self):
        self.cacti.update()
        self.pteras.update()

    def draw(self, screen):
        if pygame.display.get_surface() != None:
            self.cacti.draw(screen)
            self.pteras.draw(screen)

    def get_info(self):
        if len(queue)>0:
            obst = False
            for obs in queue:
                if obs.rect.left > 84:
                    obst = obs
                    break
            if obst == False:
                return [-1, -1, -1, -1]
            dist = obst.rect.left - 84
            dist_vert = self.height - obst.rect.bottom
            width = obst.rect.right - obst.rect.left
            height = obst.rect.bottom - obst.rect.top
            return [dist, dist_vert, width, height]
        else:
            return [-1, -1, -1, -1]
