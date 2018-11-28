import numpy as np

'''
Input
0 - distance
1 - vertical distance
2 - width of obstacle
3 - height of obstacle

Output
0 - jump
1 - duck
'''

class Network:
    def __init__(self):
        self.input_size  = 4
        self.hidden_size = 4
        self.output_size = 2

        self.L1 = np.random.randn(self.input_size, self.hidden_size)
        self.L2 = np.random.randn(eslf.hidden_size, self.output_size)

        self.fitness = 0

    #the logistic function of Logistic Regression
    def sigmoid(self, z):
        return (1 / (1 + np.exp(-z)))

    def predict(self, input):
        z2 = input.dot(self.L1)
        a2 = np.tanh(z2)
        z3 = a2.dot(self.L2)
        yHat = np.tanh(z3)
        return yHat
