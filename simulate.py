import pybullet as p # type: ignore
import time

physicsClient = p.connect(p.GUI)

for i in range(1000):
	time.sleep(1/60)
	p.stepSimulation()
	print(i)


p.disconnect()