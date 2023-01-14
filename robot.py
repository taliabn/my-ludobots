import pybullet as p # type: ignore

class ROBOT:

	def __init__(self):

		self.sensors = {}
		self.motors = {}
		self.robotId = p.loadURDF("body.urdf") # floor

		