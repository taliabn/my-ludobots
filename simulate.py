import time
import numpy as np
import pybullet_data # type: ignore
import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim

# number of times to step through simulation
steps = 1000

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf") # floor
robotId = p.loadURDF("body.urdf") # floor
p.loadSDF("world.sdf")

backLegSensorValues = np.zeros(steps)
frontLegSensorValues = np.zeros(steps)

pyrosim.Prepare_To_Simulate(robotId)
# run simulation
for i in range(steps):
	time.sleep(1/60)
	backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
	frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
	pyrosim.Set_Motor_For_Joint(bodyIndex = robotId,
								jointName = b'Torso_BackLeg',
								controlMode =  p.POSITION_CONTROL,
								targetPosition = 0.0,
								maxForce = 500)
	p.stepSimulation()
	# print(i)
p.disconnect()
np.save("./data/backLegSensorValues", backLegSensorValues)
np.save("./data/frontLegSensorValues", frontLegSensorValues)