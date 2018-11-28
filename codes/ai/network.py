import numpy as np

'''
Input
0 - distance
1 - vertical distance
2 - width of obstacle
3 - height of obstacle
4 - speed

Output
0 - jump
1 - duck
'''

class Network:
    def __init__(self):
        self.input_size  = 5
        self.hidden_size = 8
        self.output_size = 2

        self.L1 = np.random.randn(self.input_size, self.hidden_size)
        self.L2 = np.random.randn(self.hidden_size, self.output_size)

        self.fitness = 0

    def predict(self, input):
        z2 = input.dot(self.L1)
        a2 = np.tanh(z2)
        z3 = a2.dot(self.L2)
        yHat = np.tanh(z3)
        return yHat
