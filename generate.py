import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")
length, height, width = 1, 1, 1 # box dimensions
x, y, z = 0, 0, 0.5 # box starting position
for i in range(10):
	pyrosim.Send_Cube(name="Box", pos=[x, y, z + i*10] , 
					  size=[length*(0.9**i), height*(0.9**i), width*(0.9**i)])
pyrosim.End()