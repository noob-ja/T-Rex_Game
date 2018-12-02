import numpy as np
import copy
import random
from .network import *

class Generation:
    # generate initial population
    def __init__(self, pop_size=10, best_candidate_size=2, mutation_rate=0.5, mutation_range=(0.8, 1.2), crossing_points=1):
        self.max_population_size = pop_size
        self.population = [Network() for i in range(pop_size)]
        self.best_candidate = []
        self.best_candidate_size = best_candidate_size if best_candidate_size < pop_size else pop_size
        self.mutation_rate = mutation_rate
        self.mutation_range = mutation_range
        self.crossing_points = crossing_points

    def loadPopulation(self, candidates):
        self.population = []
        for c in candidates:
            self.population.append(Network(np.array(c[0]), np.array(c[1])))
        for i in range(self.max_population_size - len(candidates)):
            self.population.append(Network())

    def get_best_candidate(self):
        return self.best_candidate

    # only keep the best candidate(s)
    def keep_best_candidate(self):
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        self.population = self.population[:self.best_candidate_size]
        self.best_candidate = self.population

    # mutations
    def mutations(self):
        new_pop = []
        new_pop_size = (self.max_population_size) - len(self.population)
        if new_pop_size > self.max_population_size:
            new_pop_size = self.max_population_size
        if new_pop_size > 0:
            for i in range(new_pop_size):
                candidate = random.choice(self.best_candidate)
                new_pop.append(self.mutate(candidate))
        return new_pop

    # mutate the weight of the layer of the candidate
    def mutate(self, candidate):
        mutated = copy.deepcopy(candidate)
        mutated.L1 = self.mutate_weight(mutated.L1)
        mutated.L2 = self.mutate_weight(mutated.L2)
        return mutated

    # random mutate the weight of layer
    def mutate_weight(self, layer):
        if random.uniform(0, 1) < self.mutation_rate:
            return layer * (random.uniform(*self.mutation_range))
        else:
            return layer

    # crossover
    def crossover(self):
        new_pop = []
        new_pop_size = (self.best_candidate_size*self.best_candidate_size)
        if new_pop_size > self.max_population_size:
            new_pop_size = self.max_population_size
        for i in range(new_pop_size):
            candidate1 = random.choice(self.best_candidate)
            candidate2 = random.choice(self.best_candidate)
            new_pop.append(self.crossing_over(candidate1, candidate2, self.crossing_points))
        return new_pop

    def crossing_over(self, candidate1, candidate2, crossing_points=1):
        c1 = copy.deepcopy(candidate1)
        c2 = copy.deepcopy(candidate2)
        for i in range(crossing_points):
            c1.L1, c2.L1 = self.crossing_over_weight(c1.L1, c2.L1)
            c1.L2, c2.L2 = self.crossing_over_weight(c1.L2, c2.L2)
        return c1

    def crossing_over_weight(self, c1_layer, c2_layer):
        cut_loc = int(len(c1_layer) * random.uniform(0, 1))
        for i in range(cut_loc):
            c1_layer[i], c2_layer[i] = c2_layer[i], c1_layer[i]
        return c1_layer, c2_layer

    # generate new generation
    def generate_new_population(self):
        new_pop = self.crossover()
        for new_pop_ in new_pop:
            self.population.append(self.mutate(new_pop_))
        new_pop = self.mutations()
        for new_pop_ in new_pop:
            self.population.append(new_pop_)
        # ensure that the training will still occur for just a single pop
        if self.max_population_size == 1:
            self.population = [self.population[1]]
        if len(self.population) > self.max_population_size:
            self.population = self.population[:self.max_population_size]

    def get_outputs(self, input):
        input = np.array(input)
        outputs = [pop.predict(input) for pop in self.population]
        return outputs
