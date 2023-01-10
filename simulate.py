import time
import numpy as np
import pybullet_data # type: ignore
import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim


physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf") # floor
robotId = p.loadURDF("body.urdf") # floor
p.loadSDF("world.sdf")

backLegSensorValues = np.zeros(10000)
print(backLegSensorValues)

pyrosim.Prepare_To_Simulate(robotId)
# run simulation
for i in range(1000):
	time.sleep(1/60)
	backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
	p.stepSimulation()
	# print(i)
p.disconnect()
np.save("./data/backLegSensorValues", backLegSensorValues)