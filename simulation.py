from world import WORLD
from robot import ROBOT
import pybullet_data # type: ignore
import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
import time
import constants as c

class SIMULATION:

	def __init__(self):

		self.physicsClient = p.connect(p.GUI)
		p.setAdditionalSearchPath(pybullet_data.getDataPath())
		p.setGravity(0,0,-9.8)
		self.world = WORLD()
		self.robot = ROBOT()

		pyrosim.Prepare_To_Simulate(self.robot.robotId)

	# runs simulation
	def Run():
		for i in range(c.steps):
			time.sleep(1/60)
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
			p.stepSimulation()
			print(i)