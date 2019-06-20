# cellulator_food_io.py
from . import cd_food_io
from ..food_types import food_type_not
import random

__author__ = 'Yuta A. Takagi (2016) & Diep Nguyen (2018)'


# this food In/Out is designed for Yuta's model and utilizes the following food types:
# FoodNot
#
# it provides a 'FoodNot' food every time an organism requests a food


# initialize the food_type_not script
def init_script():
	food_type_not.init_script()


class FoodIO(cd_food_io.FoodIO):  # this class name cannot be altered. Leave as 'FoodIO'  
	def next_step(self):
		food_type_not.calc_food_payoff_reduction_factor()

	def get_food(self):
		return food_type_not.FoodNot()

	def get_test_food(self):
		return food_type_not.FoodNot()

	def discard_food(self, food_to_discard):
		pass

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
