from world import WORLD
from robot import ROBOT
import pybullet_data # type: ignore
import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
import time
import constants as c


class SIMULATION:

	def __init__(self, directOrGUI, solutionID, seed):
		if directOrGUI == "DIRECT":
			self.physicsClient = p.connect(p.DIRECT)
			self.stepTime = 0
		elif directOrGUI == "GUI":
			self.physicsClient = p.connect(p.GUI)
			p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
			self.stepTime = c.stepLength
		else:
			print("ERROR: invalid run mode")
			exit()
		p.setAdditionalSearchPath(pybullet_data.getDataPath())
		p.setGravity(0,0,-9.8)
		# only writes new world for first simulation (solutionID=0)
		self.world = WORLD(initial_world = not int(solutionID)) 
		self.robot = ROBOT(directOrGUI, solutionID, seed)
		self.ID = solutionID


	# runs simulation
	def Run(self):
		# give cubes time to drop
		for i in range(50):
			time.sleep(self.stepTime)
			p.stepSimulation()
		for i in range(c.steps):
			time.sleep(self.stepTime)
			p.stepSimulation()
			self.robot.Sense(i)
			self.robot.Think()
			self.robot.Act(i)
		

	def Return_Displacement(self):
		return self.robot.Return_Displacement(self.ID)


	def Record_Displacement(self):
		self.robot.Record_Displacement(self.ID)


	# destructor
	def __del__(self):

		p.disconnect()	