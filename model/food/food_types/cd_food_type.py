
#!/usr/bin/env python

"""
This file is part of Simmerpop which is released under the GNU General Purpose License version 3. 
See COPYING or go to <https://www.gnu.org/licenses/> for full license details.
"""

from ... import global_variables

__authors__ = ['Yuta A. Takagi', 'Diep H. Nguyen']
__copyright__ = 'Copyright 2019, Goldman Lab'
__license__ = 'GPLv3'


# holds the class definition for the 'Food' parent class. see the 'custom_food_template' module for details
# change this module at your own risk


# the 'Food' parent class
class Food:
	def __init__(self):
		self.inputs = [None, None, None, None, None, None, None, None]
		self.solution = [None, None, None, None, None, None, None, None]
		self.id = None

	def __repr__(self):
		raise NotImplementedError

	def check_solution(self):
		raise NotImplementedError
