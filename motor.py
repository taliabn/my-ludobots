import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p # type: ignore
from os.path import join


class MOTOR:

	def __init__(self, jointName):
		self.jointName = jointName


	def Set_Value(self, robot, desiredAngle):
		pyrosim.Set_Motor_For_Joint(bodyIndex = robot.robotId,
									jointName = self.jointName,
									controlMode =  p.POSITION_CONTROL,
									targetPosition = desiredAngle,
									maxForce = c.maxMotorForce)		