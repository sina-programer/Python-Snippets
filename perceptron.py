import pandas as pd
import numpy as np

class Perceptron:
    def __init__(self, input_dim, learning_rate=.1, bias=1):
        self._is_trained = False
        self.input_dim = input_dim
        self.learning_rate = learning_rate
        self.bias = bias
        self.bias_weight = np.random.random()
        self.weights = np.random.random(size=self.input_dim)

    def train(self, X, y, epochs=200):
        for epoch in range(1, epochs+1):
            print(f"    Epoch: {epoch:<4} ".center(50, '-'))
            total_error = 0

            for idx, row in X.iterrows():
                result = self._predict([row])[0]
                error = y.iloc[idx] - result
                total_error += abs(error)

                self.bias_weight += (self.learning_rate * error * self.bias)
                for i in range(self.input_dim):
                    self.weights[i] += (self.learning_rate * error * row.iloc[i])

            print("Error: ", total_error)

        self._is_trained = True
        print('-'*50)

    def __predict(self, x):
        return Perceptron._activation_function(
            np.sum(x * self.weights) + (self.bias * self.bias_weight)
        )

    def _predict(self, X):
        return list(map(self.__predict, X))

    def predict(self, X):
        if self._is_trained:
            return self._predict(X.values)
        raise PermissionError('First train the model!')

    @staticmethod
    def _activation_function(number):
        if number > 0:
            return 1
        return 0


if __name__ == '__main__':
    df = pd.DataFrame({
        'Distance': [10, 5, 0, 4, 3, 7, 6, 2, 8, 1],
        'Rate': [    10, 5, 0, 1, 4, 5, 6, 2, 9, 1],
        'Prize': [    1, 1, 0, 0, 0, 1, 1, 0, 1, 0]
    })
    print(df)

    X = df.iloc[:, :-1]
    y = df['Prize']

    X_test = pd.DataFrame({
        'Distance': [.5, 7, 0, 6, 9],
        'Rate': [     5, 6, 1, 8, 2],
    })
    y_test = pd.Series([0, 1, 0, 1, pd.NA])

    perseptron = Perceptron(input_dim=len(X.columns))
    perseptron.train(X, y, epochs=20)
    print("Weights: ", perseptron.weights)
    print("Bias / Bias-Weight:  ", perseptron.bias, '/', perseptron.bias_weight)
    X_test['Prize'] = perseptron.predict(X_test)
    X_test['RealPrize'] = y_test
    print(X_test)
