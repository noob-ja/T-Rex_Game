from .util import *
import pygame

class Ground():
    def __init__(self, img, speed=-5, scr_size=(600,150)):
        (width,height)=scr_size
        self.image,self.rect = load_image(img,-1,-1,-1)
        self.image1,self.rect1 = load_image(img,-1,-1,-1)
        self.rect.bottom = height
        self.rect1.bottom = height
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self, screen):
        screen.blit(self.image,self.rect)
        screen.blit(self.image1,self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image(img,int(90*30/42),30,-1)
        self.speed = 1
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1*self.speed,0]

    def draw(self, screen):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()

class Scoreboard():
    def __init__(self, img, x=-1, y=-1, scr_size=(600,150)):
        (width,height)=scr_size
        self.score = 0
        self.tempimages,self.temprect = load_sprite_sheet(img,12,1,11,int(11*6/5),-1)
        self.image = pygame.Surface((55,int(11*6/5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = width*0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height*0.1
        else:
            self.rect.top = y

    def draw(self,screen):
        screen.blit(self.image,self.rect)

    def update(self,score,background_col=(235,235,235)):
        score_digits = self.extractDigits(score)
        self.image.fill(background_col)
        for s in score_digits:
            self.image.blit(self.tempimages[s],self.temprect)
            self.temprect.left += self.temprect.width
        self.temprect.left = 0

    def extractDigits(self,number):
        if number > -1:
            digits = []
            i = 0
            while(number/10 != 0):
                digits.append(number%10)
                number = int(number/10)

            digits.append(number%10)
            for i in range(len(digits),5):
                digits.append(0)
            digits.reverse()
            return digits
