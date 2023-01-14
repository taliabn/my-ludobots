import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
import pybullet_data # type: ignore

class WORLD:

	def __init__(self):

		# self.physicsClient = p.connect(p.GUI)
		# p.setAdditionalSearchPath(pybullet_data.getDataPath())
		self.planeId = p.loadURDF("plane.urdf") # floor
		p.loadSDF("world.sdf")
