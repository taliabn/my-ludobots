import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p # type: ignore
from os.path import join


class MOTOR:

	def __init__(self, jointName):
		self.jointName = jointName


	def Prepare_to_Act(self):
		self.amplitude = c.amplitudeBackLeg
		self.frequency = c.frequencyBackLeg
		self.offset = c.phaseOffsetBackLeg
		self.motorValues = [self.amplitude * np.sin((2*np.pi*self.frequency * i/c.steps) + self.offset)
					for i in range(c.steps)]


	def Set_Value(self, robot, i):
		pyrosim.Set_Motor_For_Joint(bodyIndex = robot.robotId,
									jointName = self.jointName,
									controlMode =  p.POSITION_CONTROL,
									targetPosition = self.motorValues[i],
									maxForce = 25)		


	def Save_Values(self):
		file_path = join("data", self.jointName.decode() + "MotorValues")
		np.save(file_path, self.motorValues)							