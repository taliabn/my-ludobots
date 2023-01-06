import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")
length, height, width = 1, 1, 1 # box dimensions
x, y, z = 0, 0, 0.5 # box starting position
for i in range(5):	
	for j in range(5):
		for k in range(10):
			pyrosim.Send_Cube(name="Box", pos=[x + i, y + j, z + k] , 
					  		  size=[length*(0.9**k), height*(0.9**k), width*(0.9**k)])
pyrosim.End()