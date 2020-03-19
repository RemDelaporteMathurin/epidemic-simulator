import epidemic
import scipy.optimize
from scipy import interpolate
import csv
from datetime import datetime
import matplotlib.pyplot as plt


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y/%m/%d")
    d2 = datetime.strptime(d2, "%Y/%m/%d")
    return abs((d2 - d1).days)


def read_ref_data(filename):
    time_cases, time_cases_number_days,\
        cases, time_deaths, time_deaths_number_days, deaths = [], [], [], [], [], []
    with open(filename, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        next(plots)

        i = 0
        for row in plots:
            if i == 0:
                day1_cases = row[0]
                day1_deaths = row[2]
            time_cases.append(row[0])
            time_cases_number_days.append(days_between(day1_cases, row[0]))
            cases.append(float(row[1]))
            time_deaths.append(row[2])
            time_deaths_number_days.append(days_between(day1_deaths, row[2]))
            deaths.append(float(row[3]))
            i += 1
    return time_cases, time_cases_number_days, \
        cases, time_deaths, time_deaths_number_days, deaths


def cost_function(x):
    (a, b, c, d, e, f) = x
    # (v, K_r_0, K_d_0) = x
    v = a*10**(-b)
    K_r_0 = c*10**(-d)
    K_d_0 = e*10**(-f)
    time, sick, healthy, recovered, deaths = epidemic.calculate_epidemic(
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


x_n = 1e5  # french population
y_n = 70  # number of cases on 20-01
time_cases, time_cases_number_days, sick_ref, time_deaths, \
    time_deaths_number_days, deaths_ref = read_ref_data("data/france/data_france.csv")
x0 = (2.78, 6.08, 25, 1.9, 1, 2)
print('Fitting...')
res = scipy.optimize.minimize(cost_function, x0, method="Nelder-Mead")
x_opt = res.x
print(x_opt)

(a, b, c, d, e, f) = x_opt
v = a*10**(-b)
K_r_0 = c*10**(-d)
K_d_0 = e*10**(-f)
time, sick, healthy, recovered, deaths = epidemic.calculate_epidemic(
    C=0, v=v, x_n=x_n, y_n=y_n, t_final=60, K_r_0=K_r_0, K_r_minus=0,
    K_d_0=K_d_0, K_d_plus=0)

plt.figure()
plt.title("France")
plt.ylabel("Number of actives cases")
plt.xlabel("Days")
plt.plot(time, sick, label="Predicted cases")
plt.scatter(time_cases_number_days, sick_ref, label="Actual cases")
plt.legend()

plt.figure()
plt.title("France")
plt.xlabel("Days")
plt.ylabel("Number of deaths")
plt.plot(time, deaths, label="Predicted deaths")
plt.scatter(time_deaths_number_days, deaths_ref, label="Actual number of deaths")
plt.legend()

plt.show()
