from matplotlib import pyplot as plt
import numpy as np


points = 50
velocity = 1  # u
final_time = 10
time_step = 0.001

x = np.linspace(0, 1, points+1)
dx = 1 / points

U = 0.75 * np.exp(-((x-.5) / .1) ** 2)  # initial condition
for _ in range(int(final_time / time_step)):
    U[1:] = U[1:] - (time_step * velocity * np.gradient(U[1:]))  # forward Euler step
    U[0] = U[-1]  # enforce periodicity


plt.plot(x, U, 'x-', markerfacecolor='red', markeredgecolor='red')
plt.title(f't = {final_time}')
plt.xlabel('X')
plt.ylabel('U')
plt.grid()
plt.show()
