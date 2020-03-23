#!/usr/bin/env python

"""
This file is part of Simmerpop which is released under the GNU General Purpose License version 3. 
See COPYING or go to <https://www.gnu.org/licenses/> for full license details.
"""

import copy
import itertools
import random

from .. import global_variables

__authors__ = ['Yuta A. Takagi', 'Diep H. Nguyen']
__copyright__ = 'Copyright 2019, Goldman Lab'
__license__ = 'GPLv3'

# ====================================================================================================
# ****************************************************************************************************

METABOLIC_QUALITY_CHECK_COUNT = 1000  # the number of replicate sample foods to solve when calculating the genome quality
ENERGY_FACTOR = 2 # the starting energy of organisms is the genome length * the ENERGY_FACTOR
OVERRIDE_ENERGY_TRANSFER_PROB = None # overrides organisms' cellularity with a constant probability when determining energy transfer
OVERRIDE_GENE_TRANSFER_PROB = None # overrides organisms' cellularity with a constant probability when determining gene transfer

# ****************************************************************************************************
# ====================================================================================================


# initialize organism.py
def init_script():
	global METABOLIC_QUALITY_CHECK_COUNT
	global ENERGY_FACTOR
	global OVERRIDE_ENERGY_TRANSFER_PROB
	global OVERRIDE_GENE_TRANSFER_PROB
	# populate the dictionary named 'parameters' from the command line arguments
	if 'METABOLIC_QUALITY_CHECK_COUNT' in global_variables.parameters.keys():
		METABOLIC_QUALITY_CHECK_COUNT = int(global_variables.parameters.get('METABOLIC_QUALITY_CHECK_COUNT'))
	if 'ENERGY_FACTOR' in global_variables.parameters.keys():
		ENERGY_FACTOR = float(global_variables.parameters.get('ENERGY_FACTOR'))
	if 'OVERRIDE_ENERGY_TRANSFER_PROB' in global_variables.parameters.keys():
		OVERRIDE_ENERGY_TRANSFER_PROB = float(global_variables.parameters.get('OVERRIDE_ENERGY_TRANSFER_PROB'))
	if 'OVERRIDE_GENE_TRANSFER_PROB' in global_variables.parameters.keys():
		OVERRIDE_GENE_TRANSFER_PROB = float(global_variables.parameters.get('OVERRIDE_GENE_TRANSFER_PROB'))


# variables for the 'make_gene_id()' method
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
make_hash_depth = 1
make_hash_iterator = iter(ALPHA)


# creates a unique hash value
def make_hash():
	global make_hash_depth
	global make_hash_iterator
	try:
		return ''.join(next(make_hash_iterator))
	except StopIteration:
		make_hash_depth += 1
		make_hash_iterator = itertools.product(ALPHA, repeat=make_hash_depth)
		return ''.join(next(make_hash_iterator))


# creates a unique organism id combined of its parent's id, a dash '-', and its own new id
def make_id(parent_id):
	offspring_id = parent_id.split('-')[1]
	offspring_id += '-'
	offspring_id += make_hash()
	return offspring_id


# initialize an organism from a string representation
def init_organism_from_string_repr(string_repr):
	repr_params = string_repr.split('#')

	to_return = Organism()
	to_return.id = repr_params[0]
	to_return.genome = \
		[global_variables.GENOME_MANAGER.init_gene_from_string_repr(to_return, gene_as_string)
		 for gene_as_string in repr_params[1].strip('[]').split(', ')]
	to_return.energy = float(repr_params[2])
	to_return.genome_read_head = int(repr_params[3])
	to_return.food = global_variables.FOOD_IO.init_food_from_string_repr(repr_params[4])
	to_return.replicate_me = repr_params[5] == 'True'
	to_return.alive = repr_params[6] == 'True'
	to_return.mutated = repr_params[7] == 'True'
	to_return.calc_metabolic_efficiency()
	to_return.calc_cellularity()
	return to_return


