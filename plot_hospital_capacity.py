from covid import *

for v in [2, 1, 0.7, 0.5, 0.3]:

    time, sick, healthy, recovered, deads = \
        calculate_covid(K_c(v), 200)
    plt.figure(1)
    plt.plot(time, sick, label="Mobility = "+str(v))
    plt.figure(2)
    plt.plot(time, deads, label="Mobility = "+str(v))
plt.figure(1)
plt.plot([0, max(time)], [y_max, y_max], color="grey", linestyle="--")
plt.xlabel("Time")
plt.ylabel("Number of sick people")
plt.text(80, y_max*(1.1), "Hostital capacity", color="grey")
plt.xticks([])
plt.yticks([])
plt.legend()
plt.figure(2)
plt.yticks([])
plt.xticks([])
plt.xlabel("Time")
plt.ylabel("Number of dead people")
plt.legend()
plt.show()
