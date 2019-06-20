# Simmerpop
Simmulation of Emergent Populations

## Description
Simmerpop is a repository of code for conducting virtual life simmulations. It was developed with a focus on simmulating early life ecosystems to further our understanding of the origin of life. 

## Usage
The Simmerpop repository is freely available on GitHub at the url: 
https://github.com/GoldmanLab/Simmerpop/

To run the simmulation, download the entire code repository to the desired location on your machine. 

Then run the python 3 script from the Simmerpop root directory. 
If you do not have python 3 installed on your machine, it is available [here](https://www.python.org/downloads/).

#### Mac
Open the Terminal app (found in Applications -> Utilities) and navigate to the Simmerpop folder from the command line
Tip: you can simply type cd, then drag and drop the folder from the finder window
```
cd /filepath_example/Simmerpop
```
Now execute the run_simmerpop.py script
```
python3 run_simmerpop.py
```
Additional arguments can be provided to change the simmulation's behavior. See [User definable arguments](#user-definable-arguments).
Example:
```
python3 run_simmerpop.py KEY value
```

#### Linux
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
Additional arguments can be provided to change the simmulation's behavior. See "User definable arguments"
Example:
```
python3 run_simmerpop.py KEY value
```

#### Windows
Open the Windows terminal by going to the Start menu and selecting "Run...", then type ```cmd```. Now navigate to the Simmerpop folder from the command line
```
cd \example_filepath\Simmerpop
```
Now execute the run_simmerpop.py script
```
run_simmerpop.py
```
If that doesn't work make sure your PATH contains the python dictionary. See [how to get python](https://en.wikibooks.org/wiki/Python_Programming/Getting_Python).

Additional arguments can be provided to change the simmulation's behavior. See "User definable arguments"
Example:
```
run_simmerpop.py KEY value
```

### User definable arguments

global_variables.py
MUTATION_INTERVAL # (int) <100> set how frequently mutation actions are performed
ENERGY_IO # (string) <'cellulator_energy_io'> select what energy IO script to use
FOOD_IO # (string) <'cellulator_food_io'> select what food IO script to use
GENOME_MANAGER # (string) <'cellulator_genome_manager'> select what genome manager script to use

analytics.py
OUTPUT_FOLDER_NAME # (string) <'default_folder_name'> a folder name for the results folder

population_manager.py
POPULATION_CAP # (int) <10000> the maximum population
START_POPULATION # (int) <10000> the starting population number

end_conditions.py
MAX_NUM_STEPS # (int) <100000> the maximum number of steps to run
MAX_RUN_TIME # (int) <6000> the maximum runtime in minutes

organism.py
METABOLIC_QUALITY_CHECK_COUNT # (int) <1000> the number of replicate sample foods to solve when calculating the genome quality
ENERGY_FACTOR # (float) <2.0> the starting energy of organisms is the genome length * the ENERGY_FACTOR

template_genome_manager.py
KEY_FOR_EXAMPLE_MUTATION_PROB # (float) <0.001> template example for implementing key value pairs. 

cellulator_genome_manager.py
LOOSE_GENE_POOL_CAP # (int) <1000> max number of loose genome fragments
MUTATION_PROB # (float) <0.005> the probability of a mutation occuring 
POINTER_MUT_PROB # (float) <MUTATION_PROB> probability of a gene pointer mutating 
DELETION_PROB # (float) <MUTATION_PROB> probability of a gene being deleted 
INSERTION_PROB # (float) <MUTATION_PROB> probability of a gene being inserted between each gene 
INS_GET_WT # (int) <10> the relative proportion of 'GeneGet' genes being inserted
INS_PUT_WT # (int) <10> the relative proportion of 'GenePut' genes being inserted
INS_NAND_WT # (int) <30> the relative proportion of 'GeneNAND' genes being inserted
INS_CELL_WT # (int) <5> the relative proportion of 'GeneCellularity' genes being inserted
GENOME_BREAK_PROB # (float) <0.1> probability of a genome fragmenting after each gene
NUM_CELLGENES # (int) <0> initial number of cellularity genes in the starting genome
HGT_PROB # (float) <0.5> probability of horizontal gene transfer

custom_energy_io_template.py
EXAMPLE_VARIABLE # (float) <0.1> an example

cellulator_energy_io.py
ENERGY_LIMIT 	# (int) # <0> a flag indicating the behavior of the energy IO. 
# 0 = regular addition of energy and no energy pool cap
# 1 = a single burst of energy at the start and an energy pool size limited to the ENERGY_CAP_PROPORTION*POPULATION_CAP
# 2 = a single burst of energy at the start and no energy pool cap
ENERGY_CAP_PROPORTION # (float) <0.25> multiplied by the POPULATION_CAP to determine the energy pool cap limit if the ENERGY_LIMIT flag is set to 1
NEW_ENERGY_PARCEL_SIZE # (int) <500> the amount of energy in newly added energy parcels 

custom_food_io_template.py
EXAMPLE_VARIABLE # (float) <0.1> an example

food_type_not.py
# the energy_reward = n^x-a*A where 
# n = the number of digits correctly solved in the food puzzle
# x = FOODNOT_BASE_PAYOFF_EXPONENT
# a = FOODNOT_PAYOFF_ADJUSTMENT_FACTOR
# A = the adjustment amount
# the adjustment amount A increments by 1 per step if the current population size is over FOODNOT_REDUCE_PAYOFF_WHEN_OVER * POPULATION_CAP
# the adjustment amount A decrements by 1 per step if the current population size is under FOODNOT_INCREASE_PAYOFF_WHEN_UNDER * POPULATION_CAP
FOODNOT_BASE_PAYOFF_EXPONENT # (int) <3> 
FOODNOT_PAYOFF_ADJUSTMENT_FACTOR (float) <0.1>
FOODNOT_REDUCE_PAYOFF_WHEN_OVER (float) <1.0>
FOODNOT_INCREASE_PAYOFF_WHEN_UNDER (float) <0.5>





## Support

## Contributing

## Authors and acknowledgment
Yuta A. Takagi, Diep H. Nguyen, Tom Wexler, Aaron D. Goldman

Funding for this work was provided by the National Aeronautics and Space Administration, grants 16-IDEAS16-0001 and 80NSSC19M0069, and the National Science Foundation, grant MRI1427949.

## Selected publications
The origin of cellularity and organismal individuality through digital life simulations 

## License

