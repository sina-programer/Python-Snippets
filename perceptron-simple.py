import numpy as np

def loss(y_true, y_pred):
    return np.sum(np.power(np.array(y_true) - np.array(y_pred), 2))

def activation(x, threshold=0):
    if np.mean(x) >= threshold:
        return 1
    return 0

def predict(X, weights, bias):  
    return list(map(activation, np.dot(X, weights.T) + bias))

def perceptron(X, y, n=1, learning_rate=0.1, epochs=100, threshold=0):    
    weights = np.random.rand(n, len(X[0]))
    bias = np.random.rand(n)
    for epoch in range(epochs):
        for inputs, output in zip(X, y):
            linear_output = np.dot(weights, inputs) + bias
            predicted = np.where(linear_output>=threshold, 1, 0)
            error = output - predicted

            weights += learning_rate * error[:, np.newaxis] * inputs
            bias += learning_rate * error

    return weights, bias

X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])
y = np.array([0, 0, 0, 1])

weights, bias = perceptron(X, y, learning_rate=0.1, epochs=10)
predicted = predict(X, weights, bias)

print("Weights:", weights)
print("Bias:", bias)
print('Predict:', predicted)
print('Error:', loss(y, predicted))
