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
    def __init__(self, L1 = None, L2 = None):
        self.input_size  = 5
        self.hidden_size = 16
        self.output_size = 2

        self.L1 = np.random.randn(self.input_size, self.hidden_size) if L1 is None else L1
        self.L2 = np.random.randn(self.hidden_size, self.output_size) if L2 is None else L2

        self.fitness = 0

    def sigmoid(self, z):
        # return (1 / (1 + np.exp(-z)))
        return 0.5 * (1 + np.tanh(0.5 * z))

    def predict(self, input):
        z2 = input.dot(self.L1)
        a2 = np.tanh(z2)
        z3 = a2.dot(self.L2)
        yHat = self.sigmoid(z3)
        return yHat

    def getData(self):
        return [self.L1.tolist(), self.L2.tolist()]
