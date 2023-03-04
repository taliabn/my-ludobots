import numpy as np
import matplotlib.pyplot as plt
import sys
import constants as c

fig, ax = plt.subplots()
for seed in sys.argv[1:]:
	fitnessValues = np.load(f"./{seed}/fitnessValues.npy")
	ax.plot(np.min(fitnessValues, axis=1)*-1, label=seed, lw=2)
ax.set_title(f"Best fitness over time \n(population size = {c.populationSize})")
ax.set_xlabel("Generation")
ax.set_ylabel(f"Fitness \n(displacement along x axis)")
plt.legend(title='seed', loc='lower right')
plt.margins(x=0)
# plt.savefig(f"./fitnessPlot.png")
plt.show()