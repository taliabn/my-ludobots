import random
# number of evolutions
populationSize = 500
numberOfGenerations = 25
# number of times to step through simulation
steps = 1500
# length of each time-step in seconds
stepLength = 1/120
# nn properties
numHiddenNeurons = 4
# motor properties
motorJointRange = 1
maxMotorForce = 50
# pyramid dimensions
gap_width = 1.75
pyramid_x = -7.75
num_pyramid_layers = 10
pyramid_length = 15
layer_height = 0.1
# random body plan ranges
maxNumNodes = 4
maxNumSelfEdges = 3
maxNumChildEdges = 2
minSideLen = 0.1
maxSideLen = .75
startingPos = [0, 0, 1.5]

# seed = 876
seed = random.randint(0,1000)