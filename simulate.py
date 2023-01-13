import random
import time
import numpy as np
import pybullet_data # type: ignore
import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
import constants as c
from simulation import SIMULATION


simulation = SIMULATION()

# physicsClient = p.connect(p.GUI)
# p.setAdditionalSearchPath(pybullet_data.getDataPath())
# p.setGravity(0,0,-9.8)
# planeId = p.loadURDF("plane.urdf") # floor
# robotId = p.loadURDF("body.urdf") # floor
# p.loadSDF("world.sdf")

# # initialize arrays
# backLegSensorValues = np.zeros(c.steps)
# frontLegSensorValues = np.zeros(c.steps)

# # motor control angles for each leg
# targetAnglesBackLeg = [c.amplitudeBackLeg * np.sin((2*np.pi*c.frequencyBackLeg * i/c.steps) + c.phaseOffsetBackLeg)
# 					for i in range(c.steps)]
# targetAnglesFrontLeg = [c.amplitudeFrontLeg * np.sin((2*np.pi*c.frequencyFrontLeg * i/c.steps) + c.phaseOffsetFrontLeg)
# 					for i in range(c.steps)]
# # np.save("./data/targetAnglesBackLeg", targetAnglesBackLeg)
# # np.save("./data/targetAnglesFrontLeg", targetAnglesFrontLeg)
# # exit()

# pyrosim.Prepare_To_Simulate(robotId)
# # run simulation
# for i in range(c.steps):
# 	time.sleep(1/60)
# 	# add sensors
# 	backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
# 	frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
# 	# add motors
# 	pyrosim.Set_Motor_For_Joint(bodyIndex = robotId,
# 								jointName = b'Torso_BackLeg',
# 								controlMode =  p.POSITION_CONTROL,
# 								targetPosition = targetAnglesBackLeg[i],
# 								maxForce = 25)
# 	pyrosim.Set_Motor_For_Joint(bodyIndex = robotId,
# 								jointName = b'Torso_FrontLeg',
# 								controlMode =  p.POSITION_CONTROL,
# 								targetPosition = targetAnglesFrontLeg[i],
# 								maxForce = 25)
# 	p.stepSimulation()
# 	# print(i)
# p.disconnect()
# np.save("./data/backLegSensorValues", backLegSensorValues)
# np.save("./data/frontLegSensorValues", frontLegSensorValues)