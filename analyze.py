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
targetAnglesBackLeg = np.load("data/targetAnglesBackLeg.npy")
targetAnglesFrontLeg = np.load("data/targetAnglesFrontLeg.npy")
matplotlib.pyplot.plot(targetAnglesBackLeg, label="BackLeg Target Angles", lw=3)
matplotlib.pyplot.plot(targetAnglesFrontLeg, label="FrontLeg Target Angles", lw=1)
matplotlib.pyplot.legend()
matplotlib.pyplot.show()

