import codes.util
from ai.generation import *

a = Generation()
a.keep_best_candidate()

candidates = a.get_best_candidate()
weights = []
for c in candidates:
    weight = c.getData()
    weights.append(weight)

print(weights)

util.saveWeights(weights)s
