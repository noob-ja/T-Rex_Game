from .generation import *

import sys
import os
sys.path.append(os.pardir)
from dino import *

class DinoController:
    def __init__(self, dino_x, dino_y, human, num_dino=1, num_best_dino=1, threshold=0.55, scr_size=(600,150), play_sound=True):
        self.dino_x, self.dino_y = dino_x, dino_y
        self.num_dino = num_dino
        self.dinos = [Dino(self.dino_x, self.dino_y,playSound=play_sound) for i in range(self.num_dino)]
        if not human:
            self.generation = Generation(pop_size=num_dino, best_candidate_size=num_best_dino)
            self.threshold = threshold
        (self.width, self.height) = scr_size
        self.play_sound = play_sound

    def loadDinos(self, dino_weights):
        self.generation.loadPopulation(dino_weights)

    def loadSounds(self, checkPoint_sound, die_sound, jump_sound):
        self.checkPoint_sound = checkPoint_sound
        self.die_sound = die_sound
        self.jump_sound = jump_sound

    def update(self, status):
        for i in range(len(self.dinos)):
            self.dinos[i].isDead = status[i]
            self.dinos[i].update(self.checkPoint_sound, self.die_sound)

    def draw(self, screen, last_dead):
        for dino in self.dinos:
            dino.draw(screen, last_dead)

    # movements
    def moveHuman(self):
        dino = self.dinos[0]
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    dino.jump(self.jump_sound)
                if event.key == pygame.K_DOWN:
                    dino.duck()
            elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                dino.unduck()

    def moveAI(self, input):
        movements = self.generation.get_outputs(input)
        for i in range(len(movements)):
            jump, duck = movements[i]
            dino = self.dinos[i]

            if dino.isDead: continue

            if jump >= self.threshold: dino.jump(self.jump_sound)
            if duck >= self.threshold: dino.duck()
            else: dino.unduck()

            self.generation.population[i].fitness = self.dinos[i].score

    def getHighestScore(self):
        score = -1
        for dino in self.dinos:
            if dino.score > score:
                score = dino.score
        return score

    def nextGeneration(self):
        self.dinos = [Dino(self.dino_x, self.dino_y,playSound=self.play_sound) for i in range(self.num_dino)]
        self.generation.keep_best_candidate()
        self.generation.generate_new_population()

    def getBestCandidatesData(self):
        if not self.generation.get_best_candidate():
            self.generation.keep_best_candidate()
        candidates = self.generation.get_best_candidate()
        weights = []
        for c in candidates:
            weight = c.getData()
            weights.append(weight)
        return weights
