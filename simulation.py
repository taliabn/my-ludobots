from world import WORLD
from robot import ROBOT
import pybullet_data # type: ignore
import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim

class SIMULATION:

	def __init__(self):

		self.physicsClient = p.connect(p.GUI)
		p.setAdditionalSearchPath(pybullet_data.getDataPath())
		p.setGravity(0,0,-9.8)
		self.world = WORLD()
		self.robot = ROBOT()

		pyrosim.Prepare_To_Simulate(self.robot.robotId)
