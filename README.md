# Description

This repo contains work for the Northwestern University course Computer Science 396: Artificial Life. 
Branches up through 'ludobots-final-project' follow the [ludobots](https://www.reddit.com/r/ludobots/) online course on Evolutionary Robotics.

# Installation

This code runs on Python 3.9.13
Dependencies are managed through an Anaconda environment.
To copy this the environment, first [install Anaconda](https://docs.anaconda.com/anaconda/install/index.html). Then, run 
```bash
conda env create --name <new environment name> --file ludobot_env.yml
```
Before running anything, make sure to first activate the environment with
```bash
conda activate <new environment name>
```
# Usage
Instructions on running the code are as follows:
Use the command 
```bash 
python search.py <seed> <number of hidden layers>
``` 
To start running the simulation. Number of [hidden layers](!!!!!LINK TO FIGURE!!!!!!!!!) should be 0, 1, or 2.  
A numpy array of fitness values as well as brain.nndf and body.urdf files for the final robots will be saved in the folder "./seed".  
Simulations can be also resumed using the same command. Make sure that the number of hidden layers is the same as what was used for the original simulation.

<br>

To analyze a certain search by showing and saving a fitness curve (plot of best fitness value at each generation), run the following command with one or more seeds
```bash
python analyze.py GUI <list of seeds>
```
To rerun a certain simulation in GUI mode, ensure the brain file is saved as "<seed>\brain<solutionID\>.nndf" and the body file is saved as "<seed>\body<solutionID\>.urdf". This will be the case if search.py is run properly. Then, run the command: 
```bash
python simulate.py GUI <solutionID> <seed>
```
Parameters such as number of generations and population size, and simulation length can be set in the file `constants.py`.

NOTE: The code has only been tested running from a Git Bash terminal on a Windows machine.

# Final project
The [final project](https://youtu.be/uux9ZBXE7Lc) uses this codebase to compare brain architectures of robots evolved for locomotion.
![simple simulated robots moving to the left](/figures/10s-highlights.gif) 


## **Hypothesis**
At a high level, robots move using hinge joints with motors that rotate the links (cube-shaped rigid body parts) they are attached to towards a desired angle. This target angle is informed by data from sensors that detect whether or not the link it is attached to is currently making contact with the floor. The robot's "brain" plays the role of mapping these sensor values to target motor angles.

A brain is comprised of neurons and synapses. A neuron is a node that is associated with a certain sensor or motor. Synapses connect these neurons, and they indicate how much to scale the value from the incoming pre-synaptic neuron. A motor neuron's value is the sum of all its incoming synapses. A sensor neuron's value is the value of the sensor.

To potentially allow for more complex pattern recognition, brains can also contain hidden neurons, which means that sensor neurons are not diretly wired to motor neurons.  A hiden neuron's value is the sum of all its incoming synapses.

This project tests the hypothesis that having different numbers of hidden layers of neurons will make a difference on a final evolved robot's ability to move in the x-direction. 

The three brain architectures tested are illustrated in figure 1. For the simulations, actual robot brains had 4 hidden neurons in each layer, if present. The number of sensor neurons and motor neurons depended on the specific robot's body.

![figure illustrating brain architectures that resemble neural networks](/figures/hidden-layers.png) 

#### **Figure 1.** Possible structures of creature brains

<br>

## **Methods**
This hypothesis was tested using evolution simulations for each of the three possible brain architectures.
Each of the three experimental groups had 10 trials of simulated evolution, and each trial started from a specific random seed for reproducability purposes. Each evolution simulation used an initial population of 21 parents and ran for 500 generations.  

<br>

## Evolution Process
Both robot brains and bodies are initially randomly generated, and are then iteratively improved on using a *parallel hillclimber* evolutionary algorithm. The general process, which is summarized in Figure 2, starts by generating a random population of parents. Then, for each generation of evolution, children are spawned by copying and mutating parents and children are evaluated through simulation. Next, if a child performs better than its' parent, the child replaces the parent in the population.


![flowchart of evolution using hillclimber algorithm](/figures/evolution-flowchart.png) 
Figure 2. Evolution Process


The fitness function used to select creatures after each generation of evolution is total displacement of the root link (starting body part) in the negative x direction. 

### Fitness Function Flaws
One issue with this fitness function is that sometimes tall creatures that fall over in the x direction are favored. To mitigate this risk, starting position of the root was lowered from [0,0,3] to [0,0,1.5]. This reduced the chance of winning creatures being those that fall, but has the disadvantage of limitting the potential morphospace by allowing for fewer links to grow in the z direction.  

Number of body lengths traveled in the x direction was also tested as a fitness function, but this led to evolution focusing more on making creatures very skinny rather than optimizing for locomotion.

Finally, after starting to move, some creatures ended up bouncing off the floor in a way that sent them flying. Such robots were excluded in the final analysis.  

<br>

## Generating Bodies
3D bodies are recursively generated using graph-based body plans, a method that is heavily influenced by [Karl Sims'](https://www.karlsims.com/evolved-virtual-creatures.html) work<sup>[[1]](#1-evolving-virtual-creatures-ksims-computer-graphics-siggraph-94-proceedings-july-1994-pp15-22)</sup>.

Properties of creatures are divided into two categories, those randomly generated for each creature and those determined by "DNA" genotype that identifies a general body plan. This means that it is *not* a direct encoding between phenotypes and genotypes. See Table 1  for a summary. The body plan genotype graph encodes the number of uniqe link types, number of children for each link, and number of clones of each link (self edges). Each unique link (represented as a `UniqueNode` class in `body.py`) has its own dimensions, joint axis, orientation, and presence of sensor and corresponding color. See Figure 3 for an example of how body plans are generated.   

When running the simulation in GUI mode, links with sensors are colored green, and links without sensors are colored blue. Parameters dictating the range of link side lengths and the maximum number of links can be set in `constants.py`. 


| Random | Encoded |
| ------ | ------- |
| link dimensions | number of unique link types (nodes)
| sensor placement | number of clones (self edges)
| joint axis and directionality | number of new children (edges to next node)

#### **Table 1.** Summary of random vs encoded body part properties

![figure explaining how a numerical encoding of a body plan is transformed into a virtual creature](/figures/a7-fig1.png)   

<br>

#### **Figure 3.** Body plan encoding to pheontype relationship  



Note that this *indirect encoding* mechanism has an important implication: a single genotype can lead to multiple phenotypes. 

To ensure that body plans follow basic laws of physics, before adding a link to the body, we check that there is no existing link in the same absolute position, preventing overlapping body parts. This means that some links specified by the genotype may not end up in the final body. To allow for freer growth in the z-direction, the creature starts at an absolute position of [0,0,1.5] and drops to the ground when the simulation starts. Additionally, the code checks that the absolute z position of a link isn't negative (i.e below the floor) before adding it.


#### Benefits:
* Duplicated body parts create symmetry, which mimics nature
* Indirect encoding enables diversity of creatures and also mimics nature

#### Drawbacks:
* Linear graph structure: each unique node only connects to next unique node
* 2 outgoing child edges per node maximum
* Can only branch at right angles
* Symmetry can limit the potential morphospace  


<br>

##### [1] "Evolving Virtual Creatures" K.Sims, Computer Graphics (Siggraph '94 Proceedings), July 1994, pp.15-22.  
<br>

## Generating Brains
Brains have a structure resembling that of a traditional feed forward neural network, see [Figure 1](#figure-1-possible-structures-of-creature-brains) for details. All synsapses start with a random weight between -1 and 1, inclusive. The number of sensor and motor neurons is specific to each body plan, and `numHiddenNeurons` can be specified in `constants.py`. Simulations for the final project tested usig 0, 1, and 2 layers of hidden neurons. Code differentiating these trials is in the `Gen_*_Hidden_Brain_nndf` and `Mutate_*_Hidden_Brain()` functions in `body.py`.


## Mutating Brains and Bodies
During a cycle of evolution, each individual in the population undergoes exactly *one* mutation. The process for choosing which element to mutate is detailed in Figure 4. Each branch in the flowchart is equally likely to be taken, except for the initial decision between mutating the brain or the body. This choice is weighted so that body mutations are more likely earlier in evolution and brain mutations are more likely in later generations. This balances exploring more of the morphospace with fine tuning a certain body for motion.

![flowchart that resembles a decision tree explaining possible mutations](/figures/a8-fig1.png) 
#### **Figure 4. Flowchart of possible mutations**

<br>

For mutating brains, it is important to make the distinction that synapse weights are not related to the UniqueNode object that their associated links were generated from. However, synapse weights are preserved from generation to generation, except for the cases where a pre-existing link was removed or a new link was added. The number of links can change if the number of edges of a unique node change or if the dimensions or orientation of a link are mutated such that it will go below the floor or change which potential future links will or will not overlap with it.

It is also important to note that certain types of mutations are not permitted, namely removing a unique node or adding a new unique node to a body plan. Changing the number of hidden neurons or structure of the brain is also not possible. These decisions were made because larger mutations are more likely to be harmful in the process of evolutions.

<br>

## Simulation Scale and Parallel Computing
Simulations for the final project were run in parallel using 7 logical CPUs on a Windows machine that has 8 total available. The choice to use a population size of 21 was purposefully made so that each CPU had an equal number of tasks to run, meaning that processors were not left idle. This led to significant speedup on average *per simulation* as compared to a population size of 30, which was used in previous assignments.

The final project used a total of 315,000 simulations (3 experimental groups * 10 random seeds * 21 parents * 500 generations). This took just over **23 hours** to run, meaning an average of 46 minutes per trial (one random seed and one experimental group). 

This was made possible by parallel execution of simulations using the [`pathos`](https://pypi.org/project/pathos/) multiprocessing framework. Previous iterations of the code ran simulations concurrently, but coordination and communication between processes used disk files as an intermediate, which was slow and caused the simulation to sometimes raise file permission errors. The new method using multiprocessing circumvents that error and explicitly instructs the simulation processes to run in parallel, which was not gauranteed in previous versions of the code. Usage of the multiprocessing framework led to significant performance improvements. It was not possible to measure performance of the previous non-parallel version of the code since it crashed for large population sizes and number of generations, so the speedup is not quantifiable.

<br>

## Parameters
The following parameters were used in the final simulations:
* `populationSize = 21`
* `numberOfGenerations = 500`
* `steps = 750`
* `stepLength = 1/120`
* `numHiddenNeurons = 4`
* `motorJointRange = 1`
* `maxMotorForce = 20`
* `maxNumNodes = 4`
* `maxNumSelfEdges = 2`
* `maxNumChildEdges = 2`
* `minSideLen = 0.1`
* `maxSideLen = 0.75`
* `startingPos = [0, 0, 1.5]`  

These values can be changed in the file `constants.py`

<br>

## **Results**
For each experimental group, plots with the fitnesses for the best individual in the population at each generation can be found in Figures 5-7. Note that some creatures had invalid forms of motion such as bouncing off the floor and flying into the air. These were excluded in the final analysis.

![fitness curves for robots with brains with 0 hidden layers](/figures/NH-0-valid-500gen-fitnessPlot.png)
#### **Figure 5.** Fitness curves for brains with 0 hidden layers

![fitness curves for robots with brains with 1 hidden layer](/figures/NH-1-valid-500gen-fitnessPlot.png)
#### **Figure 6.** Fitness curves for brains with 1 hidden layer

![fitness curves for robots with brains with 2 hidden layers](/figures/NH-2-valid-500gen-fitnessPlot.png)
#### **Figure 7.** Fitness curves for brains with 2 hidden layers      

<br>

Fitness increases asymptotically over time, which is typical for evolutionary algorithms and neural networks.   

<br>

To directly compare the effects of number of hidden layers, fitness curves from the best 5 seeds for each experimental group are plotted together in Figure 7.   

![fitness curves for robots with brains with 2 hidden layers](/figures/NH-comp-5-valid-500gen-fitnessPlot.png)
#### **Figure 7.** Effects of number of hidden layers on fitness  

<br>  

Data and body/brain files from these simulations can be found in the folder "data-final-project". These files can be used to rerun a certain simulation in GUI mode or to continue evolution. To continue evolution, first increase `numberOfGenerations` in constants.py.  


<br>

## Analysis
From looking at the plots, it is unclear which brain architecture is better. Code used to perform further statistical analysis can be foundd in the file `stats.R`, which operates on numbers scraped using `clean.py`. The statistics investigated the final fitnesses for each individual in the population. Specifically, for each seed, the test statistics were median fitness, the best indivividual, and the mean of the best 5 individuals. Each of the three statistics was used seperately to compare each of the three experimental groups to each other using hypothesis tests.

Using a standard t-test, *no significant difference* was found between the best or median final fitnesses and the number of hidden layers in a robot's brain. The same conclusions can be made using the Wilcoxon rank sum test.

The only exception was if a confidence level of 10% was used, when looking at the best 5 final fitnesses, there was weak evidence (p-value = 0.076) to suggest that 0 hidden layers had lower fitness than 2 hidden layers. Again, the wilcox test led to the same conclusion (p-value = 0.090). 

Final fitnesses for the best 5 individuals from each seed are compared in Figure 7.
![boxplot comparing best fitnesses from the three experimental groups](/figures/best5-boxplot.png)
#### **Figure 7.** Distributions of best 5 individuals from each seed

<br>

## Conclusions
There is little statistically significant evidence to suggest that the number of hidden layers has an impact on the best final evolved robot's capabilities for locomotion. A possible explanation is that the amount of randomness in the generated robot's bodies and the evolution process shadows any possible trends in effects of brain architecture.


Outside of number of hidden layers, in these simulations there were several common features found in the **bodies** of the most successful evolved creatures. In general, many of the best creatures had some (not all) of the following traits:
* Sensors on links touching the ground (green cubes)
* No sprawling body plans, relatively compact
* Bilateral symmetry
* Galloping-like motion
* Non-sensing base on top of single row of identical "legs"
* "Tails" helping the creature balance and lean in the correct direction

Note that many of the best body plans appear to primarily grow along one axis, but the morphospace allows for more diverse structures. See the section on [Generating Bodies](#generating-bodies) for details.

<br>

## Next Steps
Future work can test the same hypothesis with additionaly simulations by increasing the population size, number of generations, and number of trials.

Other interesting hypotheses might relate to the evolutionary algorithm used or the method the robots are replicated and mutated. For instance, future experiments could investifate sexual reproduction where parent's body plans and brains are combined with crossover and then mutated.  
Also the data is somewhere!!!!!!!!!!!!!!!!!!!!!!!!!!!
<br>

# Previous Assignments

### Assignment 8: Evolving bodies
[Assignment 8](https://youtu.be/nzlCZm1mh3U) adds the capability to evolve brains and bodies simultaneously. See the branch [`evolve-random-bodies`](https://github.com/taliabn/my-ludobots/tree/evolve-random-body) for further details.  


### Assignment 7: Random 3D morphologies
[Assignment 7](https://youtube.com/shorts/HM3KmLzGZqs?feature=share) adds the capability to randomly generate morphologies that fill three dimensional space. See the branch [`random-3D-bodies`](https://github.com/taliabn/my-ludobots/tree/random-3D-bodies) for further details.


### Assignment 6: Random 1D morphologies
[Assignment 6](https://youtu.be/uXb1K-MACNE) adds the capability to randomly generate morphologies in one dimensions. See the branch [`random-1D-bodies`](https://github.com/taliabn/my-ludobots/tree/random-1D-bodies) for further details.  


### Assignment 5: Ludobots Final Project
The [Ludobots final project](https://youtu.be/qypMeX9zdyQ),  demonstrates the use of a Parallel hillclimber and an evolution through random mutations to create robots that can climb a set of stairs. See the branch [`ludobots-final-project`](https://github.com/taliabn/my-ludobots/tree/ludobots-final-project) for further details.  


### Assignments 1-4:
See [ludobots](https://www.reddit.com/r/ludobots/) online course on Evolutionary Robotics for further details. Code can be found in branches up until 'ludobots-final-project'.

<br>

# Contact

Talia Ben-Naim: taliaben-naim2025@u.northwestern.edu  
[LinkedIn](www.linkedin.com/in/talia-ben-naim
)

<br>

# Acknowledgments

* [r/ludobots](https://www.reddit.com/r/ludobots/)
* [pyrosim](https://github.com/ccappelle/pyrosim)
* [pybullet](https://github.com/bulletphysics/bullet3)
* [Northwestern University Computer Science](https://www.mccormick.northwestern.edu/computer-science/)
* [Karl Sims](https://www.karlsims.com/evolved-virtual-creatures.html)
