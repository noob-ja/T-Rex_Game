from .generation import *

import sys
import os
sys.path.append(os.pardir)
from dino import *

class DinoController:
    def __init__(self, dino_x, dino_y, num_dino=1, num_best_dino=1, threshold=0.55, scr_size=(600,150)):
        self.dinos = [Dino(dino_x, dino_y) for i in range(num_dino)]
        self.generation = Generation(pop_size=num_dino, best_candidate_size=num_best_dino)
        self.threshold = threshold

        (self.width, self.height) = scr_size

    def move(self, input, jump_sound):
        movements = self.generation.get_outputs(input)
        for i in range(len(movements)):
            jump, duck = movements[i]
            dino = self.dinos[i]

            if jump >= self.threshold:
                if dino.rect.bottom == int(0.98*self.height):
                    dino.isJumping = True
                    if pygame.mixer.get_init() != None:
                        jump_sound.play()
                    dino.movement[1] = -1*dino.jumpSpeed

            if duck >= self.threshold:
                if not (dino.isJumping and dino.isDead):
                    dino.isDucking = True
            else:
                dino.isDucking = False

    def update(self, status, checkPoint_sound):
        for i in range(len(self.dinos)):
            isDead = status[i]
            self.dinos[i].isDead = isDead
            self.dinos[i].update(checkPoint_sound)

            if isDead:
                self.generation.population[i].fitness = self.dinos[i].score

    def draw(self, screen):
        for dino in self.dinos:
            dino.draw(screen)

    def getHighestScore(self):
        score = -1
        for dino in self.dinos:
            if dino.score > score:
                score = dino.score
        return score
