## Description

This repo contains work for the Northwestern University course Computer Science 396: Artificial Life. 
Branches up until and including 'ludobots-final-project' follow the [ludobots](https://www.reddit.com/r/ludobots/) online course on Evolutionary Robotics

## Installation

This code runs on Python 3.11.0.
Dependencies are managed through an Anaconda environment.
To copy this the environment, first install Anaconda. Then, run 
```bash
conda env create --name <new environment name> --file ludobot_env.txt
```
Before running anything, make sure to first activate the environment with
```bash
conda activate <new environment name>
```

Use the command 
```bash 
python search.py
``` 
to start running the simulation. 
To rerun a certain simulation, ensure the brain file is saved as "brain\<solutionID\>.nndf. 
Then run the command 
```bash
python simulate.py GUI <solutionID>
```
Parameters such as number of generations and population size, and simulation length can be set in the file `constants.py`.

NOTE: certain lines use `os.system()` calls, which are operating system specific.
The code is currently written for a windows machine using a bash terminal. 
See [r/ludobots: parallelhillclimber](https://www.reddit.com/r/ludobots/wiki/parallelhc/) for details on how to change this.


## Ludobots Final Project
The [final project](https://youtu.be/qypMeX9zdyQ), found on the 'ludobots-final-project' branch, demonstrates the use of a Parallel hillclimber and an evolution through random mutations to create robots that can climb a set of stairs.
The fitness function used to evaluate the robots is total euclidean distance from the top of the pyramid to the final position of the robot's root link (torso).
The goal is to minimize fitness, where 0 is the best possible fitness.
Brains also feature a layer of hidden neurons.


## Contact

Talia Ben-Naim - taliaben-naim2025@u.northwestern.edu

## Acknowledgments

* [r/ludobots](https://www.reddit.com/r/ludobots/)
* [pyrosim](https://github.com/ccappelle/pyrosim)
