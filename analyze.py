import numpy as np
import matplotlib.pyplot

# read and plot sensor values
backLegSensorValues = np.load("data/backLegSensorValues.npy")
frontLegSensorValues = np.load("data/frontLegSensorValues.npy")
matplotlib.pyplot.plot(backLegSensorValues, label="BackLeg", lw=3)
matplotlib.pyplot.plot(frontLegSensorValues, label="FrontLeg", lw=1)
matplotlib.pyplot.legend()
matplotlib.pyplot.show()

# read and plot targetAngles
targetAngles = np.load("data/targetAngles.npy")
matplotlib.pyplot.plot(targetAngles)
matplotlib.pyplot.show()
