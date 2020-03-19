from epidemic import calculate_epidemic
from data import get_data

import scipy.optimize
from scipy import interpolate
import csv
from datetime import datetime
import matplotlib.pyplot as plt


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


def read_ref_data(country):
    time_cases_number_days = []
    time, cases, deaths = get_data(country)
    for t in time:
        time_cases_number_days.append(days_between(t, time[0]))
    return time, time_cases_number_days, \
        cases, time, time_cases_number_days, deaths


def cost_function(x):
    (a, b, c, d, e, f) = x
    v = a*10**(-b)
    K_r_0 = c*10**(-d)
    K_d_0 = e*10**(-f)
    time, sick, healthy, recovered, deaths = calculate_epidemic(
        C=0, v=v, x_n=x_n, y_n=y_n, t_final=60, K_r_0=K_r_0, K_r_minus=0,
        K_d_0=K_d_0, K_d_plus=0)
    interp_cases = interpolate.interp1d(time, sick, fill_value='extrapolate')
    interp_deaths = interpolate.interp1d(time, deaths, fill_value='extrapolate')
    fitness = 0
    N = 0
    for i in range(len(time_cases_number_days)):
        if time_cases_number_days[i] > 25:
            coeff = 1
        else:
            coeff = 1
        fitness += coeff*abs(sick_ref[i] - interp_cases(time_cases_number_days[i]))/max(sick_ref)
        N += coeff
    for i in range(len(time_deaths_number_days)):
        if time_cases_number_days[i] > 25:
            coeff = 1
        else:
            coeff = 1
        fitness += coeff*abs(deaths_ref[i] - interp_deaths(time_deaths_number_days[i]))/max(deaths_ref)
        N += coeff

    fitness /= 2*N
    print("Fit accuracy : " + str(fitness), end='\r')

    return fitness

country = "Italy"
x_n = 1e5  # initial healthy population arbitrary
time_cases, time_cases_number_days, sick_ref, time_deaths, \
    time_deaths_number_days, deaths_ref = read_ref_data(country)

y_n = sick_ref[0]
x0 = (2.78, 6.08, 25, 1.9, 1, 2)
print('Fitting...')
res = scipy.optimize.minimize(cost_function, x0, method="Nelder-Mead")
x_opt = res.x
print(x_opt)

(a, b, c, d, e, f) = x_opt
v = a*10**(-b)
K_r_0 = c*10**(-d)
K_d_0 = e*10**(-f)
time, sick, healthy, recovered, deaths = calculate_epidemic(
    C=0, v=v, x_n=x_n, y_n=y_n, t_final=60, K_r_0=K_r_0, K_r_minus=0,
    K_d_0=K_d_0, K_d_plus=0)

plt.figure()
plt.title(country)
plt.ylabel("Number of actives cases")
plt.xlabel("Days")
plt.plot(time, sick, label="Predicted cases")
plt.scatter(time_cases_number_days, sick_ref, label="Actual cases")
plt.legend()

plt.figure()
plt.title(country)
plt.xlabel("Days")
plt.ylabel("Number of deaths")
plt.plot(time, deaths, label="Predicted deaths")
plt.scatter(time_deaths_number_days, deaths_ref, label="Actual number of deaths")
plt.legend()

plt.show()
