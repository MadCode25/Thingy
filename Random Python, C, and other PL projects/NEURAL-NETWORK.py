import numpy as np

# Training data
X = np.array([
    [1, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

# Expected output (OR gate)
y = np.array([
    [0],
    [1],
    [1],
    [1]
])

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

np.random.seed(1)

weights = np.random.rand(2, 1)
bias = np.random.rand(1)

learning_rate = 10
print(sigmoid(np.dot(X, weights) + bias))
