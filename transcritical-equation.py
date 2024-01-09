from matplotlib import pyplot as plt
import numpy as np

PHI_MIN = 0
PHI_MAX = 1
PHI_STEP = 0.01

K = 13
M = np.arange(1.43, 1.45, .005)
MU = 1.16
DELTA = .15
SIGMA = 3e-5

def f(phi, k=K, m=M, mu=MU, delta=DELTA, sigma=SIGMA):  # the first formula
    s1 = np.sqrt((m**2 - 2*phi + 3*sigma) ** 2 - 12*sigma*m**2)
    c1 = (np.sqrt(2) * mu * m) / 2 * (np.sqrt(m**2 - 2*phi + 3*sigma + s1) + (4*sigma*m**2) / (np.sqrt(m**2 - 2*phi - 3*sigma + s1) ** (3/2)))
    return 1 - (1 - (2*phi)/(2*k-3)) ** (-k + 3/2) + c1 - delta


def g(phi, k=K, m=M, mu=MU, delta=DELTA, sigma=SIGMA):  # the second formula
    SIGMA0 = np.sqrt(3*sigma / m**2)
    SIGMA1 = np.sqrt(SIGMA0**2 + 1)
    TETA = np.arccosh((SIGMA1**2) / (2*SIGMA0) * (1 - (2*phi / (m**2 * SIGMA1**2))))
    C1 = mu * m**2 * np.sqrt(SIGMA0) * (np.exp(.5 * np.arccosh((SIGMA1**2) / (2*SIGMA0)) + 1/3 * np.exp(-3/2 * np.arccosh(SIGMA1**2) / (2*SIGMA0))))
    C2 = (mu * m**2 * np.sqrt(SIGMA0) * (np.exp(TETA/2)) + (1/3 * np.exp(-3*TETA/2)))
    V = 1 - (1 - (2*phi / (2*k - 3))) ** (-k + 1.5) - (delta*phi) + C1 - C2 - 0.285
    return V - V[0]


x = np.arange(PHI_MIN, PHI_MAX+PHI_STEP, PHI_STEP)
for m in M:
    m = round(m, 3)
    plt.plot(x, g(x, m=m), label=f'M = {m}')

plt.ylabel('V($\phi$)')
plt.xlabel('$\phi$')
plt.xlim(PHI_MIN, PHI_MAX)
plt.tight_layout()
plt.autoscale()
plt.grid(True)
plt.legend()
plt.show()
