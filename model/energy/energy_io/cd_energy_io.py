#!/usr/bin/env python

"""
This file is part of Simmerpop which is released under the GNU General Purpose License version 3. 
See COPYING or go to <https://www.gnu.org/licenses/> for full license details.
"""

import itertools

from ... import global_variables

__authors__ = ['Yuta A. Takagi', 'Diep H. Nguyen']
__copyright__ = 'Copyright 2019, Goldman Lab'
__license__ = 'GPLv3'


# holds the class definition for the 'EnergyIO' parent class. see the 'custom_energy_io_template' module for details.
# change this module at your own risk


# variables for the 'make_energy_id()' method
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
make_e_hash_depth = 1
make_e_hash_iterator = iter(ALPHA)


# makes a unique id for energy parcels
def make_energy_id():
	global make_e_hash_depth
	global make_e_hash_iterator
	try:
		return 'e*' + ''.join(next(make_e_hash_iterator))
	except StopIteration:
		make_e_hash_depth += 1
		make_e_hash_iterator = itertools.product(ALPHA, repeat=make_e_hash_depth)
		return 'e*' + ''.join(next(make_e_hash_iterator))


# the 'EnergyIO' parent class
class EnergyIO:
	def __init__(self):
		pass
	
	def next_step(self):
		pass

	def get_energy(self, organism):
		raise NotImplementedError

	def discard_energy(self, organism):
		raise NotImplementedError
