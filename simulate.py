import random
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

# initialize arrays
backLegSensorValues = np.zeros(steps)
frontLegSensorValues = np.zeros(steps)
targetAngles = np.sin(np.linspace(0, 2*np.pi, steps))
np.save("./data/sinValues", targetAngles)
exit()

pyrosim.Prepare_To_Simulate(robotId)
# run simulation
for i in range(steps):
	time.sleep(1/60)
	# add sensors
	backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
	frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
	# add motors
	pyrosim.Set_Motor_For_Joint(bodyIndex = robotId,
								jointName = b'Torso_BackLeg',
								controlMode =  p.POSITION_CONTROL,
								targetPosition = (-np.pi/2) + random.random()*np.pi,
								maxForce = 25)
	pyrosim.Set_Motor_For_Joint(bodyIndex = robotId,
								jointName = b'Torso_FrontLeg',
								controlMode =  p.POSITION_CONTROL,
								targetPosition = (-np.pi/2) + random.random()*np.pi,
								maxForce = 25)
	p.stepSimulation()
	# print(i)
p.disconnect()
np.save("./data/backLegSensorValues", backLegSensorValues)
np.save("./data/frontLegSensorValues", frontLegSensorValues)