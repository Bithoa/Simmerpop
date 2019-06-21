#!/usr/bin/env python

"""
This file is part of Simmerpop which is released under the GNU General Purpose License version 3. 
See COPYING or go to <https://www.gnu.org/licenses/> for full license details.
"""

import random

from ... import global_variables
from ... import population_manager
from ..food_types import cd_food_type
from ..food_io import cellulator_food_io

__authors__ = ['Yuta A. Takagi', 'Diep H. Nguyen']
__copyright__ = 'Copyright 2019, Goldman Lab'
__license__ = 'GPLv3'


# this food type is designed for Yuta's model
#
# the solution is the simple inverse (boolean not) of each input position
# the reward is the number of correct solutions raised to a power (3 by default), minus a dynamically adapting quantity who's
# value increases if the population is healthy, but decreases if organisms are dying

# the energy_reward = n^x-a*A where 
# n = the number of digits correctly solved in the food puzzle
# x = FOODNOT_BASE_PAYOFF_EXPONENT
# a = FOODNOT_PAYOFF_ADJUSTMENT_FACTOR
# A = the adjustment amount
# the adjustment amount A increments by 1 per step if the current population size is over FOODNOT_REDUCE_PAYOFF_WHEN_OVER * POPULATION_CAP
# the adjustment amount A decrements by 1 per step if the current population size is under FOODNOT_INCREASE_PAYOFF_WHEN_UNDER * POPULATION_CAP
FOODNOT_BASE_PAYOFF_EXPONENT = 3 
FOODNOT_PAYOFF_ADJUSTMENT_FACTOR = 0.1
FOODNOT_REDUCE_PAYOFF_WHEN_OVER = 1.0
FOODNOT_INCREASE_PAYOFF_WHEN_UNDER = 0.5

adjustment = 0

def init_script():
	global FOODNOT_BASE_PAYOFF_EXPONENT
	global FOODNOT_PAYOFF_ADJUSTMENT_FACTOR
	global FOODNOT_REDUCE_PAYOFF_WHEN_OVER
	global FOODNOT_INCREASE_PAYOFF_WHEN_UNDER
	if 'FOODNOT_BASE_PAYOFF_EXPONENT' in global_variables.parameters.keys():
		FOODNOT_BASE_PAYOFF_EXPONENT = float(global_variables.parameters.get('FOODNOT_BASE_PAYOFF_EXPONENT'))
	if 'FOODNOT_PAYOFF_ADJUSTMENT_FACTOR' in global_variables.parameters.keys():
		FOODNOT_PAYOFF_ADJUSTMENT_FACTOR = float(global_variables.parameters.get('FOODNOT_PAYOFF_ADJUSTMENT_FACTOR'))
	if 'FOODNOT_REDUCE_PAYOFF_WHEN_OVER' in global_variables.parameters.keys():
		FOODNOT_REDUCE_PAYOFF_WHEN_OVER = float(global_variables.parameters.get('FOODNOT_REDUCE_PAYOFF_WHEN_OVER'))
	if 'FOODNOT_INCREASE_PAYOFF_WHEN_UNDER' in global_variables.parameters.keys():
		FOODNOT_INCREASE_PAYOFF_WHEN_UNDER = float(global_variables.parameters.get('FOODNOT_INCREASE_PAYOFF_WHEN_UNDER'))
	

def calc_food_payoff_reduction_factor():
	global adjustment
	global FOODNOT_REDUCE_PAYOFF_WHEN_OVER
	global FOODNOT_INCREASE_PAYOFF_WHEN_UNDER
	if len(population_manager.organisms) > (global_variables.POPULATION_CAP * FOODNOT_REDUCE_PAYOFF_WHEN_OVER):
		adjustment += 1
	if len(population_manager.organisms) <= (global_variables.POPULATION_CAP * FOODNOT_INCREASE_PAYOFF_WHEN_UNDER):
		adjustment -= 1

class FoodNot(cd_food_type.Food):  # the not of the input
	def __init__(self):
		super().__init__()
		for i in range(8):
			self.inputs[i] = random.choice([True, False])
		self.position_solved = [False, False, False, False, False, False, False, False]
		self.quality = 8
		self.spent = False

	def __repr__(self):
		return 'FoodNot_' + str(self.inputs) + '_' + str(self.solution)

	def check_solution(self):
		if self.spent:
			raise Exception('bad!!!!!!')
		correct_solution = []
		for val in self.inputs:
			correct_solution.append(not val)
		num_correct = 0
		for i in range(8):
			if (not self.position_solved[i]) and (self.solution[i] is not None):
				if self.solution[i] == correct_solution[i]:
					num_correct += 1
					self.position_solved[i] = True
					
		reward = self.calc_food_payoff(num_correct)
		
		if self.position_solved == [True, True, True, True, True, True, True, True]:
			self.spent = True
		to_return = [num_correct, reward]
		self.quality -= num_correct
		return to_return
	
	def calc_food_payoff(self, num_correct):
		global FOODNOT_BASE_PAYOFF_EXPONENT
		global FOODNOT_PAYOFF_ADJUSTMENT_FACTOR
		reward = (num_correct ** FOODNOT_BASE_PAYOFF_EXPONENT) - (adjustment * FOODNOT_PAYOFF_ADJUSTMENT_FACTOR)
		if reward < 0:
			reward = 0
		return reward


