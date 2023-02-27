import numpy as np
import matplotlib.pyplot
import sys


seed = sys.argv[1]
fitnessValues = np.load(f"./{seed}/fitnessValues.npy")
print(fitnessValues)
matplotlib.pyplot.plot(fitnessValues*-1, label=seed, lw=3)
matplotlib.pyplot.legend()
matplotlib.pyplot.savefig(f"./{seed}/fitnessPlot.jpg")
matplotlib.pyplot.show()