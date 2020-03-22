from scipy.optimize import fsolve
import math


def calculate_epidemic(C, v, t_final, x_n=1, y_n=0.01, K_r_0=1/(51-32),
                       K_r_minus=1/(51-32)/2, K_d_0=0.02, K_d_plus=0.01):
    '''
    Arguments:
    - C: Hospital capacity
    - v: People's mobility (0 means perfect confinement)
    - t_final: time of simulation
    Returns: 5 lists
    '''
    dt = 5e-1

    def K_c(v):
        return 0.4*v

    def K_r(y):
        if y < C:
            return K_r_0
        else:
            return K_r_0 - K_r_minus

    def K_d(y):
        if y < C:
            return K_d_0
        else:
            return K_d_0 + K_d_plus

    z_n = 0
    d_n = 0

    def equations(p):
        x, y, z, d = p
        h = (x-x_n)/dt - (-K_c(v)*x*y)
        s = (y-y_n)/dt - (K_c(v)*x*y - K_r(y) * y - K_d(y)*y)
        r = (z-z_n)/dt - (K_r(y)*y)
        m = (d-d_n)/dt - (K_d(y)*y)
        return (h, s, r, m)

    time = []
    sick = []
    healthy = []
    recovered = []
    deaths = []
    t = 0
    while t < t_final:
        t += dt
        x, y, z, d = fsolve(equations, (x_n, y_n, z_n, d_n))
        x_n, y_n, z_n, d_n = x, y, z, d

        time.append(t)
        sick.append(y)
        healthy.append(x)
        recovered.append(z)
        deaths.append(d)

    return time, sick, healthy, recovered, deaths
