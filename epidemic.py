from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import math

dt = 1.2
y_max = 0.3
K_r_0 = 1/(51-32)
K_r_minus = 0
K_d_0 = 0.02
K_d_plus = 0.02


def K_c(v):
    return 0.4*v


def K_r(y):
    return K_r_0 - K_r_minus/(1+math.exp(-5*(y - y_max)))


def K_d(y):
    return K_d_0 + K_d_plus/(1+math.exp(-5*(y - y_max)))


def calculate_covid(K_c, t_final):
    x_n = 1
    y_n = 0.01
    z_n = 0
    d_n = 0

    def equations(p):
        x, y, z, d = p
        h = (x-x_n)/dt - (-K_c*x*y)
        s = (y-y_n)/dt - (K_c*x*y - K_r(y) * y - K_d(y)*y)
        r = (z-z_n)/dt - (K_r(y)*x*y)
        m = (d-d_n)/dt - (K_d(y)*y)
        return (h, s, r, m)

    time = []
    sick = []
    healthy = []
    recovered = []
    deads = []
    t = 0
    while t < t_final:
        t += dt
        x, y, z, d = fsolve(equations, (x_n, y_n, z_n, d_n))
        x_n, y_n, z_n, d_n = x, y, z, d

        time.append(t)
        sick.append(y)
        healthy.append(x)
        recovered.append(z)
        deads.append(d)

    return time, sick, healthy, recovered, deads
