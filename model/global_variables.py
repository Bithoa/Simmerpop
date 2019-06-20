# global_variables.py
from . import population_manager
from . import analytics
import importlib
import os

__author__ = 'Yuta A. Takagi (2016) & Diep H. Nguyen (2018)'


# defines a number of important globally used variables.

# a dictionary of variables created from command line arguments at runtime.
parameters = {}


# user defined static variables
# ====================================================================================================
# ****************************************************************************************************

# set how frequently mutation actions are performed
MUTATION_INTERVAL = 100

# global In/Out object instances accessed by the model. navigate to the appropriate module using the python hierarchy:
# separate folders and modules are separated by '.'s

# the energy IO script to use.
MODULE_ENERGY_IO = importlib.import_module('model.energy.energy_io.cellulator_energy_io')

# the food IO script to use.
MODULE_FOOD_IO = importlib.import_module('model.food.food_io.cellulator_food_io')

# the genome manager script to use.
MODULE_GENOME_MANAGER = importlib.import_module('model.organism.genome.cellulator_genome_manager')



POPULATION_CAP = 10000	# the maximum population

START_POPULATION = 10000  # the starting population number

# ****************************************************************************************************
# ====================================================================================================


# create instances of global in/outs
ENERGY_IO = None
FOOD_IO = None
GENOME_MANAGER = None


# global dynamic variables accessed by the model
# the current time step
step_num = None


# initialize the global variables
def init_global_variables(command_line_args):
	# initialize the step number to -1 so the first step increments to 0
	global step_num
	step_num = -1

	# populate the dictionary named 'parameters' from the command line arguments
	global parameters
	i = 1
	while i < len(command_line_args)-1 :
		key = command_line_args[i]
		val = command_line_args[i+1]
		parameters.update({key : val})
		i = i + 2

	# set custom values of variables from command line arguments
	global MUTATION_INTERVAL
	global MODULE_ENERGY_IO
	global MODULE_FOOD_IO
	global MODULE_GENOME_MANAGER
	global POPULATION_CAP
	global START_POPULATION
	
	if 'MUTATION_INTERVAL' in parameters.keys():
		MUTATION_INTERVAL = int(parameters.get('MUTATION_INTERVAL'))
	if 'ENERGY_IO' in parameters.keys():
		MODULE_ENERGY_IO = importlib.import_module('model.energy.energy_io.' + parameters.get('ENERGY_IO'))
	if 'FOOD_IO' in parameters.keys():
		MODULE_FOOD_IO = importlib.import_module('model.food.food_io.' + parameters.get('FOOD_IO'))
	if 'GENOME_MANAGER' in parameters.keys():
		MODULE_GENOME_MANAGER = importlib.import_module('model.organism.genome.' + parameters.get('GENOME_MANAGER'))
	if 'POPULATION_CAP' in parameters.keys():
		POPULATION_CAP = int(parameters.get('POPULATION_CAP'))
	if 'START_POPULATION' in parameters.keys():
		START_POPULATION = int(parameters.get('START_POPULATION'))
		
	try:
		MODULE_ENERGY_IO.init_script()
	except:
		pass
	try:
		MODULE_FOOD_IO.init_script()
	except:
		pass
	try:
		MODULE_GENOME_MANAGER.init_script()
	except:
		pass
	
	global ENERGY_IO
	global FOOD_IO
	global GENOME_MANAGER
	
	ENERGY_IO = MODULE_ENERGY_IO.EnergyIO()
	FOOD_IO = MODULE_FOOD_IO.FoodIO()
	GENOME_MANAGER = MODULE_GENOME_MANAGER.GenomeManager()

