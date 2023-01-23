import numpy as np
import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
import constants as c
from simulation import SIMULATION


simulation = SIMULATION()
simulation.Run()
simulation.Get_Fitness()
