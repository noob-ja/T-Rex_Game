import os
import pygame
from pygame import RLEACCEL

import sys
sys.path.append(os.pardir)
import values

def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
    ):

    fullname = os.path.join(values.sprite_path, name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())

def load_sprite_sheet(
        sheetname,
        nx,
        ny,
        scalex = -1,
        scaley = -1,
        colorkey = None,
        ):
    fullname = os.path.join(values.sprite_path,sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()

    sprites = []

    sizex = sheet_rect.width/nx
    sizey = sheet_rect.height/ny

    for i in range(0,ny):
        for j in range(0,nx):
            rect = pygame.Rect((j*sizex,i*sizey,sizex,sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet,(0,0),rect)

            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey,RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image,(scalex,scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites,sprite_rect

def saveWeights(candidate_weights):
    if not os.path.exists(values.weight_path):
        os.makedirs(values.weight_path)
    with open(os.path.join(values.weight_path, values.weight), 'w') as file:
        file.write(str(len(candidate_weights))+'\n')
        for i in range(len(candidate_weights)):
            for layer in candidate_weights[i]:
                weight = ''
                for weights in layer:
                    weight += ','.join(str(w) for w in weights) + ';'
                file.write(weight[:-1]+'\n')

def readWeights():
    if not os.path.exists(values.weight_path):
        os.makedirs(values.weight_path)
    candidates = []
    if not os.path.isfile(os.path.join(values.weight_path, values.weight)):
        return None
    with open(os.path.join(values.weight_path, values.weight), 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        if not lines:
            return None
        num_candidates = int(lines[0])
        for i in range(num_candidates):
            l1 = lines[i*2+1]
            l2 = lines[i*2+2]
            l1 = [[float(weight) for weight in weights.split(',')] for weights in l1.split(';')]
            l2 = [[float(weight) for weight in weights.split(',')] for weights in l2.split(';')]
            candidates.append([l1,l2])
    return candidates
