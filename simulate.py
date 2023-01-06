import time
import pybullet_data # type: ignore
import pybullet as p # type: ignore


physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf") # floor
p.loadSDF("world.sdf")

# run simulation
for i in range(1000):
	time.sleep(1/60)
	p.stepSimulation()
	print(i)

p.disconnect()