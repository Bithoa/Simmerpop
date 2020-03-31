#!/usr/bin/env python

"""
This file is part of Simmerpop which is released under the GNU General Purpose License version 3. 
See COPYING or go to <https://www.gnu.org/licenses/> for full license details.
"""

import random

from . import cd_food_io
from ..food_types import food_type_not
from ... import global_variables

__authors__ = ['Yuta A. Takagi', 'Diep H. Nguyen']
__copyright__ = 'Copyright 2019, Goldman Lab'
__license__ = 'GPLv3'


# this food In/Out is designed for Yuta's model and utilizes the following food types:
# FoodNot
#
# it provides a 'FoodNot' food every time an organism requests a food


# the number of food in a newly added food parcel
FOOD_CAP_PROPORTION = 1.5
LOOSE_FOOD_POOL_CAP = 10000
NEW_FOOD_PARCEL_SIZE = 5


# initialize the food_type_not script
def init_script():
	food_type_not.init_script()


class FoodIO(cd_food_io.FoodIO):  # this class name cannot be altered. Leave as 'FoodIO'  
	def __init__(self):
		global FOOD_CAP_PROPORTION
		global LOOSE_FOOD_POOL_CAP
		global NEW_FOOD_PARCEL_SIZE
		self.loose_food_parcels = []

		if 'FOOD_CAP_PROPORTION' in global_variables.parameters.keys():
			FOOD_CAP_PROPORTION = float(global_variables.parameters.get('FOOD_CAP_PROPORTION'))
		LOOSE_FOOD_POOL_CAP = int(FOOD_CAP_PROPORTION*global_variables.POPULATION_CAP)
		if 'NEW_ENERGY_PARCEL_SIZE' in global_variables.parameters.keys():
			NEW_FOOD_PARCEL_SIZE = int(global_variables.parameters.get('NEW_FOOD_PARCEL_SIZE'))
	
	def next_step(self):
		food_type_not.calc_food_payoff_reduction_factor()
		if global_variables.step_num % global_variables.MUTATION_INTERVAL == 0:
			self.add_food()
			self.cull_food_pool()
		
	def add_food(self):
		global NEW_FOOD_PARCEL_SIZE
		global LOOSE_FOOD_POOL_CAP
		while len(self.loose_food_parcels) <= LOOSE_FOOD_POOL_CAP:
			temp = []
			for i in range(NEW_FOOD_PARCEL_SIZE):
				temp.append(food_type_not.FoodNot())
			self.loose_food_parcels.append(temp)

	def cull_food_pool(self):
		global LOOSE_FOOD_POOL_CAP:
		while len(self.loose_food_parcels) > LOOSE_FOOD_POOL_CAP:
			remove_me = random.randint(0, len(self.loose_food_parcels) - 1)
			self.loose_food_parcels.pop(remove_me)

	def get_food(self):
		temp = len(self.loose_food_parcels)
		if temp > 0:
			return self.loose_food_parcels.pop(random.randint(0, temp - 1))
		else:
			return []

	def get_test_food(self):
		return food_type_not.FoodNot()

	def discard_food(self, organism):
		#self.loose_food_parcels.append(food_to_discard)
		
		if len(organism.food_stockpile) > 0:
			# deletes a random number of food parcels up to half of the organism's energy stock
			maximum = len(organism.food_stockpile) / 2
			num_to_lose = int(maximum*random.random())
			parcel_to_lose = []
			for i in range(num_to_lose):				
				# discard a random food
				index_to_discard = random.randrange(len(organism.food_stockpile))
				parcel_to_lose.append(organism.food_stockpile.pop(index_to_discard))
				# if the organism is currently working on a food
				if organism.food_index is not None:
					# when the current food being worked on is discarded
					if index_to_discard == organism.food_index:
						organism.food_index = None
						organism.food = None
					# adjust the food_index if a food earlier in the food_stockpile list is deleted
					elif index_to_discard < organism.food_index:
						organism.food_index -= 1
						
			self.loose_energy_parcels.append(parcel_to_lose)

	def init_food_from_string_repr(self, string_repr):
		repr_params = string_repr.split('_')
		to_return = None
		if repr_params[0] == 'FoodNot':
			to_return = food_type_not.FoodNot()
			to_return.inputs = [input_as_string == 'True' for input_as_string in repr_params[1].strip('[]').split(', ')]
			to_return.solution = \
				[None if solution_as_string == 'None' else solution_as_string == 'True'
				 for solution_as_string in repr_params[2].strip('[]').split(', ')]
		return to_return
