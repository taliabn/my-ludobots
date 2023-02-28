# Description

This repo contains work for the Northwestern University course Computer Science 396: Artificial Life. 
Branches up through 'ludobots-final-project' follow the [ludobots](https://www.reddit.com/r/ludobots/) online course on Evolutionary Robotics.

# Installation

This code runs on Python 3.9.13
Dependencies are managed through an Anaconda environment.
To copy this the environment, first [install Anaconda](https://docs.anaconda.com/anaconda/install/index.html). Then, run 
```bash
conda env create --name <new environment name> --file ludobot_env.txt
```
Before running anything, make sure to first activate the environment with
```bash
conda activate <new environment name>
```
# Usage
Instructions on running the code are as follows:
Use the command 
```bash 
python search.py <seed>
``` 
to start running the simulation. 
For running multiple searches in a row, first set the list of desired seeds in line 1 of the file `run-search.sh`. Then run the command
```bash
sh search.py
```
Both error messages and console outputs will be saved in the file "out\<seed>.txt". A numpy array of fitness values as well as brain.nndf and body.urdf files for the best robots will be saved in a folder named <seed>.
To analyze a certain search by showing and saving a fitness curve (plot of best fitness value for each generation), run the command with one or more seeds
```bash
python analyze.py GUI <list of seeds>
```
To rerun a certain simulation in GUI mode, ensure the brain file is saved as "<seed>\brain<solutionID\>.nndf" and the body file is saved as "<seed>\body<solutionID\>.urdf". This will be the case if search.py is run properly. Then, run the command: 
```bash
python simulate.py GUI <solutionID> <seed>
```
Parameters such as number of generations and population size, and simulation length can be set in the file `constants.py`.

NOTE: The code has only been tested running from a Git Bash terminal on a windows machine.

# Assignment 8: random 3D morphologies
[Assignment 8](https://youtu.be/nzlCZm1mh3U), found on the [`evolve-random-body`](https://github.com/taliabn/my-ludobots/tree/evolve-random-body) branch, adds the capability to evolve both brains and bodies simultaneously.

## Evaluation
The fitness function used to select creatures after each generation of evolution is displacement of the root link in the negative x direction. A hillclimber algorithm is used, meaning that parents are compared to children, and if the child has a better fitness, it replaces the parent in the population. Figure 1 shows an example of evolution for five trials, each starting from a different random seed. [These parameters](#parameters) were used in this simulation, and can be changed in `constants.py`.

![Line graph of fitness curves](/figures/a8-fitness-curves.png )
**Figure 1. Fitness for five trials, each for 150 generations with a population of 30**

<br>

## Method to Generate Bodies
3D bodies are recursively generated using graph-based body plans, a mehod that is heavily influenced by [Karl Sims'](https://www.karlsims.com/evolved-virtual-creatures.html) work<sup>[1]</sup>.

Properties of creatures are divided into two categories, those randomly generated for each creature and those determined by "DNA" genotype that identifies a general body plan. This means that it is *not* a direct encoding between phenotypes and genotypes. See Table 1  for a summary. The body plan genotype graph encodes the number of uniqe link types, number of children for each link, and number of clones of each link (self edges). Each unique link (represented as a `UniqueNode` class in `body.py`) has its own dimensions, joint axis, orientation, and presence of sensor and corresponding color. See Figure 2 for an example of how body plans are generated.   

When running the simulation in GUI mode, links with sensors are colored green, and links without sensors are colored blue. Parameters dictating the range of link side lengths and the maximum number of links can be set in `constants.py`. 


| random | encoded |
| ------ | ------- |
| link dimensions | number of unique link types (nodes)
| sensor placement | number of clones (self edges)
| joint axis and directionality | number of new children (edges to next node)

**Table 1. Summary of random vs encoded body part properties**

![figure explaining how a numerical encoding of a body plan is transformed into a virtual creature](/figures/a7-fig1.png) 

**Figure 2. Body plan encoding to pheontype relationship**

Note that this *indirect encoding* mechanism has an important implication: a single genotype can lead to multiple phenotypes. 

To ensure that body plans follow basic laws of physics, before adding a link to the body, we check that there is no existing link in the same absolute position, preventing overlapping body parts. This means that some links specified by the genotype may not end up in the final body. To allow for freer growth in the z-direction, the creature starts at an absolute position of [0,0,1.5] and drops to the ground when the simulation starts. Additionally, we check that the absolute z position of a link isn't negative (i.e below the floor) before adding it.

##### [1] "Evolving Virtual Creatures" K.Sims, Computer Graphics (Siggraph '94 Proceedings), July 1994, pp.15-22  

### Benefits:
* Duplicated body parts create symmetry, which mimics nature
* Indirect encoding enables diversity of creatures and also mimics nature

### Drawbacks:
* linear graph structure: each unique node only connects to next unique node
* 2 children edges per node maximum
* can only branch at right angles
* symmetry can limit the potential morphospace

<br>

## Method to Generate Brains
Brains have a structure resembling that of a traditional feed forward neural network. There is one sensor neuron for each link with a sensor and one motor neuron for each link. Sensor neurons are connected to a layer of hidden neurons which are then connected to motor neurons. All synsapses start with a random weight between -1 and 1. The number of sensor and motor neurons is specific to each body plan, and `numHiddenNeurons` can be specified in `constants.py`. See Fig. 3 for an example of brain structure.

![figure illustrating structure that resembles a neural network](/figures/a7-fig2.png) 

**Figure 3. Structure of creature brains**  

<br>

## Method to Mutate Brains and Bodies
During a cycle of evolution, each individual in the population undergoes exactly *one* mutation. The process for choosing which element to mutate is detailed in Figure 4. Each branch in the flowchart is equally likely to be taken, except for the initial decision between mutating the brain or the body. This choice is weighted so that body mutations are more likely earlier in evolution and brain mutations are more likely in later generations. This balances exploring more of the morphospace with fine tuning a certain body for motion.

![flowchart that resembles a decision tree explaining possible mutations](/figures/a8-fig1.png) 
**Figure 4. Flowchart of possible mutations**

For mutating brains, it is useful to make the distinction that synapse weights are not related to the UniqueNode object that their associated links came from. However, synapse weights are preserved from generation to generation, except for the cases where a pre-existing link was removed or a new link was added. The number of links can change if the number of edges of a unique node change or if the dimensions or orientation of a link are mutated such that it will go below the floor or change which potential future links will or will not overlap with it.

It is important to note that certain types of mutations are not permitted, namely removing a unique node or adding a new unique node to a body plan. Changing the number of hidden neurons or structure of the brain is also not possible. These decisions were made because larger mutations are more likely to be harmful in the process of evolutions.

<br>

## Parallel Computing
Since evolution trials are computationally expensive and time intensive to run, this version of the code allows for parallel execution of simulations using the [`pathos`](https://pypi.org/project/pathos/) multiprocessing framework. Simulations for assignment 8 were run using 7 logical CPUs on a windows machine that has 8 total available. Previous iterations of the code ran simulations concurrently, but coordination and communication between processes used disk files as an intermediate, which was slow and caused the simulation to sometimes raise file permission errors. The new method using multiprocessing circumvents that error and explicitly instructs the simulation processes to run in parallel, which was not gauranteed in previous versions of the code. 

<br>

## Parameters
The following parameters were used in the final simulations for assignmment 8:
* `populationSize = 2`
* `numberOfGenerations = 2`
* `steps = 1000`
* `stepLength = 1/120`
* `numHiddenNeurons = 4`
* `motorJointRange = 1`
* `maxMotorForce = 30`
* `maxNumNodes = 4`
* `maxNumSelfEdges = 3`
* `maxNumChildEdges = 2`
* `minSideLen = 0.1`
* `maxSideLen = 0.75`
* `startingPos = [0, 0, 1.5]`  


# Previous Assignments

### Assignment 7: random 3D morphologies
[Assignment 7](https://youtube.com/shorts/HM3KmLzGZqs?feature=share) adds the capability to randomly generate morphologies that fill three dimensional space. See the branch [`random-3D-bodies`](https://github.com/taliabn/my-ludobots/tree/random-3D-bodies) for further details.


### Assignment 6: random 1D morphologies
[Assignment 6](https://youtu.be/uXb1K-MACNE) adds the capability to randomly generate morphologies in one dimensions. See the branch [`random-1D-bodies`](https://github.com/taliabn/my-ludobots/tree/random-1D-bodies) for further details.

### Assignment 5: Ludobots Final Project
The [Ludobots final project](https://youtu.be/qypMeX9zdyQ),  demonstrates the use of a Parallel hillclimber and an evolution through random mutations to create robots that can climb a set of stairs. See the branch [`ludobots-final-project`](https://github.com/taliabn/my-ludobots/tree/ludobots-final-project) for further details.

### Assignments 1-4:
See [ludobots](https://www.reddit.com/r/ludobots/) online course on Evolutionary Robotics for further details. Code can be found in branches up until 'ludobots-final-project'.

# Contact

Talia Ben-Naim: taliaben-naim2025@u.northwestern.edu  
[LinkedIn](www.linkedin.com/in/talia-ben-naim
)

# Acknowledgments

* [r/ludobots](https://www.reddit.com/r/ludobots/)
* [pyrosim](https://github.com/ccappelle/pyrosim)
* [pybullet](https://github.com/bulletphysics/bullet3)
* [Northwestern University Computer Science](https://www.mccormick.northwestern.edu/computer-science/)
* [Karl Sims](https://www.karlsims.com/evolved-virtual-creatures.html)
