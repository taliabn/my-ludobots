import random
import time
import numpy as np
import pybullet_data # type: ignore
import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
import constants as c
from simulation import SIMULATION


simulation = SIMULATION()
simulation.Run()

# # motor control angles for each leg
# targetAnglesBackLeg = [c.amplitudeBackLeg * np.sin((2*np.pi*c.frequencyBackLeg * i/c.steps) + c.phaseOffsetBackLeg)
# 					for i in range(c.steps)]
# targetAnglesFrontLeg = [c.amplitudeFrontLeg * np.sin((2*np.pi*c.frequencyFrontLeg * i/c.steps) + c.phaseOffsetFrontLeg)
# 					for i in range(c.steps)]
# # np.save("./data/targetAnglesBackLeg", targetAnglesBackLeg)
# # np.save("./data/targetAnglesFrontLeg", targetAnglesFrontLeg)
# # exit()


# p.disconnect()
# np.save("./data/backLegSensorValues", backLegSensorValues)
# np.save("./data/frontLegSensorValues", frontLegSensorValues)