# the 'Organism' class defines organisms
class Organism:
	# initializes the organism
	def __init__(self):
		self.genome = None
		self.make_genome()
		self.energy = self.init_energy()
		self.genome_read_head = 0
		self.cellularity = None	 # 0. to 1. with 0 being completely leaky and 1 being completely closed off
		self.calc_cellularity()
		self.food_index = None
		self.food_stockpile = []
		self.replicate_me = False
		self.alive = True
		self.mutated = True
		self.position = None
		self.genome_size = len(self.genome)

		# for analytics
		self.id = None
		self.last_solution_num_correct = 0
		self.metabolic_efficiency = 0
		self.age = 0
		self.generation = 0

	# creates a string representation of the organism
	def __repr__(self):
		to_return = '<<'
		to_return += self.id + '#'
		to_return += str(self.genome) + '#'
		to_return += str(self.energy) + '#'
		to_return += str(self.genome_read_head) + '#'
		to_return += str(self.food_index) + '#'
		to_return += str(self.food_stockpile) + '#'
		to_return += str(self.replicate_me) + '#'
		to_return += str(self.alive) + '#'
		to_return += str(self.mutated) + '>>'
		return to_return

	# executes the next step in the genome
	def step(self, *args):
		if len(args) > 0:
			self.position = args[0]

		# reset mutated flag
		self.mutated = False

		# increase organism's age counter
		self.age += 1

		# if organism has no food, try to get food
		if self.food_index is None:
			#self.food = global_variables.FOOD_IO.get_food()
			if len(self.food_stockpile) > 0:
				self.food_index = random.randrange(len(self.food_stockpile))
			self.energy -= 1

		# if organism has food
		else:
			# execute current gene
			temp_gene = self.genome[self.genome_read_head]
			temp_gene.execute()
			self.energy -= temp_gene.cost()

			# move the read head position
			self.genome_read_head += 1

			# if organism has reached the end of its genome
			if self.genome_read_head == len(self.genome):
				self.genome_read_head = 0
				solution = self.food_stockpile[self.food_index].check_solution()
				self.energy += solution[1]
				self.last_solution_num_correct = solution[0]  # analytics
				#global_variables.FOOD_IO.discard_food(self.food)
				global_variables.FOOD_IO.discard_food(self.food_stockpile.pop(self.food_index))
				#self.food = None
				self.food_index = None
				if self.energy >= self.init_energy()*2:
					self.replicate_me = True
				for gene in self.genome:
					gene.val = None

		# dies if it runs out of energy
		if self.energy <= 0:
			self.alive = False

	# creates a de novo genome defined in the 'GenomeManager' you are using
	def make_genome(self):
		self.genome = global_variables.GENOME_MANAGER.make_genome(self)

	# returns an offspring of the organism
	def replicate(self):
		to_return = Organism()
		# calculate new energy
		to_return.energy = self.energy/2
		if to_return.energy >= self.init_energy()*2:
			to_return.replicate_me = True
		# copy genome
		to_return.genome = copy.deepcopy(self.genome)
		for gene in to_return.genome:
			gene.organism = to_return
		# set to correct analytical values
		to_return.id = make_id(self.id)
		to_return.last_solution_num_correct = self.last_solution_num_correct
		to_return.metabolic_efficiency = self.metabolic_efficiency
		to_return.cellularity = self.cellularity
		to_return.generation = self.generation + 1
		to_return.genome_size = len(to_return.genome)
		return to_return

	# passively gain energy based on cellularity
	def gain_energy(self):
		global OVERRIDE_ENERGY_TRANSFER_PROB
		if OVERRIDE_ENERGY_TRANSFER_PROB is None:
			if self.cellularity <= random.random():
				self.energy += global_variables.ENERGY_IO.get_energy(self)
		else:
			if OVERRIDE_ENERGY_TRANSFER_PROB > random.random():
				self.energy += global_variables.ENERGY_IO.get_energy(self)

	# passively lose energy based on cellularity
	def lose_energy(self):
		global OVERRIDE_ENERGY_TRANSFER_PROB
		if OVERRIDE_ENERGY_TRANSFER_PROB is None:
			if self.cellularity <= random.random():
				self.energy -= global_variables.ENERGY_IO.discard_energy(self)
		else:
			if OVERRIDE_ENERGY_TRANSFER_PROB > random.random():
				self.energy -= global_variables.ENERGY_IO.discard_energy(self)

	# passively gain genes based on cellularity
	def gain_genes(self):
		global OVERRIDE_GENE_TRANSFER_PROB
		if OVERRIDE_GENE_TRANSFER_PROB is None:
			if self.cellularity <= random.random():
				global_variables.GENOME_MANAGER.gain_genes(self)
		else:
			if OVERRIDE_GENE_TRANSFER_PROB > random.random():
				global_variables.GENOME_MANAGER.gain_genes(self)
		self.genome_size = len(self.genome)

	# passively lose genes based on cellularity
	def lose_genes(self):
		global OVERRIDE_GENE_TRANSFER_PROB
		if OVERRIDE_GENE_TRANSFER_PROB is None:
			if self.cellularity <= random.random():
				global_variables.GENOME_MANAGER.lose_genes(self)
		else:
			if OVERRIDE_GENE_TRANSFER_PROB > random.random():
				global_variables.GENOME_MANAGER.lose_genes(self)
		self.genome_size = len(self.genome)
		
	# passively add food to food_stockpile
	def gain_food(self):
		if self.cellularity <= random.random():
			self.food_stockpile.append(global_variables.FOOD_IO.get_food())
	
	# passively remove food from food_stockpile
	def lose_food(self):
		if len(self.food_stockpile) > 0:
			if self.cellularity <= random.random():
				# discard a random food
				index_to_discard = random.randrange(len(self.food_stockpile))
				global_variables.FOOD_IO.discard_food(self.food_stockpile.pop(index_to_discard))
				# if the organism is currently working on a food
				if self.food_index is not None:
					# when the current food being worked on is discarded
					if index_to_discard == self.food_index:
						self.food_index = None
					# adjust the food_index if a food earlier in the food_stockpile list is deleted
					elif index_to_discard < self.food_index:
						self.food_index -= 1
	
	# mutate genome
	def mutate(self):
		global_variables.GENOME_MANAGER.mutate(self)
		self.genome_size = len(self.genome)

	# returns the starting energy of a new organism
	def init_energy(self):
		global ENERGY_FACTOR
		return ENERGY_FACTOR*len(self.genome)

	# calculates the genome quality
	def calc_metabolic_efficiency(self):
		global METABOLIC_QUALITY_CHECK_COUNT
		temp_genome = copy.copy(self.genome)
		metabolic_efficiency = 0
		for x in range(METABOLIC_QUALITY_CHECK_COUNT):
			temp_food = global_variables.FOOD_IO.get_test_food()
			for i, gene in enumerate(temp_genome):
				gene.test_execute(temp_food, i)
			metabolic_efficiency += temp_food.check_solution()[0]
		metabolic_efficiency /= float(METABOLIC_QUALITY_CHECK_COUNT)
		self.metabolic_efficiency = metabolic_efficiency

		return metabolic_efficiency

	# calculates the genome cellularity by a function defined in the GenomeManager you are using
	def calc_cellularity(self):
		self.cellularity = global_variables.GENOME_MANAGER.calculate_cellularity(self)
