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


	# runs simulation
	def Run(self):
		for i in range(c.steps):
			time.sleep(1/60)
			p.stepSimulation()
			self.robot.Sense(i)
			self.robot.Act(i)
			print(i)

		for motor in self.robot.motors.values():
			motor.Save_Values()

		for sensor in self.robot.sensors.values():
			sensor.Save_Values()


	# destructor
	def __del__(self):

		p.disconnect()	