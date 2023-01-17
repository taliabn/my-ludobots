import pybullet as p # type: ignore


class WORLD:

	def __init__(self):

		self.planeId = p.loadURDF("plane.urdf") # floor
		p.loadSDF("world.sdf")
