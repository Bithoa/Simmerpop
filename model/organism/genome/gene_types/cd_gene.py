#!/usr/bin/env python

"""
This file is part of Simmerpop which is released under the GNU General Purpose License version 3. 
See COPYING or go to <https://www.gnu.org/licenses/> for full license details.
"""

__authors__ = ['Yuta A. Takagi', 'Diep H. Nguyen']
__copyright__ = 'Copyright 2019, Goldman Lab'
__license__ = 'GPLv3'

# holds the class definition for the 'Gene' parent class. see the 'custom_gene_template' module for details.
# change this module at your own risk


# the 'Gene' parent class
class Gene:
	def __init__(self, organism):
		self.organism = organism
		self.value = None
		self.test_value = None
		self.can_be_first_gene = None

	def __repr__(self):
		raise NotImplementedError

	def execute(self):	# does the action of the gene
		raise NotImplementedError

	def test_execute(self, food, read_head):
		raise NotImplementedError

	def cost(self):
		raise NotImplementedError
