from epidemic import calculate_epidemic
from data import get_data

import scipy.optimize
from scipy import interpolate
import csv
import matplotlib.pyplot as plt

import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    "country",
    help="simulate the epidemic in this country. Ex: China")
args = parser.parse_args()


def cost_function(x):
    (a, b, c, d, e, f) = x
    v = a*10**(-b)
    K_r_0 = c*10**(-d)
    K_d_0 = e*10**(-f)
    time_sim, cases_sim, healthy_sim, recovered_sim, deaths_sim \
        = calculate_epidemic(
            C=0, v=v, x_n=x_n, y_n=y_n, t_final=60, K_r_0=K_r_0, K_r_minus=0,
            K_d_0=K_d_0, K_d_plus=0)
    interp_cases = interpolate.interp1d(
        time_sim, cases_sim, fill_value='extrapolate')
    interp_deaths = interpolate.interp1d(
        time_sim, deaths_sim, fill_value='extrapolate')
    fitness = 0
    N = 0

    for i in range(len(time_number_days)):
        if time_number_days[i] > 25:
            coeff = 1
        else:
            coeff = 1
        fitness += coeff*abs(
            deaths_ref[i] - interp_deaths(time_number_days[i])) / \
            max(deaths_ref)
        fitness += coeff*abs(
            cases_ref[i] - interp_cases(time_number_days[i])) / \
            max(cases_ref)
        N += 2*coeff

    fitness /= 2*N
    print("Fit accuracy : " + str(fitness), end='\r')

    return fitness


country = args.country
x_n = 1e5  # initial healthy population arbitrary
time, time_number_days, cases_ref, deaths_ref = get_data(country)

y_n = cases_ref[0]
x0 = (2.78, 6.08, 25, 1.9, 1, 2)
print('Fitting...')
res = scipy.optimize.minimize(cost_function, x0, method="Nelder-Mead")
x_opt = res.x
print(x_opt)

(a, b, c, d, e, f) = x_opt
v = a*10**(-b)
K_r_0 = c*10**(-d)
K_d_0 = e*10**(-f)
time_sim, cases_sim, healthy_sim, recovered_sim, deaths_sim \
    = calculate_epidemic(
        C=0, v=v, x_n=x_n, y_n=y_n, t_final=60, K_r_0=K_r_0, K_r_minus=0,
        K_d_0=K_d_0, K_d_plus=0)

plt.figure()
plt.title(country)
plt.ylabel("Number of actives cases")
plt.xlabel("Days")
plt.plot(time_sim, cases_sim, label="Predicted cases")
plt.scatter(time_number_days, cases_ref, label="Actual cases")
plt.legend()

plt.figure()
plt.title(country)
plt.xlabel("Days")
plt.ylabel("Number of deaths")
plt.plot(time_sim, deaths_sim, label="Predicted deaths")
plt.scatter(time_number_days, deaths_ref, label="Actual number of deaths")
plt.legend()

plt.show()
