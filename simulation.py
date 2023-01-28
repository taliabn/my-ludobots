from world import WORLD
from robot import ROBOT
import pybullet_data # type: ignore
import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
# from pyrosim.neuralNetwork import NEURAL_NETWORK
import time
import constants as c
# stopped after 45

class SIMULATION:

	def __init__(self, directOrGUI, solutionID):
		print(f"\ninitializing simulation with mode {directOrGUI}\n")
		if directOrGUI == "DIRECT":
			self.physicsClient = p.connect(p.DIRECT)
			self.stepTime = 0
		elif directOrGUI == "GUI":
			self.physicsClient = p.connect(p.GUI)
			self.stepTime = c.stepLength
		else:
			print("ERROR: invalid run mode")
			exit()
		p.setAdditionalSearchPath(pybullet_data.getDataPath())
		p.setGravity(0,0,-9.8)
		self.world = WORLD()
		self.robot = ROBOT(solutionID)


	# runs simulation
	def Run(self):
		for i in range(c.steps):
			time.sleep(self.stepTime)
			p.stepSimulation()
			self.robot.Sense(i)
			self.robot.Think()
			self.robot.Act(i)
			# print(i)
		
		# for sensor in self.robot.sensors.values():
		# 	sensor.Save_Values()


	# gets final position of robot
	def Get_Fitness(self, solutionID):
		self.robot.Get_Fitness(solutionID)


	# destructor
	def __del__(self):

		p.disconnect()	