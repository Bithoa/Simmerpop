# Simmerpop
Simulation of Emergent Populations


## Description
Simmerpop is a repository of code for conducting virtual life simulations. It was developed with a focus on simmulating early life ecosystems to further our understanding of the origin of life. 


## Usage

The Simmerpop repository is freely available on GitHub at:  
https://github.com/GoldmanLab/Simmerpop/

### Instalation and execution
To run the simulation, download the entire code repository to the desired location on your machine. 

Then run the python 3 script from the Simmerpop root directory. 
If you do not have python 3 installed on your machine, it is available [here](https://www.python.org/downloads/).

##### Mac
Open the Terminal app (found in Applications -> Utilities) and navigate to the Simmerpop folder from the command line
Tip: you can simply type cd, then drag and drop the folder from the finder window
```
cd /filepath_example/Simmerpop
```
Now execute the run_simmerpop.py script
```
python3 run_simmerpop.py
```
Additional arguments can be provided to change the simulation's behavior. See [User definable arguments](#user-definable-arguments).  
Example:
```
python3 run_simmerpop.py KEY value
```

##### Linux
Open the terminal program. In KDE, open the main menu and select "Run Command..." to open Konsole. In GNOME, open the main menu, open the Applications folder, open the Accessories folder, and select Terminal. Navigate to the Simmerpop folder from the command line
```
cd /filepath_example/Simmerpop
```
Make sure the run_simmerpop.py script is executable
```
chmod +x run_simmerpop.py
```
Now execute the run_simmerpop.py script
```
python3 run_simmerpop.py
```
Additional arguments can be provided to change the simulation's behavior. See [User definable arguments](#user-definable-arguments).  
Example:
```
python3 run_simmerpop.py KEY value
```

##### Windows
Open the Windows terminal by going to the Start menu and selecting "Run...", then type ```cmd```. Now navigate to the Simmerpop folder from the command line
```
cd \example_filepath\Simmerpop
```
Now execute the run_simmerpop.py script
```
run_simmerpop.py
```
If that doesn't work make sure your PATH contains the python dictionary. See [how to get python](https://en.wikibooks.org/wiki/Python_Programming/Getting_Python).

Additional arguments can be provided to change the simulation's behavior. See [User definable arguments](#user-definable-arguments).  
Example:
```
run_simmerpop.py KEY value
```


### User definable arguments
User definable arguments can be added as arguments when running run_simmerpop.py from the command line. Each argument comes as a `KEY` `value` pair. Any number of these pairs can be given as arguments in any order. 
+ Most `KEY`s simply change a simulation constant (such as the starting population size) to the given `value` overriding the default value. 
+ Some `KEY`s change the simulation's behavior, following a ruleset denoted by the given `value`. 
+ Some `KEYS`s are used to indicate a different user definable script by giving its name as the `value`. This allows users to program their own versions of specific modules to behave in new ways, without overwriting existing modules. 

`KEY` `value` pairs are listed below organized by which scripts they modify. They are given in the format:

`KEY` `default_value` *(data_type)*\
Description: where KEY is the keyword to use, default_value is the value used by the model when it is not especified here, and data_type is the type of data, either and integer, float, boolean, or string.


##### Simmerpop scripts
(common to all Simmerpop runs)

**global_variables.py**  

`MUTATION_INTERVAL` `100` *(int)*\
set how frequently mutation actions are performed

`ENERGY_IO` `cellulator_energy_io` *(string)*\
select what energy IO script to use

`FOOD_IO` `cellulator_food_io` *(string)*\
select what food IO script to use

`GENOME_MANAGER` `cellulator_genome_manager` *(string)*\
select what genome manager script to use


**population_manager.py**

`POPULATION_CAP` `10000` *(int)*\
the maximum population

`START_POPULATION` `10000` *(int)*\
the starting population number


**end_conditions.py**
`MAX_NUM_STEPS` `100000` *(int)*\
the maximum number of steps to run

`MAX_RUN_TIME` `6000` *(int)*\
the maximum runtime in minutes


**analytics.py**

`OUTPUT_FOLDER_NAME` `default_folder_name` *(string)*\
a folder name for the results folder


**organism.py**

`METABOLIC_QUALITY_CHECK_COUNT` `1000` *(int)*\
the number of replicate sample foods to solve when calculating the genome quality

`ENERGY_FACTOR` `2.0` *(float)*\
the starting energy of organisms is the genome length * the ENERGY_FACTOR

##### Example scripts
(templates for writing your own scripts, won't actually do anything if used)

**custom_genome_manager_template.py**

`KEY_FOR_EXAMPLE_MUTATION_PROB` `0.001` *(float)*\
template example for implementing key value pairs

**custom_energy_io_template.py**

`EXAMPLE_VARIABLE` `0.1` *(float)*\
an example

**custom_food_io_template.py**

`EXAMPLE_VARIABLE` `0.1` *(float)*\
an example


##### Cellulator scripts
(scripts belonging to the "Cellulator" build of Simmerpop)

**cellulator_genome_manager.py**

`LOOSE_GENE_POOL_CAP` `1000` *(int)*\
max number of loose genome fragments

`MUTATION_PROB` `0.005` *(float)*\
the probability of a mutation occuring

`POINTER_MUT_PROB` `MUTATION_PROB` *(float)*\
probability of a gene pointer mutating

`DELETION_PROB` `MUTATION_PROB` *(float)*\
probability of a gene being deleted

`INSERTION_PROB` `MUTATION_PROB` *(float)*\
probability of any gene type being inserted between each gene

`INS_GET_WT` `10` *(int)*\
`INS_PUT_WT` `10` *(int)*\
`INS_NAND_WT` `30` *(int)*\
`INS_CELL_WT` `5` *(int)*\
the relative proportion of *GeneGet*, *GenePut*, *GeneNAND*, and *GeneCellularity* genes being inserted such that the probability of a *GeneGet* insertion mutation is\
INS_GET_WT * INSERTION_PROB / (INS_GET_WT + INS_PUT_WT + INS_NAND_WT + INS_CELL_WT)\
and so on. 

`GENOME_BREAK_PROB` `0.1` *(float)*\
probability of a genome fragmenting after each gene

`NUM_CELLGENES` `0` *(int)*\
initial number of cellularity genes in the starting genome

`HGT_PROB` `0.5` *(float)*\
probability of horizontal gene transfer


**cellulator_energy_io.py**

`ENERGY_LIMIT` `0` *(int)*\
a flag indicating the behavior of the energy IO.
+ 0 = regular addition of energy and no energy pool cap
+ 1 = a single burst of energy at the start and an energy pool size limited to the ENERGY_CAP_PROPORTION * POPULATION_CAP
+ 2 = a single burst of energy at the start and no energy pool cap

`ENERGY_CAP_PROPORTION` `0.25` *(float)*\
multiplied by the POPULATION_CAP to determine the energy pool cap limit if the ENERGY_LIMIT flag is set to 1

`NEW_ENERGY_PARCEL_SIZE` `500` *(int)*\
the amount of energy in newly added energy parcels 


**food_type_not.py**

`FOODNOT_BASE_PAYOFF_EXPONENT` `3` *(int)*\
`FOODNOT_PAYOFF_ADJUSTMENT_FACTOR` `0.1` *(float)*\
`FOODNOT_REDUCE_PAYOFF_WHEN_OVER` `1.0` *(float)*\
`FOODNOT_INCREASE_PAYOFF_WHEN_UNDER` `0.5` *(float)*\
variables that define the energy reward of food such that n^x-a*A where 
+ n = the number of digits correctly solved in the food puzzle
+ x = FOODNOT_BASE_PAYOFF_EXPONENT
+ a = FOODNOT_PAYOFF_ADJUSTMENT_FACTOR
+ A = the adjustment amount
  + the adjustment amount A increments by 1 per step if the current population size is over FOODNOT_REDUCE_PAYOFF_WHEN_OVER * POPULATION_CAP
  + the adjustment amount A decrements by 1 per step if the current population size is under FOODNOT_INCREASE_PAYOFF_WHEN_UNDER * POPULATION_CAP

### Customizing scripts
Three major scripts are designed to be easily interchanged with user created versions. 
+ The genome manager script defines the behavior of and manages organism's genomes  
+ The energy in/out script defines the behavior of and manages energy  
+ The food in/out script defines the behavior of and manages food  

Each of these has a corresponding folder containing a class definition file (ex. cd_genome_manager.py) and a template (ex. custom_genome_manager_template.py). To implement a custom version of one of these scripts, make a duplicate of the desired template, then rename it to your liking. The general structure for the scripts and their required methods are already implemented in the template.  
To use your new script, give the script's name as a command line argument when running the script. For example, if you create your own genome manager script named my_genome_manager.py, put it in the genome folder with the other genome managers, and run the following command:
```
python3 run_simmerpop.py GENOME_MANAGER my_genome_manager 
```
The food and gene types are similarly available to be custamized for use in the "Cellulator" build.  
If you have a series of interdependent custom scripts, it would be good practice to give them a common name.  


## Support
For questions regarding or help running the Simmerpop simulation, or to report a bug or unexpected behavior, please contact Yuta A. Takagi at <yutaatakagi@gmail.com>.

For questions about using the Simmerpop simulation in your own research, please contact Dr. Aaron D. Goldman at <agoldman@oberlin.edu>.

## Contributing
Anyone is welcome to download, use, and modify the Simmerpop repository to their liking.

If you have created useful or interesting modifications, and would like to contribute them to the distribution version of Simmerpop, please contact Yuta A. Takagi at <yutaatakagi@gmail.com>.

## Authors and acknowledgment
Yuta A. Takagi, Diep H. Nguyen, Tom Wexler, Aaron D. Goldman

Funding for this work was provided by the National Aeronautics and Space Administration, grants 16-IDEAS16-0001 and 80NSSC19M0069, and the National Science Foundation, grant MRI1427949.

## Selected publications
!!Add our paper reference here when published

## License
!!Add a public license
