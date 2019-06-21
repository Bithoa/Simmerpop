
#!/usr/bin/env python

"""
This file is part of Simmerpop which is released under the GNU General Purpose License version 3. 
See COPYING or go to <https://www.gnu.org/licenses/> for full license details.
"""

import random

from ... import global_variables
from ..food_types import cd_food_type
from ..food_io import cd_food_io

__authors__ = ['Yuta A. Takagi', 'Diep H. Nguyen']
__copyright__ = 'Copyright 2019, Goldman Lab'
__license__ = 'GPLv3'


# change 'FoodNot' to whatever you'd like to call your food class
# all food should be child classes to the 'Food' class defined in the 'cd_food_type' module
class FoodCustom(cd_food_type.Food):
	def __init__(self):
		# this is the method called when creating instances of this class
		# all variables should be defined and initialized here
		#
		# this class inherits the following variables from its parent class 'Food':
		# self.inputs
		#	a list of eight booleans representing the inputs given to the 'Organism' to solve
		# self.solution
		#	a list of eight corresponding booleans that the 'Organism' stores its current values to.
		# self.id
		#	an id for the instance of this class

		super().__init__()	# this example line initializes variables using the 'Gene' class '__init__()' method

		# the following example lines set each of the 'self.inputs' values to a random value
		for i in range(8):
			self.inputs[i] = random.choice([True, False])

		# the following example lines use the 'make_food_id()' function defined in the 'cd_food_io' module to generate
		# a unique id for this food instance
		self.id = cd_food_io.make_food_id()

		self.example = 'Hello'	# this example line defines a variable 'example' unique to this food type

	def __repr__(self):
		# this is the method called when a string representation of this food is required (ex. if you print() this food)
		# if you would like to enable saving functionality with your custom food type you will need to create/modify
		# your 'FoodIO' class to recreate this food instance based the string representation returned here.

		# although you can handle this however you'd like, I would suggest you follow the format I have used in my food
		# classes. a continuous string with each section separated by an underscore '_'. the first section is an
		# identifying string unique for this gene type. the second section is the current 'self.input' list. the third
		# section is the current 'self.solution' list. all other variables follow.

		return 'FoodCustom_' + str(self.inputs) + '_' + str(self.solution) + '_' + str(self.example)

	def check_solution(self):
		# this method is called to see how well the organism solution matches the correct solution and returns a list
		# of two items, the number of correct positions out of the eight, and the amount of corresponding reward energy

		# the following example lines defines the correct solution as the same values as the 'self.inputs' values and
		# counts the number of correct solutions
		num_correct = 0
		for i in range(8):
			if self.solution == self.inputs[i]:
				num_correct += 1

		# the following example line defines the energy reward as the number of correct solutions multiplied by five
		reward = num_correct * 5

		# then return these values.
		return [num_correct, reward]
